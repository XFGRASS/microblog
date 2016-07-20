from .models import Blog, Comment

from django import forms
from django.utils.translation import ugettext_lazy as _

class BlogCreationForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ('content_text', )
		widgets = {
			"content_text": forms.Textarea(attrs={
					"style":"resize:none;",
					"rows":"4",
					'placeholder': _("Write something to funny"),
				}),
		}

class ForwardForm(BlogCreationForm):
	pass

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content_text', )
		widgets = {
			"content_text": forms.Textarea(attrs={
					"style":"resize:none;",
					"rows":"4",
					'placeholder': _("Write something to funny"),
				}),
		}
