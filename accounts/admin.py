from .forms import BloguserAdminForm, BloguserCreationAdminForm
from .models import Bloguser, FollowRelation

from django.contrib import admin

@admin.register(Bloguser)
class BloguserAdmin(admin.ModelAdmin):
	'''
	额外添加add_form, 用于设置密码创建用户
	'''
	list_display = ("pk", "email", 
		"mobile_phone", "date_joined", 
		"is_active", 'followers_count', 
		"following_count")
	list_display_links = ("pk", "email", 
		"mobile_phone")
	readonly_fields = ('password', )

	form = BloguserAdminForm
	add_form = BloguserCreationAdminForm

	# def get_readonly_fields(self, request, obj=None):
	# 	if not obj:
	# 		return ["password", 'last_login']

	def followers_count(self, obj):
		return obj.followers.exclude(pk=obj.pk).count()

	def following_count(self, obj):
		return obj.following.exclude(pk=obj.pk).count() 

	def get_form(self, request, obj=None, **kwargs):
		defaults = {}
		if obj is None:
			defaults['form'] = self.add_form
			defaults['exclude'] = self.add_form._meta.exclude
		defaults.update(kwargs)
		return super(BloguserAdmin, self).get_form(request, obj, **defaults)

	def get_queryset(self, request):
		return super(BloguserAdmin,self).get_queryset(request).exclude(is_admin=True)
			
admin.site.register(FollowRelation)