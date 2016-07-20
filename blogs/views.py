from .forms import ( BlogCreationForm, CommentForm, 
	ForwardForm)
from .models import ( Blog, BlogImage, Comment, 
	LikeRecord)
from accounts.models import Bloguser

from django.shortcuts import render
from django.views.generic import detail, list, edit
# from django.contrib.auth.decorator import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
# from django.views.decorator.http import require_POST

def create_blog(request):
	if request.method == 'POST':
		#处理基本文字内容
		form = BlogCreationForm(data=request.POST)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.user = request.bloguser
			blog.save()
			#处理图片内容
			images = request.FILES.getlist("blog_images")
			for image in images:
				BlogImage.objects.create(blog=blog, image=image)
 
			return HttpResponseRedirect(blog.get_absolute_url())
	else:
		form = BlogCreationForm()
	context = {
		"blog_form": form,
	}
	return render(request, 
		template_name="blogs/blog_edit.html", 
		context=context)

class BlogDetail(detail.DetailView):
	model = Blog
	template_name = "blogs/blog_detail.html"
	context_object_name = 'blog'

	def get_context_data(self, **kwargs):
		context = {
			'user': self.request.bloguser,
		}
		context.update(**kwargs)
		return super().get_context_data(**context)

class BlogList(list.ListView):
	template_name = "blogs/blog_list.html"
	context_object_name = "blogs"

	def get_queryset(self):
		try:
			bloguser = Bloguser.objects.get(pk=self.kwargs["pk"])
		except Bloguser.DoesNotExist:
			return HttpResponseRedirect('The bloguser is not existing')
		return bloguser.blogs.all()

	def get_context_data(self, **kwargs):
		context = {
			'user': self.request.bloguser,
		}
		context.update(**kwargs)
		return super().get_context_data(**context)
	

class BlogFeeds(BlogList):
	def get_queryset(self):
		return self.request.bloguser.blog_feeds()


class CommentList(list.ListView):
	template_name = 'blogs/blog_comments.html'
	context_object_name = 'comments'

	def get_queryset(self):
		self.blog = Blog.objects.get(pk=self.kwargs['pk'])
		return self.blog.all_comments

	def get_context_data(self, **kwargs):
		super_context = super().get_context_data(**kwargs)
		context = {
			'user': self.request.bloguser,
			'blog': self.blog,
		}
		super_context.update(context)
		return super_context

class ForwardList(list.ListView):
	template_name = 'blogs/blog_forwards.html'
	context_object_name = 'forwards'

	def get_queryset(self):
		self.blog = Blog.objects.get(pk=self.kwargs['pk'])
		return self.blog.be_forwarded.select_related(
			'forwarder', 
			'forwarded_blog')

	def get_context_data(self, **kwargs):
		super_context = super().get_context_data(**kwargs)
		context = {
			'user': self.request.bloguser,
			'blog': self.blog,
		}
		super_context.update(context)
		return super_context

def comment(request, pk):
	try:
		blog = Blog.objects.get(pk=pk)
	except Blog.DoesNotExist:
		return HttpResponse("invalid operate")
	if request.method == "POST":
		form = CommentForm(data=request.POST)
		if form.is_valid():
			comment_obj = form.save(commit=False)
			comment_obj.blog = blog
			comment_obj.commenter = request.bloguser
			comment_obj.save()
			return HttpResponseRedirect('/microblogs/blog-detail/%d/comments/' % blog.pk)

	form = CommentForm()
	context = {
		"form":form,
		'blog': blog,
	}
	return render(request, 'blogs/comment_edit.html', context)

class ReplyComment(edit.UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blogs/comment_edit.html'
	context_object_name = 'parent_comment'

	def get_form_kwargs(self):
		'''不显示被评论的内容'''
		kwargs = super().get_form_kwargs()
		kwargs.pop('instance')
		return kwargs

	def form_valid(self, form):
		comment_obj = form.save(commit=False)
		blog = self.object.blog
		comment_obj.blog = blog
		comment_obj.parent_comment = self.object
		comment_obj.commenter = self.request.bloguser
		comment_obj.save()
		return HttpResponseRedirect('/microblogs/blog-detail/%d/' % blog.pk)


def forward(request, pk):
	try:
		source_blog = Blog.objects.get(pk=pk)
	except Blog.DoesNotExist:
		return HttpResponse('invalid operate')
	if request.method == 'POST':
		form = ForwardForm(data=request.POST)
		if form.is_valid():
			blog_obj = form.save(commit=False)
			blog_obj.source_blog = source_blog
			blog_obj.user = request.bloguser
			blog_obj.save()
			return HttpResponseRedirect('/microblogs/feeds/')

	form = ForwardForm()
	context = {
		'form':form,
		'blog': source_blog,
	}
	return render(request, 'blogs/forward_edit.html', context)


def like_action(request, pk):
	try:
		blog = Blog.objects.get(pk=pk)
	except Blog.DoesNotExist:
		return HttpResponse('Invalid operation')
	context = {"blog": blog}	
	try:
		like_record = blog.got_likes.get(user=request.bloguser)
	except LikeRecord.DoesNotExist:
		blog.got_likes.create(user=request.bloguser)
		template_name = "blogs/like_done.html"
	else:
		like_record.delete()
		template_name = "blogs/unlike_done.html"
	return render(request, template_name, context)

def conversations(request, pk):
	if not request.bloguser.is_authenticated():
		return HttpResponse("No login")
	try:
		comment = Comment.objects.get(pk=pk)
	except Comment.DoesNotExist:
		return HttpResponse('Have no this comment')
	else:
		# 此处要将每一个子评论与父评论（即每一个小对话）组成一个list
		# 没有父评论的子评论（即最开始的评论）的父评论设为None
		conversations = []
		var_list = comment.all_parents.copy()
		var_list.insert(0, comment)
		index = 0
		length = len(var_list)
		for comment in var_list:
			index += 1
			child = comment
			if index == length:
				conversations.append((child, None))
			else:
				parent = var_list[index]
				conversations.append((child, parent))
		# 反转顺序，将最开始的评论至于前
		conversations.reverse()
		context = {
			'comment':comment,
			'conversations': conversations,
		}
		return render(request, 
			template_name="blogs/conversations.html", 
			context=context)


