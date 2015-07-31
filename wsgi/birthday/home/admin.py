from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
 
admin.site.unregister(User)

class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','username', 'email', 'password1', 'password2')}
        ),
    )

class FriendAdmin(admin.ModelAdmin):
	list_display = ('user','date_of_birth','quote','image_tag','header_image_tag')
	fields = ['user','date_of_birth','quote','image','header_image']

class PostAdmin(admin.ModelAdmin):
	list_display = ('image', 'caption','friend','author')
	fields = ['image', 'caption','friend','author']

class CommentAdmin(admin.ModelAdmin):
	list_display = ('comment', 'post','author')
	fields = ['comment', 'post','author']

class UserEnrollAdmin(admin.ModelAdmin):
	list_display=('first_name','last_name','email','username','password','date_of_birth','image_tag',)
	fields = ['first_name','last_name','email','username','password','date_of_birth','image']


admin.site.register(User, MyUserAdmin)
admin.site.register(Friend,FriendAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(UserEnroll,UserEnrollAdmin)
