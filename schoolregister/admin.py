from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import *


admin.site.register([Grade, Lesson, Note, Presence, Rate, Subject, Taught])


class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'email')
    list_filter = ('group',)


class StudentInline(admin.TabularInline):
    model = Student
    extra = 3

admin.site.register(Student, StudentAdmin)


class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ('name', 'supervisor', 'number_of_students')

admin.site.register(Group, GroupAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'specialization', 'group')

admin.site.register(Teacher, TeacherAdmin)
