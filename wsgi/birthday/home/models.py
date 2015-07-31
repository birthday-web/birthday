from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from time import strftime
from django.conf import settings
from PIL import Image

def resize_image(image):
	size=(350,350)
	filename=str(image.path)
	new_image = Image.open(filename)
	new_image.thumbnail(size, Image.ANTIALIAS)
	new_image.save(filename)
	
class Friend(models.Model):
	user = models.OneToOneField(User)
	image=models.ImageField(upload_to='friends')
	date_of_birth=models.DateField("Date of Birth")
	header_image=models.ImageField(upload_to='friends/headers',blank=True)
	quote=models.CharField(max_length=500)
	def __str__(self):
		return self.user.first_name+" "+self.user.last_name+"("+self.user.username+")"
	
	@property
	def image_url(self):
		return settings.MEDIA_URL + '/'.join(self.image.url.split("/")[-2:])
	
	@image_url.setter
	def image_url(self, value):
		self.__image_url = value
	
	@property
	def header_image_url(self):
		if self.header_image:
			return settings.MEDIA_URL + '/'.join(self.header_image.url.split("/")[-3:])
		else:
			return ''
	
	@header_image_url.setter
	def header_img_url(self, value):
		self.__header_image_url = value
	
	def image_tag(self):
		return u'<img src="%s" width=150 />' % (self.image_url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True
	
	def header_image_tag(self):
		return u'<img src="%s" width=150 />' % (self.header_image_url)
	header_image_tag.short_description = 'Header Image'
	header_image_tag.allow_tags = True
	
	def save(self,*args, **kwargs):
		super(Friend,self).save()
		resize_image(self.image)
	
class Post(models.Model):
	image=models.ImageField(upload_to='posts')
	caption=models.CharField(max_length=500)
	friend=models.ForeignKey(Friend)
	author=models.ForeignKey(Friend, related_name="author")
	def __str__(self):
		return "("+str(self.image)+")"+self.caption
	def save(self,*args, **kwargs):
		super(Post,self).save()
		resize_image(self.image)
	@property
	def get_image_url(self):
		return settings.MEDIA_URL + '/'.join(self.image.url.split("/")[-2:])
	
	@get_image_url.setter
	def get_image_url(self, value):
		self.__get_image_url = value
	
	def image_tag(self):
		return u'<img src="%s" width=150 />' % (self.get_image_url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True

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
	image=models.ImageField(upload_to='enrolls')
	def __str__(self):
		return self.first_name+" "+self.last_name+"("+self.username+")"
	@property
	def get_image_url(self):
		return settings.MEDIA_URL + '/'.join(self.image.url.split("/")[-2:])
	
	@get_image_url.setter
	def get_image_url(self, value):
		self.__get_image_url = value
	
	def image_tag(self):
		return u'<img src="%s" width=150 />' % (self.get_image_url)
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True
	def save(self,*args, **kwargs):
		super(UserEnroll,self).save()
		resize_image(self.image)
