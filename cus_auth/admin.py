from django.contrib import admin
from .models import User
from .forms import UserAdminForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("pk", "email", 
		"is_active", "is_admin", 
		"is_superuser")
	list_display_links = ("pk", "email")
	readonly_fields = ('is_superuser', 'is_admin', "password")

	form = UserAdminForm

	def get_queryset(self, request):
		qs = super(UserAdmin, self).get_queryset(request)
		return qs.filter(is_admin=True)
				
