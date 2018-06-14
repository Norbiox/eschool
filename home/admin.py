from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import *

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            ("Status", {'fields': ('is_teacher','is_student','is_writer',)}),
    )

admin.site.register(User, MyUserAdmin)


class FileAdmin(admin.ModelAdmin):
    list_display = ('file','owner','uploaded_at')
    list_filter = ('owner',)

admin.site.register(File, FileAdmin)


class ShareAdmin(admin.ModelAdmin):
    list_display = ('owner','file','shared_to','shared_at')
    list_filter = ('shared_to',)

admin.site.register(Share, ShareAdmin)
