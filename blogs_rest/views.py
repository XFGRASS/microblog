from blogs.models import ( Blog, LikeRecord, 
	ForwardRecord )
from accounts.models import Bloguser
from .permissions import IsOwnerOrReadOnly
from .serializers import ( BlogSerializer, BlogSimpleSerializer, 

	LikeRecordSerializer, ForwardRecordSerializer )
from rest_framework import generics, permissions

# Blog
class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Blog.objects.all()
	serializer_class = BlogSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
		IsOwnerOrReadOnly)

class BlogList(generics.ListCreateAPIView):
	serializer_class = BlogSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
		IsOwnerOrReadOnly)

	def get_queryset(self):
		bloguser = Bloguser.objects.get(pk=self.kwargs["pk"])
		return bloguser.blogs.all()

class BlogFeeds(generics.ListAPIView):

	serializer_class = BlogSerializer

	def get_queryset(self):
		bloguser = self.request.bloguser
		return bloguser.blog_feeds()

# Like

class LikeRecordDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = LikeRecord.objects.all()
	serializer_class = LikeRecordSerializer

class LikeRecordList(generics.ListAPIView):
	serializer_class = LikeRecordSerializer

	def get_queryset(self):
		blog = Blog.objects.get(pk=self.kwargs["pk"])
		return blog.got_likes.all()

# Forward

class ForwardRecordDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = ForwardRecord.objects.all()
	serializer_class = ForwardRecordSerializer


class ForwardRecordList(generics.ListAPIView):
	queryset = ForwardRecord.objects.all()
	serializer_class = ForwardRecordSerializer
 
	def get_queryset(self):
		blog = Blog.objects.get(pk=self.kwargs["pk"])
		if blog.is_forwarded:
			return blog.be_forwarded.all()
		else:
			return blog.be_forwarded_all.all()
