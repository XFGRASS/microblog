from .views import BloguserDetail, BloguserList

from django.conf.urls import url
# from rest_framework import 



urlpatterns = [
	url(r'bloguser-detail/(?P<pk>\d+)/$', BloguserDetail.as_view(), name='bloguser-detail'),
	url(r'bloguser-list/$', BloguserList.as_view(), name="bloguser-list"),
]