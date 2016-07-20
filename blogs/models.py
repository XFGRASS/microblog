from django.db import models
from django.db.models import F
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

class ForwardRecord(models.Model):
	class Meta:
		ordering = ['-date_forwarded']
		
	forwarder = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name='forwarded', 
		verbose_name=_('forwarder'))
	from_blog = models.ForeignKey('Blog', 
		models.SET_NULL, 
		null=True, 
		related_name = 'be_forwarded',
		verbose_name=_("forwarded from (blog)"))
	source_blog = models.ForeignKey('Blog', 
		models.SET_NULL, 
		null=True, 
		related_name = 'be_forwarded_all',
		verbose_name=_("source blog"))
	forwarded_blog = models.OneToOneField('Blog',
		related_name='source_relation', 
		verbose_name=_('forwarded blog'))
	date_forwarded = models.DateTimeField(_('date forwarded'), default=timezone.now)

	def __str__(self):
		# return "pk: %d | from: %s | get: %s | to: %s" % (self.pk,
		# 	# self.from_blog.user.nickname, 
		# 	# self.source_blog.user.nickname, 
		# 	self.forwarded_blog.user.nickname)
		return "pk: %d | to: %s" % (self.pk,
			# self.from_blog.user.nickname, 
			# self.source_blog.user.nickname, 
			self.forwarded_blog.user.nickname)

class LikeRecord(models.Model):
	class Meta:
		ordering = ['-date_liked']
		
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		models.SET_NULL,
		null=True, 
		related_name="liked",
		verbose_name=_("like by (user)"))
	blog = models.ForeignKey('Blog', 
		models.SET_NULL, 
		null=True, 
		related_name = 'got_likes',
		verbose_name=_("blog"))

	date_liked = models.DateTimeField(_('date liked'), default=timezone.now)

	def __str__(self):
		return 'pk: %d | user: %s | blog: < %s >' % (self.pk, 
			self.user.nickname, 
			self.blog)

	def save(self, *args, **kwargs):
		super(LikeRecord, self).save(*args, **kwargs)
		if not (self.user or self.blog):
			self.delete()


class Blog(models.Model):
	class Meta:
		verbose_name = _("microblog")
		verbose_name_plural = _("microblogs")
		ordering = ["-date_blogged"]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
		related_name="blogs",
		verbose_name=_("blogger"))
	source_blog = models.ForeignKey('self', 
		models.SET_NULL, 
		null=True, 
		blank=True,
		default=None,
		related_name="child_blogs", 
		verbose_name=_('source blog'))
	is_forwarded = models.BooleanField(_('is forwarded blog'), default=False)
	content_text = models.CharField(_("content text"), max_length=200)
	date_blogged = models.DateTimeField(_("date blogged"), default=timezone.now)
	last_modified = models.DateTimeField(_("last modified"), auto_now=True)

	def __str__(self):
		return 'pk: %s | user: %s | text: %s' % (self.pk, self.user.nickname, self.content_text)

	def save(self, *args, **kwargs):
		if self.source_blog:
			if self.pk:
				#将已存在的微博修改（admin site中）为转发的微博，
				#并且source blog指向自己的话，将会创建一个新的blog
				#同样，已存在的“转发的微博”修改source blog指向其他blog时，将会重写创建一个新的blog
				if self.pk == self.source_blog.pk or (
					self.source_blog != self.__class__._default_manager.get(pk=self.pk).source_blog
					):
					self.__class__._default_manager.create(user=self.user,
						source_blog=self, 
						content_text=self.content_text)
					return
			else:
				# 始终指向“原微博”
				if self.source_blog.is_forwarded:
					self._from_blog = self.source_blog
					self.source_blog = self.source_blog.source_blog
				#设置为“转发微博”的同时，创建 ForwardRecord 作为转发记录
				self._forwarded_record_obj = ForwardRecord(
					forwarder=self.user,
					#保留“直接转发处”的微博信息 from_blog
					from_blog=getattr(self, "_from_blog", self.source_blog),
					source_blog=self.source_blog)
			# 自动设置is_forwarded	
			if not self.is_forwarded:
				self.is_forwarded = True
		super(Blog, self).save(*args, **kwargs)
		if hasattr(self, "_forwarded_record_obj"):
				self._forwarded_record_obj.forwarded_blog = self
				self._forwarded_record_obj.save()

	def get_absolute_url(self):
		return '/microblogs/blog-detail/%d/' % self.id

	def get_image_urls(self):
		if self.content_images.count() > 0:
			image_urls = []
			for image in self.content_images.all():
				image_urls.append(image.image.url)
			return image_urls

	image_urls = cached_property(get_image_urls, name="image_urls")

	def forwarded_count(self):
		if self.is_forwarded:
			return self.child_blogs.count()
		else:
			return self.be_forwarded.count()

	def liked_count(self):
		return self.got_likes.count()

	def comments_count(self):
		return self.comments.count()

	@cached_property
	def all_comments(self):
		return self.comments.select_related('commenter', 
			'parent_comment', 
			'parent_comment__commenter')

	@cached_property
	def liked_users(self):
		got_likes = self.got_likes.select_related('user')
		liked_users = []
		for got_like in got_likes:
			liked_users.append(got_like.user)
		return liked_users

def get_image_path(instance, filename):
	return 'blog_images/user_%s/blog_%s/%s' % (instance.blog.user.id, instance.blog.id, filename)

class BlogImage(models.Model):
	blog = models.ForeignKey(Blog, related_name="content_images", verbose_name=_("blog"))
	image = models.ImageField(_("content image"), upload_to=get_image_path)

class Comment(models.Model):
	class Meta:
		ordering = ['-date_commented']
		verbose_name = _("comment")
		verbose_name_plural = _('comments')

	blog = models.ForeignKey(Blog,
		models.SET_NULL,
		null=True,
		related_name="comments", 
		verbose_name=_("blog"))
	commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
		related_name='commented',
		verbose_name=_("commenter"))
	content_text = models.CharField(_('content_text'), max_length=200)
	# 评论别人的评论
	parent_comment = models.ForeignKey('self', 
		models.SET_NULL,
		null=True,
		blank=True,
		default=None,
		related_name="child_comments", 
		verbose_name=_('parent comment'))
	date_commented = models.DateTimeField(_("date commented"), default=timezone.now)

	def __str__(self):
		return "pk: %d  | commenter: %s | blog: < %s > | content: < %s >" % (self.pk, 
			self.commenter.nickname, 
			self.blog,
			self.content_text,
		)

	# def get_all_parents(self, parent=None):
	# 	if not parent and not hasattr(self, 'all_parents'):
	# 		parent = self.parent_comment
	# 	if not hasattr(self, 'all_parents'):
	# 		self.all_parents = []
	# 	if parent:
	# 		self.all_parents.append(parent)
	# 		if parent.parent_comment:
	# 			self.get_all_parents(parent.parent_comment)
	# 	return self.all_parents

	@cached_property
	def all_parents(self):
		all_parents = []
		parent = self.parent_comment
		while parent:
			all_parents.append(parent)
			parent = parent.parent_comment
		return all_parents

