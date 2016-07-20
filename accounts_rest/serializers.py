from accounts.models import Bloguser
from blogs.models import Blog

from rest_framework import serializers, viewsets


class BloguserSimpleSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="accounts_rest:bloguser-detail")

	class Meta:
		model = Bloguser
		fields = ('url', "id", 'is_admin', 'nickname')
			
class BloguserSerializer(BloguserSimpleSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="accounts_rest:bloguser-detail")
	is_admin = serializers.ReadOnlyField()
	blogs = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog-list")
	# blogs = serializers.HyperlinkedRelatedField(many=True, view_name="blogs_rest:blog-detail", queryset=Blog.objects.all())
	blog_feeds = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog-feeds")
	# follower = serializers.HyperlinkedRelatedField(many=True, view_name='accounts_rest:bloguser-detail', read_only=True)
	following = serializers.HyperlinkedRelatedField(many=True, view_name="accounts_rest:bloguser-detail", read_only=True)
	followers = serializers.HyperlinkedRelatedField(many=True, view_name="accounts_rest:bloguser-detail", read_only=True)

	class Meta:
		model = Bloguser
		fields = ("url", "id", 'is_admin', "nickname", 
			"email", "mobile_phone", "following", 
			"followers", "blogs", "blog_feeds")






	