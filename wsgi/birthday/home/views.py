from django.shortcuts import render
from home.models import *
from home.forms import *
from django.contrib.auth import authenticate, login, logout
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import datetime


def get_by_bday():
	upc=[]
	mnt_srt=[]
	for x in range(12):
		mnt_srt.append([])
	today=datetime.date.today()
	for x in Friend.objects.all():#order_by('date_of_birth'):
		mnt_srt[x.date_of_birth.month-1].append(x)
	curr_mnt=today.month-1
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
		curr_mnt+=1
		if curr_mnt==12:
			curr_mnt=0
	return upc
	
# Create your views here.
def index(request):
	submit_status=False
	sidebar_msg=''
	user_enroll_form=''
	login_form=''
	if request.method=='POST':
		if 'login_button' in request.POST:
			username=request.POST['username']
			password=request.POST['password']
			user=authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request,user)
					print 'active'
					sidebar_msg='Successfully sign in'
				else:
					print 'inactive'
					sidebar_msg='You are inavtive contact admin'
			else:
				print 'no such user'
				sidebar_msg='no such user'
		elif 'logout_button' in request.POST:
			logout(request)
			sidebar_msg='Successfully sign  out'
		elif 'request_button' in request.POST:			
			user_enroll_form=UserEnrollForm(request.POST,request.FILES);
			if user_enroll_form.is_valid():
				user_enroll_form.save()
				submit_status=True
	if not user_enroll_form:
		user_enroll_form=UserEnrollForm()
	if not login_form:
		login_form=LoginForm()
	friends=get_by_bday()
	return render(request,'home/index.html',{'sidebar_msg':sidebar_msg,'submit_status':submit_status,'is_index':True,'form':user_enroll_form,'friends':friends,'login_form':login_form})

def listPosts(request,username):
	#user=User.objects.get(username=username)
	friend=Friend.objects.get(user=User.objects.get(username=username))
	if request.method=='POST':
		author=Friend.objects.get(user=request.user)
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
		post_form=PostForm()
	return render(request,'home/list_posts.html',{'friend':friend,'posts':friend.post_set.all(),'login_form':LoginForm(),'post_form':post_form,'comment_form':CommentForm()})
	
