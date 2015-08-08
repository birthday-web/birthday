from django.shortcuts import render,redirect
from home.models import *
from home.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime
import os
import json
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import traceback

def err_404(request):
	return render(request,'404.html')

def err_500(request):
	return render(request,'500.html')	
	
def get_by_bday(request):
	friends=request.user.friend.friends.filter(to_friend__status=FRIENDSHIP_FRIEND)
	upc=[]
	mnt_srt=[]
	for x in range(12):
		mnt_srt.append([])
	today=datetime.date.today()
	for x in friends:
		mnt_srt[x.date_of_birth.month-1].append(x)
	curr_mnt=today.month-1
	last=[]
	for y in range(12):
		# insertion sort
		x=mnt_srt[curr_mnt]
		l=len(x)
		if l>1:
			j,i=1,0
			while j<l:
				i=j-1
				tmp=x[j]
				while i>=0 and tmp.date_of_birth.day<x[i].date_of_birth.day:
					x[i+1]=x[i]
					i-=1
				x[i+1]=tmp
				j+=1
		upc.extend(x)
		if curr_mnt==today.month-1:# in first loop only
			k=0
			while k<len(upc) and upc[k].date_of_birth.day<today.day:
				k+=1
			last=upc[:k]
			upc=upc[k:]
		curr_mnt+=1
		if curr_mnt==12:
			curr_mnt=0
	upc.extend(last)
	return upc
	
# Create your views here.

def do_logout(request):
	if request.method=='POST':
		data={}
		logout(request)
		data['status']=True
		data['msg']='successfully sign out'
		return HttpResponse(json.dumps(data),content_type="application/json")
	else:
		return HttpResponseRedirect("/")

def do_login(request):
	data={}
	if request.method=='POST':
		print 'post request',data
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username, password=password)
		print user
		if user:
			if user.is_active:
				login(request,user)
				data['full_name']=user.get_full_name()
				data['username']=user.username
				data['email']=user.email
				data['post_count']=user.friend.post_set.count()
				data['image_url']=user.friend.image.url
				data['date_of_birth']=user.friend.date_of_birth.strftime('%d-%B-%Y')
				data['status']=True
				data['msg']='Success, redirecting..'
			else:
				data['status']=False
				data['error']='Your account is inavtive, wait for referal confirmation'
		else:
			data['status']=False
			data['error']='Login attemp failed! check username and password'
		return HttpResponse(json.dumps(data),content_type="application/json")
	else:
		return HttpResponseRedirect("/")

def add_friend_request(request):
	if request.user.is_authenticated() and request.method=="POST":
		data={}
		form=AddFriendForm(request.POST)
		if form.is_valid():
			email=form.cleaned_data['email']
			try:
				friend=User.objects.get(email=email).friend
				#already requested ?
				if friend != request.user.friend:
					
					if friend not in request.user.friend.friends.all():
						request.user.friend.add_relationship(friend,FRIENDSHIP_REQUESTED,False)
						data['status']=True
						data['msg']="Request has been created, waiting for approval from your friend"
					else:
						data['status']=False
						if friend in request.user.friend.get_friendships(FRIENDSHIP_BLOCKED):
							data['error']='Your friend has blocked you !!'
						else:
							data['error']='You already have this friend or requested for friendship'
				else:
					data['status']=False
					data['error']='You cannot be friend with yourself'
			except ObjectDoesNotExist:
				data['status']=False
				data['error']='Your friend is not registered with us'
		else:
			print 'not valid'
			data['status']=False
			data['error']="Invalid email address"
		return HttpResponse(json.dumps(data),content_type="application/json")
	else:
		return HttpResponseRedirect("/")
	
def register(request):
	if request.method=='POST':
		print "registration request"
		data={}
		user_enroll_form=UserEnrollForm(request.POST,request.FILES);
		if user_enroll_form.is_valid():
			#create a inactive user and send request
			user_enroll=user_enroll_form.save()
			try:
				reference=User.objects.get(email=user_enroll.reference_email)
			except:
				reference=False
			if reference and reference.is_active:
				print 'reference ok'
				user=User(username=user_enroll.username,email=user_enroll.email)
				user.set_password(user_enroll.password)
				user.first_name=user_enroll.first_name
				user.last_name=user_enroll.last_name
				user.is_active=False
				user.save()
				print user
				user_friend=Friend()
				user_friend.user=user
				user_friend.date_of_birth=user_enroll.date_of_birth
				user_friend.image=user_enroll.image
				user_friend.save()
				print user_friend
				user_friend.add_relationship(reference.friend,FRIENDSHIP_REQUESTED,False)
				data['status']=True
				data['msg']='Congratulations!! you are now registered'
			else:
				data['status']=False
				data['error']='invalid reference'
		else:
			data['status']=False
			data['error']='Correct errors in form and retry !!'
			data['errors']=user_enroll_form.errors
	else:
		data['status']=False
		data['error']='Invalid request'
	return HttpResponse(json.dumps(data),content_type="application/json")

def index_login(request):
	data={}
	data['form']=UserEnrollForm()
	data['login_form']=LoginForm()
	return render(request,'home/login.html',data)
	
