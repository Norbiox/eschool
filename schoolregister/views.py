# -*- coding: utf-8 -*-
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, RedirectView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url

from .models import *
from .decorators import *


@method_decorator(student_or_teacher_required, name='dispatch')
class GradeView(DetailView):
    model = Grade
    template_name = 'schoolregister/grade_detail.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class GroupsList(ListView):
    template_name = 'schoolregister/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.order_by('-year')[::-1]


@method_decorator(student_or_teacher_required, name='dispatch')
class GroupsView(DetailView):
    model = Group
    template_name = 'schoolregister/groups_html'


@method_decorator(student_or_teacher_required, name='dispatch')
class IndexView(View):
    template_name = 'schoolregister/index.html'

    def get(self, request):
        context = { 'welcome': "Yo mon! You're in school register index!"}
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name='dispatch')
class StudentView(DetailView):
    model = Student
    template_name = 'schoolregister/student_details.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class TeacherView(DetailView):
    model = Teacher
    template_name = 'schoolregister/teacher_details.html'


class UnactiveUserView(View):
    pass
