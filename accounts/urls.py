from .views import (Home, Profile, profile_settings, 
	received_comments, commented_records, 
	got_likes, liked_records, got_forwards, 
	Notifications, follow_action, FollowerList, 
	FollowingList)
from cus_auth.views import login, signup, logout, signup_done
from django.conf.urls import url, include

'''Authentication'''

authentication_urls = [
	url(r'login/$', login, name='login'),
	url(r'signup/$', signup, name='signup'),
	url(r'logout/$', logout, name='logout'),
	url(r'signup-done/$', signup_done, name="signup_done")
]

profile_urls = [
	url(r'^$', Profile.as_view(), name='index'),
	url(r'followers/$', FollowerList.as_view(), name="followers"),
	url(r'following/$', FollowingList.as_view(), name="following"),
	url(r'settings/$', profile_settings, name='settings'),
]

'''Notifications'''

notifications_received_urls = [
	url(r'got-likes/$', got_likes, name="got_likes"),
	url(r'received-comments/$', received_comments, name='received_comments'),
	url(r'got-forwards/$', got_forwards, name='got_forwards'),
]


notification_dispath_urls = [
	url(r'^$', Notifications.as_view(), name='index'),
	url(r'commented-records/$', commented_records, name='commented_records'),
	url(r'liked-records/$', liked_records, name='liked_records'),
]

notification_urls = notifications_received_urls + notification_dispath_urls


urlpatterns = [
	url(r'home/$', Home.as_view(), name="home"),
	url(r'profile/(?P<pk>\d+)/', include(profile_urls, namespace='profile')),
	url(r'notifications/', include(notification_urls, namespace="notifications")),
	url(r'follow-action/(?P<pk>\d+)/$', follow_action, name="follow_action"),

] + authentication_urls
