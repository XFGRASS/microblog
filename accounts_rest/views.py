from accounts.models import Bloguser
from .serializers import BloguserSerializer, BloguserSimpleSerializer

from rest_framework import generics


class BloguserDetail(generics.RetrieveUpdateAPIView):
	serializer_class = BloguserSerializer
	queryset = Bloguser.objects.all()

class BloguserList(generics.ListAPIView):
	serializer_class = BloguserSimpleSerializer
	queryset = Bloguser.objects.all()

