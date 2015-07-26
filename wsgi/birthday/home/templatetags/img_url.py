from django import template

register = template.Library()


@register.filter
def get_image_url(value):
	tmp=value.url.split("/")
	return '/static/'+"/".join(tmp[-3:])
	
