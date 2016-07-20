from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect

def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/accounts/home/')
	return HttpResponseRedirect('/accounts/login/')

class UserContextMixin(object):
	'''将已登录认证的用户添加到context中'''
	def get_context_data(self, **kwargs):
		context = {
			'user': self.request.bloguser,
		}
		if kwargs:
			context.update(kwargs)
		return super().get_context_data(**context)