def index(request):
	user_enroll_form=UserEnrollForm()
	login_form=LoginForm()
	if not request.user.is_authenticated():
		return index_login(request)
	else:
		friends=get_by_bday(request)
		primary_friends=[]
		for x in friends:
			if x.date_of_birth.month==datetime.date.today().month and x.date_of_birth.day==datetime.date.today().day:
				primary_friends.append(x)
			else:
				break;
		for x in primary_friends:
			friends.remove(x)
		data={
			'add_friend_form':AddFriendForm(),
			 'is_index':True,
			 'form':user_enroll_form,
			'friends':friends,
			'primary_friends':primary_friends,
			'login_form':login_form
		}
		return render(request,'home/index.html',data)

def listPosts(request,username):
	friend=Friend.objects.get(user=User.objects.get(username=username))
	'''
	checks required
	1. user is authenticated
	2. friend is a in friend list of user
	'''
	#check number 1 and 2
	if request.user.is_authenticated() and friend in request.user.friend.get_friendships():
		if request.method=='POST':
		#POST request
			author=request.user.friend
			if 'post_button' in request.POST:
				post_form=PostForm(request.POST,request.FILES)
				if post_form.is_valid():
					post=post_form.save(commit=False)
					post.author=author
					post.friend=friend
					post.save()
					post_form=PostForm()
			elif 'comment_button' in request.POST:
				comment_form=CommentForm(request.POST)
				if comment_form.is_valid():
					print 'comment valid'
					comment=comment_form.save(commit=False)
					comment.author=author
					comment.save()
				else:
					print 'comment invalid'
				post_form=PostForm()
			
		else:
			#GET request
			post_form=PostForm()
		data={'friend':friend,'posts':friend.post_set.all(),'post_form':post_form,'comment_form':CommentForm(),}
		return render(request,'home/list_posts.html',data)
	else:
	#User not authenticated
		return HttpResponseRedirect("/")
	
def delPost(request,username,post_id):
	data={}
	if request.user.is_authenticated():
		try:
			post=Post.objects.get(pk=post_id)
			if post.author.user==request.user:
				#path=post.image.url
				#os.remove(path)
				#post.delete()
				data['result']=True
				data['msg']='Item deleted'
			else:
				data['result']=False
				data['msg']='Your are not owner of this item'
		except:
			data['result']=False
			data['msg']='Error occured'
	else:
		data['result']=False
		data['msg']='User not authenticated'
	return HttpResponse(json.dumps(data),content_type="application/json")
	
def delComment(request,username,comment_id):
	data={}
	if request.user.is_authenticated():
		try:
			comment=Comment.objects.get(pk=comment_id)
			if comment.author.user == request.user:
				#comment.delete()
				data['result']=True
				data['msg']='Item deleted'
			else:
				data['result']=False
				data['msg']='Your are not owner of this item'
		except Exception as e:
			data['result']=False
			data['msg']='Error occured'
			data['err']=e
	else:
		data['result']=False
		data['msg']='User not authenticated'
	return HttpResponse(json.dumps(data),content_type="application/json")

def get_friend_list(request):
	friends=get_by_bday(request)
	primary_friends=[]
	for x in friends:
		if x.date_of_birth.month==datetime.date.today().month and x.date_of_birth.day==datetime.date.today().day:
			primary_friends.append(x)
		else:
			break;
	for x in primary_friends:
		friends.remove(x)
	return primary_friends,friends

def acceptRequest(request,request_id):
	data={}
	if request.user.is_authenticated():	
		try:
			fr=Friendship.objects.get(pk=request_id)
			if fr.status==FRIENDSHIP_REQUESTED and fr.to_person == request.user.friend:
				request.user.friend.add_relationship(fr.from_person,FRIENDSHIP_FRIEND)
				if not fr.from_person.user.is_active: # activate friend
					fr.from_person.user.is_active=True
					fr.from_person.user.save()
				fr.delete()
				data['status']=True
				data['msg']='You are now friend with '+fr.from_person.user.get_full_name()
				primary_friends,friends=get_friend_list(request)
				pf_json=[]
				for x in primary_friends:
					pf={'name':x.user.get_full_name(),
					'username':x.user.username,
					'dob':x.date_of_birth.strftime("%d, %b"),
					'image':x.image.url
					}
					pf_json.append(pf)
				f_json=[]
				for x in friends:
					f={'name':x.user.get_full_name(),
					'username':x.user.username,
					'dob':x.date_of_birth.strftime("%d, %b"),
					'image':x.image.url
					}
					f_json.append(f)
				data['primary_friends']=pf_json
				data['friends']=f_json
				print data
			else:
				data['status']=False
				data['error']='You are not authorized to approve this friendship'
		except ObjectDoesNotExist as ex:
			data['status']=False
			data['error']='No such request'
	else:
		data['status']=False
		data['error']='You must Login first'
	return HttpResponse(json.dumps(data),content_type="application/json")

def rejectRequest(request,request_id):
	data={}
	if request.user.is_authenticated():
		try:
			fr=Friendship.objects.get(pk=request_id)
			if fr.status==FRIENDSHIP_REQUESTED and fr.to_person==request.user.friend:
				#request.user.friend.add_relationship(fr.from_person,FRIENDSHIP_BLOCKED)
				#fr.delete()
				data['status']=True
				data['msg']=fr.from_person.user.get_full_name()+' blocked'
			else:
				data['status']=False
				data['error']='You are not authorized to reject this friendship'
		except ObjectDoesNotExist as ex:
			data['status']=False
			data['error']='No such request'
	else:
		data['status']=False
		data['error']='You must Login first'
	return HttpResponse(json.dumps(data),content_type="application/json")
