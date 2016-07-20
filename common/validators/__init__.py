from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.exceptions import ValidationError

validate_mobile_phone = validators.RegexValidator(r'^[0-9]{11}$',
				_("Enter a real mobile phone number."), 
				code='invalid_mobile_phone')

class UsernameValidator(object):
	def __init__(self, message=None):
		self.message = message or _('Please enter the correct email or mobile phone.')

	def __call__(self, value):
		try:
			try:
				validators.validate_email(value)
			except ValidationError:
				validate_mobile_phone(value)
		except ValidationError:
			raise ValidationError(self.message, code="invalid_username")

validate_username = UsernameValidator()
