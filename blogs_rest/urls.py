from .views import ( BlogDetail, BlogFeeds, BlogList, 
	LikeRecordDetail, LikeRecordList, ForwardRecordDetail,
	ForwardRecordList )

from django.conf.urls import url

urlpatterns = [
	url(r'blog-detail/(?P<pk>\d+)/$', BlogDetail.as_view(), name="blog-detail"),
	url(r'blog-list/(?P<pk>\d+)/$', BlogList.as_view(), name="blog-list"),
	url(r'blog-feeds/(?P<pk>\d+)/$', BlogFeeds.as_view(), name="blog-feeds"),

	url(r'blog-like/(?P<pk>\d+)/$', LikeRecordDetail.as_view(), name="blog_like-detail"),
	url(r'blog-likes/(?P<pk>\d+)/$', LikeRecordList.as_view(), name="blog_like-list"),

	url(r'blog-forward/(?P<pk>\d+)/$', ForwardRecordDetail.as_view(), name="blog_forward-detail"),
	url(r'blog-forwards/(?P<pk>\d+)/$', ForwardRecordList.as_view(), name="blog_forward-list"),
] 