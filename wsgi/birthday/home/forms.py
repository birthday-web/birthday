from home.models import Friend,Post,Comment
from django.forms import ModelForm
from django import forms
from home.models import *
from nocaptcha_recaptcha.fields import NoReCaptchaField
from copy import deepcopy

class DateInput(forms.DateInput):
	input_type = 'date'
    
class LoginForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','password']
		widgets={
			'username':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'Username'}),
			'password':forms.PasswordInput(attrs={'class': 'form-control','Placeholder':'Password'}),
		}
		
class UserEnrollForm(forms.ModelForm):
	captcha=NoReCaptchaField(error_messages={'required':'This check is mandatory.'})
	class Meta:
		model= UserEnroll
		fields=['first_name','last_name','email','date_of_birth','username','password','image','captcha']
		widgets={
			'first_name':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'First Name'}),
			'last_name':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'Last Name'}),
			'email':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'Email'}),
			'date_of_birth':forms.DateInput(attrs={'class': 'form-control','type':'date','placeholder':'mm/dd/yyyy'}),
			'username':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'Username'}),
			'password':forms.PasswordInput(attrs={'class': 'form-control','Placeholder':'Password'}),
			'image':forms.FileInput(attrs={'class': 'form-control file-input','type':'file','title':'Your Image'}),
		}
		error_messages = {
            'username': {
                'unique':"This username is already taken.",
            },
            'email':{
				'unique':"This email is already registered."
            },
            'date_of_birth':{
				'required':"Oh common! you must have date of birth."
            },
            'image':{
				'required':"Select your image."
            }
        }
class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=['image','caption']
		widgets={
			'image':forms.FileInput(attrs={'class': 'form-control file-input','type':'file','title':'Post Image'}),
			'caption':forms.Textarea(attrs={'class': 'form-control','required':True,'placeholder':'Caption'}),
			}
			
class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['comment','post']
		widgets={
			'comment':forms.TextInput(attrs={'class': 'form-control','required':True,'placeholder':'Comment'}),
			'post':forms.HiddenInput(),
			}
