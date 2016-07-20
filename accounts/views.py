from .models import Bloguser, FollowRelation
from common.views import UserContextMixin

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import list, base

class QuickBaseView(base.TemplateView, UserContextMixin):
	'''Use in tests'''
	def get(self, request, *args, **kwargs):
		if not request.bloguser.is_authenticated():
			return HttpResponseRedirect("/")
		return super().get(request, *args, **kwargs)

class Home(QuickBaseView):
	template_name = 'accounts/home.html'

###########
# Profile #
###########

class Profile(QuickBaseView):
	template_name = 'accounts/profile.html'
	
	def get(self, *args, **kwargs):
		response = super().get(*args, **kwargs)
		try:
			bloguser = Bloguser.objects.get(pk=kwargs['pk'])
		except Bloguser.DoesNotExist:
			return HttpResponse("The user might not exist")
		else:
			response.context_data['the_user'] = bloguser
		return response

class FollowerList(list.ListView, UserContextMixin):
	template_name = "accounts/follower_list.html"
	context_object_name = "followers"

	def get_queryset(self):
		try:
			self.the_bloguser = Bloguser.objects.get(pk=self.kwargs["pk"])
		except Bloguser.DoesNotExist:
			return HttpResponse("The bloguser is not existing")
		
		return self.the_bloguser.get_followers()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["the_user"] = self.the_bloguser
		return context

class FollowingList(FollowerList):
	template_name = "accounts/following_list.html"
	context_object_name = "following"

	def get_queryset(self):
		try:
			self.the_bloguser = Bloguser.objects.get(pk=self.kwargs["pk"])
		except Bloguser.DoesNotExist:
			return HttpResponse("The bloguser is not existing")
		
		return self.the_bloguser.get_following()

###############
# Interactive #
###############

def profile_settings(request):
	if not request.bloguser.is_authenticated():
		return HttpResponse("Not login")
	return HttpResponse("%s's profile settings page" % request.bloguser.nickname)
 

def follow_action(request, pk):
	'''Follow or unfollow'''
	try:
		target = Bloguser.objects.get(pk=pk)
	except Bloguser.DoesNotExist:
		return HttpResponse("The bloguser is not existing")
	follower = request.bloguser
	# 无法主动取关自己或关注自己
	if target.pk == follower.pk:
		return HttpResponse("不能取关或关注自己")
	context = {
		"user": request.bloguser,
		"target": target,
	}
	try:
		follow_relation = FollowRelation.objects.get(follow=target, follower=follower)
	except FollowRelation.DoesNotExist:
		# 未关注则关注
		follower.follow(target)
		template_name = "accounts/follow_done.html"
	else:
		# 已关注则取关
		follow_relation.delete()
		template_name = "accounts/unfollow_done.html"
	return render(request, template_name, context)

#################
# Notifications #
#################

class Notifications(QuickBaseView):
	template_name = 'accounts/notifications.html'

def received_comments(request):
	if not request.bloguser.is_authenticated():
		return HttpResponse("Not login")
	context = {
		'user': request.bloguser, 
		'comments': request.bloguser.received_comments,
	}
	return render(request, 
		template_name='accounts/notification_comments.html', 
		context=context)

def commented_records(request):
	if not request.bloguser.is_authenticated():
		return HttpResponse("Not login")
	context = {
		'user': request.bloguser, 
		'comments': request.bloguser.commented_records,
	}
	return render(request, 
		template_name='accounts/notification_comments.html', 
		context=context)

def got_likes(request):
	if not request.bloguser.is_authenticated():
		return HttpResponse("Not login")
	context = {
		'user': request.bloguser, 
		'like_records': request.bloguser.got_likes_records,
	}
	return render(request, 
		template_name='accounts/notification_likes.html', 
		context=context)

def liked_records(request):
	if not request.bloguser.is_authenticated():
		return HttpResponse("Not login")
	context = {
		'user': request.bloguser,
		'like_records': request.bloguser.liked_records,
	}
	return render(request, 
		template_name='accounts/notification_likes.html', 
		context=context)

def got_forwards(request):
	context = {
		'user': request.bloguser,
		'forwards': request.bloguser.got_forwards,
	}
	return render(request, 
		template_name='accounts/notification_forwards.html', 
		context=context)



