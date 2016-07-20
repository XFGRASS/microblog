'''
1.提供了DoubleIdentifierCleanMixin来组件用于admin的form和用于普通用户交互界面的form
'''
from .models import Bloguser
from common.validators import validate_username

from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

class DoubleIdentifierCleanMixin(object):
	'''提供了三个clean方法，用于验证双账号的填写'''

	def clean_email(self):
		'''这里无值情况主动返回None，是为避免触发Unique验证错误'''
		return self.cleaned_data.get("email") or None

	def clean_mobile_phone(self):
		return self.cleaned_data.get("mobile_phone") or None

	def clean_username(self):
		'''根据username的值来设置email或mobile_phone'''
		username = self.cleaned_data.get('username')
		if username:
			if "@" in username:
				username = self._meta.model._default_manager.normalize_email(username)
				self.instance.email = username
			else:
				self.instance.mobile_phone = username

		return username

	def clean(self):
		'''确保email和mobile_phone不同时为空'''
		cleaned_data = super().clean()
		if self.fields.get('email') and self.fields.get('mobile_phone'):
			if not (cleaned_data["email"] or cleaned_data["mobile_phone"]):
				msg = _("Must be set a correct value or go to set %s")
				self.add_error("email", (msg) % "mobile phone")
				self.add_error("mobile_phone", (msg) % "email")
				raise forms.ValidationError(_("Cannot set email and mobile phone to empty value at the same time"))
		return cleaned_data


class BloguserAdminForm(DoubleIdentifierCleanMixin, forms.ModelForm):
	'''用于在admin的retrieve和update'''
	class Meta:
		model = Bloguser
		exclude = ('is_superuser', 'is_admin')

class BloguserCreationAdminForm(DoubleIdentifierCleanMixin, auth_forms.UserCreationForm):
	'''用于在admin设置密码创建新用户'''
	class Meta:
		model = Bloguser
		exclude = ("is_superuser", 'is_admin', 'password', 'last_login')


class BloguserCreationForm(DoubleIdentifierCleanMixin, auth_forms.UserCreationForm):
	'''用于普通用户交互界面注册账号创建新用户'''
	class Meta:
		model = Bloguser
		fields = ()

	username = forms.CharField(label=_('Username'), 
		max_length=254, 
		validators=[validate_username], 
		help_text=_("email or mobile phone"))

	def save(self, commit=True):
		bloguser_obj = super(BloguserCreationForm, self).save(commit=False)
		# account 必须已保存, 否则bloguser无法获取到account_id属性
		if commit:
			bloguser_obj.save()
		return bloguser_obj
 

