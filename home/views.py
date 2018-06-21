# -*- coding: utf-8 -*-
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse
from django.views import View
from django.views import generic, View
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


class ContactView(View):
    template_name = 'home/contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request):
        context = { 'welcome': "Yo mon! You're at our school homepage!"}
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'home/profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        if user.is_teacher:
            return HttpResponseRedirect(reverse(
                'schoolregister:teacher_details', kwargs={'teacher_pk':user.teacher.id}
            ))
        if user.is_student:
            return HttpResponseRedirect(reverse(
                'schoolregister:student_details', kwargs={'student_pk':user.student.id}
            ))
        viewer = request.user
        context = {
            'user' : user,
            'viewer' : viewer
        }
        return render(request, self.template_name, context)
