from .views import ( create_blog, BlogDetail, 
	conversations, BlogFeeds, CommentList, like_action, 
	comment, forward, ForwardList, ReplyComment, 
	BlogList)

from django.conf.urls import url, include

'''Interactive with blog and comment'''

blog_interactive_urls = [
	url(r'like-action/$', like_action, name='like_blog_action'),
	url(r'comment/$', comment, name='comment_blog'),
	url(r'forward/$', forward, name='forward_blog'),
]

comment_interactive_urls = [
	# url(r'like-comment/$', name='like_comment'),
]

interactive_urls = blog_interactive_urls + comment_interactive_urls

'''Detail of blog and comment'''

blog_detail_urls = [
	url(r'^$', BlogDetail.as_view(), name="index"),
	url(r'comments/$', CommentList.as_view(), name='comments'),
	url(r'forwards/$', ForwardList.as_view(), name='forwards'),
]

comment_detail_urls = [
	url(r'reply/$', ReplyComment.as_view(), name='reply_comment'),
	url(r'conversations/$', conversations, name='conversations'),
]

'''All of urls in here'''

urlpatterns =[
	url(r'create/$', create_blog, name="create"),
	url(r'feeds/$', BlogFeeds.as_view(), name="feeds"),
	url(r'interactive/(?P<pk>\d+)/', include(interactive_urls, namespace='interactive')),
	
	url(r'blogs/(?P<pk>\d+)/$', BlogList.as_view(), name="blogs"),
	url(r'blog-detail/(?P<pk>\d+)/', include(blog_detail_urls, namespace='blog_detail')),
	url(r'comment-detail/(?P<pk>\d+)/', include(comment_detail_urls, namespace='comment_detail')),
] 
