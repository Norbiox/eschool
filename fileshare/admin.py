from django.contrib import admin
from .models import *


class FileAdmin(admin.ModelAdmin):
    list_display = ('file','owner','uploaded_at')
    list_filter = ('owner',)

admin.site.register(File, FileAdmin)


class ShareAdmin(admin.ModelAdmin):
    list_display = ('owner','file','shared_to','shared_at')
    list_filter = ('shared_to',)

admin.site.register(Share, ShareAdmin)
