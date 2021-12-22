from .models import ClientProfile, SpecialistProfile
from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin
User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    pass


admin.site.register(ClientProfile)
admin.site.register(SpecialistProfile)
