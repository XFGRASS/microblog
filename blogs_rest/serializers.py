from blogs.models import ( Blog, LikeRecord, BlogImage, 
	ForwardRecord )

from rest_framework import serializers

# class BlogImageSerializer(serializers.ModelSerializer):
# 	url = serializers.ReadOnlyField(source="image.url")

# 	class Meta:
# 		model = BlogImage
# 		fields = ("url",)

class BlogSimpleSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog-detail")
	user_nickname = serializers.ReadOnlyField(source="user.nickname")
	user = serializers.HyperlinkedRelatedField(view_name="accounts_rest:bloguser-detail", read_only=True)

	class Meta:
		model = Blog
		fields = ("url","pk", "user_nickname", "user")

class BlogSerializer(BlogSimpleSerializer):
	is_forwarded = serializers.ReadOnlyField()
	source_blog = serializers.HyperlinkedRelatedField(view_name='blogs_rest:blog-detail', read_only=True)
	# content_images = BlogImageSerializer(many=True, read_only=True)
	likes = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog_like-list")
	forwards = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog_forward-list")

	class Meta(BlogSimpleSerializer.Meta):
		model = Blog
		fields = BlogSimpleSerializer.Meta.fields + ('content_text', 
			'image_urls', 'is_forwarded', 'source_blog', 'likes', 
			'forwards', 'date_blogged')

class LikeRecordSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog_like-detail")
	user = serializers.HyperlinkedRelatedField(view_name="accounts_rest:bloguser-detail", read_only=True)
	blog = serializers.HyperlinkedRelatedField(view_name="blogs_rest:blog-detail", read_only=True)
	class Meta:
		model = LikeRecord
		fields = ("url", 'user', 'blog', 'date_liked')

class ForwardRecordSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="blogs_rest:blog_forward-detail")
	forwarder = serializers.HyperlinkedRelatedField(view_name="accounts_rest:bloguser-detail", read_only=True)
	from_blog = serializers.HyperlinkedRelatedField(view_name="blogs_rest:blog-detail", read_only=True)
	source_blog = serializers.HyperlinkedRelatedField(view_name="blogs_rest:blog-detail", read_only=True)
	forwarded_blog = serializers.HyperlinkedRelatedField(view_name="blogs_rest:blog-detail", read_only=True)

	class Meta:
		model = ForwardRecord
		fields = ('url', 'forwarder', 'from_blog', 
			'source_blog', 'forwarded_blog', 'date_forwarded')

