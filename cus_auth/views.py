from .forms import UserLoginForm, BloguserCreationForm

from django.shortcuts import (render, resolve_url)
from django.contrib.auth import (REDIRECT_FIELD_NAME, 
	authenticate, views as auth_views, login as auth_login, 
	logout as auth_logout)
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url

# by default
#REDIRECT_FIELD_NAME = 'next'

def login(request, redirect_to=None, 
	redirect_field_name=REDIRECT_FIELD_NAME):
	context = {}
	if redirect_to:
		context[redirect_field_name] = resolve_url

	response = auth_views.login(request, 
		template_name="cus_auth/login.html", 
		authentication_form=UserLoginForm, 
		redirect_field_name=redirect_field_name, 
		extra_context=context)
	return response

def logout(request, redirect_to=None):
	auth_logout(request)
	if redirect_to:
		redirect_to = resolve_url(redirect_to)
	else:
		redirect_to = resolve_url(settings.LOGOUT_REDIRECT_URL)
	return HttpResponseRedirect(redirect_to)

def signup(request, redirect_to=None, 
	redirect_field_name=REDIRECT_FIELD_NAME):
	if not redirect_to:
		redirect_to = request.POST.get(redirect_field_name, 
			request.GET.get(redirect_field_name, settings.SIGNUP_REDIRECT_URL))

	if request.method == "POST":
		form = BloguserCreationForm(data=request.POST)
		if form.is_valid():
			bloguser = form.save()
			account_cache = authenticate(username=form.cleaned_data['username'], 
				password=form.cleaned_data['password1'])
			auth_login(request, account_cache)

			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(settings.SIGNUP_REDIRECT_URL)
			return HttpResponseRedirect('/accounts/signup-done/')
	else:
		form = BloguserCreationForm()
	context = {
		'form':form,
		redirect_field_name: redirect_to,
	}
	return TemplateResponse(request, 'cus_auth/signup.html', 
		context=context)


def signup_done(request, redirect_to=None, 
	redirect_field_name=REDIRECT_FIELD_NAME):
	if not redirect_to:
		redirect_to = request.POST.get(redirect_field_name, 
			request.GET.get(redirect_field_name, settings.SIGNUP_REDIRECT_URL))

	context = {
		redirect_field_name: redirect_to
	}
	return TemplateResponse(request, 'cus_auth/signup_done.html', 
		context=context)
