from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_noop as g_np, ugettext_lazy as _
# from django.utils.functional import cached_property
from django.utils import timezone

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, mobile_phone, password, **extra_fields):
		if not email and not mobile_phone:
		    raise ValueError("The given email or mobile phone must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, mobile_phone=mobile_phone, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email=None, mobile_phone=None, password=None, **extra_fields):
	    extra_fields.setdefault('is_admin', False)
	    extra_fields.setdefault('is_superuser', False)
	    return self._create_user(email, mobile_phone, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
	    extra_fields.setdefault('is_admin', True)
	    extra_fields.setdefault('is_superuser', True)

	    if extra_fields.get('is_admin') is not True:
	        raise ValueError('Superuser must have is_admin=True.')
	    if extra_fields.get('is_superuser') is not True:
	        raise ValueError('Superuser must have is_superuser=True.')

	    return self._create_user(email, None, password, **extra_fields)

	def get_default_nickname(self, def_nickname):
		try:
			self.get(nickname=def_nickname)
		except self.model.DoesNotExist:
			return def_nickname
		else:
			lower_alphabet = "abcdefghijklmnopqrsduvwxyz"
			upper_alphabet = lower_alphabet.upper()
			alphabets = lower_alphabet + upper_alphabetp
	
			def random_extra_name():
				word = []
				extra_name = ""
				for i in range(4):
					word.append(random.choices(alphabets))
				extra_name = (''.join(word))
				return extra_name
	
			while self.filter(nickname=def_nickname).count() > 0:
				def_nickname = "%s_%s_%s" % (def_nickname, 
					random_extra_name(), 
					random.randint(0, 1024))
			return def_nickname


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_("email"), 
		unique=True, 
		null=True,
		blank=True)
	mobile_phone = models.CharField(_("mobile phone"), 
		max_length=15,
		unique=True,
		null=True,
		blank=True)
	nickname = models.CharField(_("nickname"), 
		max_length=60,
		unique=True)
	following = models.ManyToManyField('self', symmetrical=False, 
		through='accounts.FollowRelation',
		related_name='followers',
		verbose_name=_('following'))

	is_admin = models.BooleanField(_('admin status'), default=False)   
	is_active = models.BooleanField(_('active'), default=True)
	date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

	USERNAME_FIELD = "email"

	objects = UserManager()

	class Meta:
		verbose_name = _("user")
		verbose_name_plural = _("users")
		permissions = (
			('add_admin', g_np("can add a user of is_admin=True ")),
			('change_admin', g_np('can change a user of is_admin=True')),
			('delete_admin', g_np("can delete a user of is_admin=True")),
		)

	def save(self, *args, **kwargs):
		if not self.email and not self.mobile_phone:
			raise ValueError()
		if not self.nickname:
			self.nickname = self.__class__.objects.get_default_nickname(self.email or self.mobile_phone)
		super(User, self).save(*args, **kwargs)

	def get_username(self):
		return self.email or self.mobile_phone

	def get_full_name(self):
		return self.email or self.mobile_phone

	def get_short_name(self):
		return self.mobile_phone or self.email

	def is_authentication(self):
		return self.is_active

	@property
	def is_staff(self):
		return self.is_admin


