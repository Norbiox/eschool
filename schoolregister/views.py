# -*- coding: utf-8 -*-
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve, reverse
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


class GradeView(DetailView):
    model = Grade
    template_name = 'schoolregister/grade_details.html'


class GroupsList(ListView):
    template_name = 'schoolregister/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.order_by('-year')[::-1]


class GroupsView(DetailView):
    model = Group
    template_name = 'schoolregister/group_details.html'


class IndexView(View):
    template_name = 'schoolregister/index.html'

    def get(self, request):
        context = { 'welcome': "Yo mon! You're in school register index!"}
        return render(request, self.template_name, context)


class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/school'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'schoolregister/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = '/school'
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/school'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class StudentView(DetailView):
    model = Student
    template_name = 'schoolregister/student_details.html'


class TeacherView(DetailView):
    model = Teacher
    template_name = 'schoolregister/teacher_details.html'


class UnactiveUserView(View):
    pass
