# -*- coding: utf-8 -*-

import os
import mimetypes
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.urls import resolve, reverse
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from eschool import settings
from .models import *
from .forms import *


@method_decorator(login_required, name='dispatch')
class FileDeleteView(View):

    def post(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        if file.owner == request.user:
            file.delete()
            if os.path.isfile(file.path()):
                os.remove(file.path())
            return HttpResponseRedirect(reverse('fileshare:index'))
        return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class FileDownloadView(View):

    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        with open(file.path(), 'rb') as f:
            data = f.read()
        response = HttpResponse(data, content_type=mimetypes.guess_type(file.path())[0])
        response['Content-Disposition'] = "attachment; filename={0}".format(file)
        response['Content-Length'] = os.path.getsize(file.path())
        return response


@method_decorator(login_required, name='dispatch')
class FileShareView(View):
    template_name = 'fileshare/share_file.html'

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
        return HttpResponseRedirect(reverse('fileshare:index'))


@method_decorator(login_required, name='dispatch')
class FileShowView(View):

    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, id=kwargs['pk'])
        user = request.user
        if user == file.owner or file.share_set.filter(shared_to=user):
            return HttpResponseRedirect(file.link())
        return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'fileshare/index.html'
    upload_file_form = FileForm

    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'upload_file_form': self.upload_file_form(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST['upload_submit']:
            form = FileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.save(commit=False)
                file.owner = request.user
                file.uploaded_at = timezone.now()
                file.save()
                return HttpResponseRedirect('')
        return HttpResponseRedirect(reverse('fileshare:index'))
