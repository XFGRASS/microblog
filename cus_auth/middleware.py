from accounts.models import Bloguser

from django.contrib.auth.middleware import AuthenticationMiddleware, get_user
from django.utils.functional import SimpleLazyObject

def get_bloguser(request):
	_user = get_user(request)
	try:
		return Bloguser.objects.get(pk=_user.pk)
	except Bloguser.DoesNotExist:
		return _user

class NewAuthenticationMiddleware(AuthenticationMiddleware):

	def process_request(self, request):
		super(NewAuthenticationMiddleware, self).process_request(request)
		request.bloguser = SimpleLazyObject(lambda: get_bloguser(request))