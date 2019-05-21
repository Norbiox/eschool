# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import User


class ContactView(View):
    template_name = 'home/contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class IndexView(View):
    template_name = 'home/index.html'

    def get(self, request):
        context = {'welcome': "Yo mon! You're at our school homepage!"}
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'home/profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        if user.is_teacher:
            return HttpResponseRedirect(reverse(
                'schoolregister:teacher_details',
                kwargs={'teacher_pk': user.teacher.id}
            ))
        if user.is_student:
            return HttpResponseRedirect(reverse(
                'schoolregister:student_details',
                kwargs={'student_pk': user.student.id}
            ))
        viewer = request.user
        context = {
            'user': user,
            'viewer': viewer
        }
        return render(request, self.template_name, context)
