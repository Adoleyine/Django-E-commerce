from django.contrib import admin
from userAuths.models import User, Profile



# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name', 'bio', 'phone', 'email', 'verified']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)