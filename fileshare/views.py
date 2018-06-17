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
from .forms import *


@method_decorator(login_required, name='dispatch')
class FileDeleteView(View):

    def post(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        if file.owner == request.user:
            file.delete()
            return HttpResponseRedirect(reverse('home:profile', \
                kwargs={'pk':request.user.id}))
        return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class FileShareView(View):
    template_name = 'home/share_file.html'

    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        context = {
            'file' : file,
            'group_share_form' : ShareWithClassForm(),
            'user_share_form' : ShareWithUserForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        if request.user != file.owner:
            return HttpResponseForbidden()
        if 'user-share-submit' in request.POST:
            form = ShareWithUserForm(request.POST)
            if form.is_valid():
                share = Share()
                share.file = file
                share.shared_to = form.cleaned_data['shared_to']
                share.shared_at = timezone.now()
                share.save()
        elif 'group-share-submit' in request.POST:
            form = ShareWithClassForm(request.POST)
            if form.is_valid():
                group = form.cleaned_data['group']
                for student in group.student_set.all():
                    share = Share()
                    share.file = file
                    share.shared_to = student.user
                    share.shared_at = timezone.now()
                    share.save()
        return HttpResponseRedirect(reverse('home:profile', \
            kwargs={'pk':request.user.id}))
