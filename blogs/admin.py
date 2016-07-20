from .models import (Blog, BlogImage, Comment, 
	ForwardRecord, LikeRecord)
from django.contrib import admin

class CommentInline(admin.StackedInline):
	model = Comment
	extra = 0
	
class ImageInline(admin.StackedInline):
	model = BlogImage
	extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ['pk', 
		'user', 
		'is_forwarded',
		'comments_count',
		'forwarded_count',
		'liked_count',
	]
	readonly_fields = ["is_forwarded"]
	list_display_links = ['pk']

	inlines = [
		CommentInline,
		ImageInline, 
	]

# admin.site.register(Blog)
admin.site.register(BlogImage)
admin.site.register(Comment)
admin.site.register(ForwardRecord)
admin.site.register(LikeRecord)
