from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from time import strftime
from django.conf import settings
from PIL import Image

def get_friend_image_path(instance,filename):
	base=settings.IMAGE_ROOT+'friends/'
	filename=datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f_')+filename
	return base+filename
	

def get_post_image_path(instance,filename):
	base=settings.IMAGE_ROOT+'posts/'
	filename=datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f_')+filename
	return base+filename

def get_enroll_image_path(instance,filename):
	base=settings.IMAGE_ROOT+'enrolls/'
	filename=datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f_')+filename
	return base+filename
	

def resize_image(image):
	size=(350,350)
	filename=str(image.path)
	new_image = Image.open(filename)
	new_image.thumbnail(size, Image.ANTIALIAS)
	new_image.save(filename)
	
class Friend(models.Model):
	user = models.OneToOneField(User)
	image=models.ImageField(upload_to=get_friend_image_path)
	date_of_birth=models.DateField("Date of Birth")
	def __str__(self):
		return self.user.first_name+" "+self.user.last_name+"("+self.user.username+")"
	def get_img_url(self):
		tmp=self.image.url.split("/")
		return 'static/'+"/".join(tmp[-3:])
	def image_tag(self):
		return u'<img src="/%s" width=150 />' % self.get_img_url()
	image_url=property(get_img_url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True
	def save(self,*args, **kwargs):
		super(Friend,self).save()
		resize_image(self.image)
	
class Post(models.Model):
	image=models.ImageField(upload_to=get_post_image_path)
	caption=models.CharField(max_length=500)
	friend=models.ForeignKey(Friend)
	author=models.ForeignKey(Friend, related_name="author")
	def __str__(self):
		return "("+str(self.image)+")"+self.caption
	def save(self,*args, **kwargs):
		super(Post,self).save()
		resize_image(self.image)

class Comment(models.Model):
	comment=models.CharField(max_length=200)
	post=models.ForeignKey(Post)
	author=models.ForeignKey(Friend)
	def __str__(self):
		return self.comment
		

class UserEnroll(models.Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	email=models.EmailField(unique=True)
	username=models.CharField(max_length=50,unique=True)
	password=models.CharField(max_length=50)
	date_of_birth=models.DateField("Date of Birth")
	image=models.ImageField(upload_to=get_enroll_image_path)
	def __str__(self):
		return self.first_name+" "+self.last_name+"("+self.username+")"
	def get_img_url(self):
		tmp=self.image.url.split("/")
		return 'static/'+"/".join(tmp[-3:])
	def image_tag(self):
		return u'<img src="/%s" width=200/>' % self.get_img_url()
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True
	def save(self,*args, **kwargs):
		super(UserEnroll,self).save()
		resize_image(self.image)
