from .models import User
from common.validators import validate_username
from accounts.forms import BloguserCreationForm

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _

__all__ = [
	'BloguserCreationForm',
]
class UserAdminForm(forms.ModelForm):
	class Meta:
		model = User
		exclude = ("mobile_phone", )

	def __init__(self, *args, **kwargs):
		super(UserAdminForm, self).__init__(*args, **kwargs)
		self.fields["email"].required = True

class UserLoginForm(auth_forms.AuthenticationForm):

	username = forms.CharField(label=_('Username'), 
		max_length=254, 
		validators=[validate_username], 
		help_text=_("email or mobile phone"))
	
	def get_bloguser(self):
		user_id = super(UserLoginForm, self).get_user_id()
		if user_id:
			from bloguser.models import Bloguser
			try:
				return Bloguser.objects.get(id=user_id)
			except Bloguser.DoesNotExsit:
				return None
		return None