'''
1.follow处理未保存对象的机制，目前仅限于处理follow自己
'''

from cus_auth.models import User
from common.choices import SEX_CHOICE
from blogs.models import Comment, LikeRecord, ForwardRecord, Blog

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core import validators
from django.utils.functional import cached_property


class Bloguser(User):

	class Meta(User.Meta):	
		proxy = True
		verbose_name = _("bloguser")
		verbose_name_plural = _("blogusers")

	'''interactive with bloguser'''

	def save(self, *args, **kwargs):
		'''这里处理了未保存的relation of follow'''
		self.follow(self)
		super(Bloguser, self).save(*args, **kwargs)
		if hasattr(self, 'unsaved_relation'):
			# 重新加载对象的pk到relation实例中
			self.unsaved_relation.follower = self
			self.unsaved_relation.follow = self
			self.unsaved_relation.save()

	@cached_property
	def user(self):
		try:
			return User.objects.get(pk=self.pk)
		except User.DoesNotExist:
			return Non

	def follow(self, target):
		'''若follow对象或follower对象未存在DB中则在双方保存后存储relation of follow'''
		if target.is_authenticated():
			relation = FollowRelation(follower=self, follow=target)
			# pre-follow
			if self.pk and target.pk:
				relation.save()
			else:
				self.unsaved_relation = relation

	def unfollow(self, target):
		try:
			relation = FollowRelation.objects.get(follower=self, follow=target)
		except FollowRelation.DoesNotExist:
			return
		else:
			relation.delete()

	def get_followers(self, order_by=None, self_included=False):
		records = self.follower_records.select_related("follower")
		if order_by:
			records.order_by(order_by)
		followers = []
		if not self_included:
			records.exclude(follower=self)
		for record in records:
			followers.append(record.follower)
		return followers

	# cached_followers = cached_property(get_followers, name="cached_followers")

	def get_following(self, order_by=None, self_included=False):
		records = self.follow_records.select_related('follow')
		if order_by:
			records.order_by(order_by)
		following = []
		if not self_included:
			records.exclude(follow=self)
		for record in records:
			following.append(record.follow)
		return following

	# cached_following = cached_property(get_following, name="cached_following")

	def blog_feeds(self, self_included=True):
		'''返回当前所有关注的用户的微博'''
		'''测试环境下返回所有的微博'''
		if settings.DEBUG:
			return Blog.objects.all().select_related("user", 
				"source_blog", 
				"source_blog__user")
		blogs = Blog.objects.filter(user__in=self.following.all())
		if not self_included:
			blogs = blogs.exclude(user=self)
		return blogs.select_related('user', 'source_blog', 'source_blog__user')
	
	# cached_blogs = cached_property(get_blogs, name="cached_blogs")

	'''interactive with microblog'''
	
	def like(self, blog, else_unlike=False):
		try:
			self.like_record.get(blog=blog)
		except LikeRecord.DoesNotExist:
			self.like_record.create(blog=blog)
		else:
			if else_unlike:
				self.unlike(blog)

	def unlike(self, blog, else_like=False):
		try:
			like_record = LikeRecord.objects.get(user=self, blog=blog)
		except LikeRecord.DoesNotExist:
			if else_like:
				self.like(blog)
		else:
			like_record.delete()

	@cached_property
	def received_comments(self):
		'''返回所有已发表的微博接收到的评论'''
		return Comment.objects.filter(Q(blog__in=self.blogs.all()) | 
			# 评论的评论（回复）
			Q(parent_comment__in=self.commented.all())
			).select_related('blog', 
			'commenter', 
			'parent_comment')

	@cached_property
	def commented_records(self):
		'''返回所有评论过的微博的评论'''
		return self.commented.select_related('blog', 
			'parent_comment',
			 'blog__user')

	@cached_property
	def got_likes_records(self):
		'''返回所有已发表的微博的被点赞记录'''
		return LikeRecord.objects.filter(blog__in=self.blogs.all()).select_related('blog', 'user')

	@cached_property
	def liked_records(self):
		'''返回所有点赞的记录'''
		return self.liked.select_related('blog', 'blog__user')

	@cached_property
	def got_forwards(self):
		'''返回所有转发微博的记录'''
		blogs = self.blogs.all()
		return ForwardRecord.objects.filter(Q(source_blog__in=blogs) | 
			Q(from_blog__in=blogs)
			).select_related('forwarder', 
			"from_blog",
			'source_blog', 
			'forwarded_blog')

	@cached_property
	def forwarded_record(self):
		blogs = self.blogs.filter(is_forwarded=True)
		return ForwardRecord.objects.filter(forwarded_blog__in=blogs).select_related(
				"forwarder",
				"from_blog",
				"source_blog",
				"forwarded_blog",
			)

class FollowRelation(models.Model):
	'''
	follower: 关注者（粉丝）
	follow: 被关注者
	'''

	class Meta:
		verbose_name = _("Relationship of follow")

	follower = models.ForeignKey(settings.AUTH_USER_MODEL,
		related_name="follow_records", 
		verbose_name=_('follower'))

	follow = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name="follower_records",
		verbose_name=_('follow'))

	date_followed = models.DateTimeField(_('date followed'), 
		default=timezone.now)

	def __str__(self):
		return "id: %d | follower: %s | follow: %s" % (self.id, 
			self.follower.nickname, self.follow.nickname)

class BasicProfile(models.Model):
	class Meta:
		verbose_name = _("basic profile of bloguser")
		
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="basic_profile")
	realname = models.CharField(_("realname"), 
		max_length=30, 
		blank=True,
		validators=[
			validators.RegexValidator(r'^[\w\u4e00-\u9fa5]+$', 
				_("Please enter a real name"),
				code="invalid_realname")
		])
	sex = models.CharField(_("sex"), max_length=10, 
		choices=SEX_CHOICE,
		blank=True) 
	bio = models.CharField(_("bio"), max_length=60, 
		help_text=_("Biography"),
		blank=True)

	def __str__(self):
		return "id: %s | user: %s" % (self.id, self.user.nickname)