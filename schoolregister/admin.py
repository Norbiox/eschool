from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from .models import *


admin.site.register([Grade, Lesson, Note, Presence, Rate, Subject, Taught])


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'group', 'email')
    list_filter = ('group',)


class StudentInline(admin.TabularInline):
    model = Student
    extra = 3

admin.site.register(Student, StudentAdmin)


class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ('name', 'supervisor', 'number_of_students')

admin.site.register(Group, GroupAdmin)

"""
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal info',   {'fields': ['first_name', 'last_name', 'title', \
                                        'birth_date']}),
        ('Contact info',    {'fields': ['email', 'address', 'phone']}),
        ('School info',     {'fields': ['specialisation']})
    ]
    list_display = ('full_name', 'email', 'group')
"""

admin.site.register(Teacher)
