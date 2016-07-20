from django.contrib.auth import get_user_model

User = get_user_model()

class DoubleIdentifierBackend(object):

	def authenticate(self, username, password=None):
		identifier = username
		user_query = {}
		if "@" in identifier:
			user_query["email"] = identifier
		else:
			user_query["mobile_phone"] = identifier

		try:
			user = User.objects.get(**user_query)
			if user.check_password(password):
				return user
		except User.DoseNotExist:
			return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoseNotExist:
			return None

