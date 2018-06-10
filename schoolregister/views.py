# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse
from django.views import View, generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils import timezone
from django.utils.http import is_safe_url

from .models import *
from .decorators import *
from .forms import *

logger = logging.getLogger(__name__)

@method_decorator(teacher_required, name='dispatch')
class GiveGradeView(View):
    template_name = 'schoolregister/give_grade.html'
    form_class = GiveGrade

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs['pk'])
        context = { 'form':self.form_class(),
                    'student': student }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            pass


@method_decorator(student_or_teacher_required, name='dispatch')
class GradeView(generic.DetailView):
    model = Grade
    template_name = 'schoolregister/grade_details.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class GradesView(View):
    template_name = 'schoolregister/student_grades.html'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=kwargs['pk'])
        if not request.user.is_teacher:
            if request.user.student != student:
                return HttpResponseForbidden("Forbidden.")
        context = {'student':student}
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name='dispatch')
class GroupsList(View):
    template_name = 'schoolregister/groups.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            teacher = request.user.teacher
            context = { 'myclass': None,
                        'teaching_in_classes': [],
                        'other_classes': []
                    }
            for group in Group.objects.all():
                is_teaching_in = bool(list(filter(
                    lambda s: s.teacher == teacher,
                    group.taught_set.all()
                )))
                if group.supervisor == teacher:
                    context['myclass'] = group
                elif is_teaching_in:
                    context['teaching_in_classes'].append(group)
                else:
                    context['other_classes'].append(group)
        else:
            student = request.user.student
            context = { 'myclass': None, 'other_classes': []}
            for group in Group.objects.all():
                if group == student.group:
                    context['myclass'] = group
                else:
                    context['other_classes'].append(group)
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name='dispatch')
class GroupView(View):
    template_name = 'schoolregister/group_details.html'

    def get(self, request, *args, **kwargs):
        group_abbrev = kwargs['abbrev']
        group = Group.objects.all().filter(year=int(group_abbrev[0])).filter(letter=group_abbrev[1])[0]
        if not group:
            raise Http404
        if group:
            context = {'group':group}
            context['students'] = group.student_set.all()
            context['taughts'] = group.taught_set.all()
            return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name='dispatch')
class IndexView(View):
    template_name = 'schoolregister/index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user':user})


@method_decorator(teacher_required, name='dispatch')
class LessonPortalView(View):
    template_name = 'schoolregister/lesson_portal.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            teacher = request.user.teacher
            context = { 'teacher':teacher,
                        'active_lesson':teacher.active_lesson(),
                        'taughts':teacher.taught_set.all() }
        else:
            student = request.user.student
            context = { 'student':student,
                        'active_lesson':student.active_lesson() }
        print(context['active_lesson'])
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name='dispatch')
class LessonView(View):
    template_name = 'schoolregister/lesson_details.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['lesson'] = get_object_or_404(Lesson, pk=kwargs['pk'])
        context['presences'] = context['lesson'].presence_set.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['lesson'] = get_object_or_404(Lesson, pk=kwargs['pk'])
        context['presences'] = context['lesson'].presence_set.all()
        logger.info("POST: {}".format(request.POST))
        if request.POST.get("submit"):
            present_student_ids = list(map(int,request.POST.getlist('present')))
            for presence in context['presences']:
                if presence.student.id in present_student_ids:
                    presence.state = True
                else:
                    presence.state = False
                presence.save()
        elif request.POST.get("end_lesson"):
            context['lesson'].end_time = timezone.now()
            context['lesson'].save()
            logger.info("Lesson save with end_time {}".format(context['lesson'].end_time))
        return render(request, self.template_name, context)



@method_decorator(student_or_teacher_required, name='dispatch')
class NoteView(generic.DetailView):
    model = Note
    template_name = 'schoolregister/note_details.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class NotesView(View):
    template_name = 'schoolregister/student_notes.html'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=kwargs['pk'])
        if not request.user.is_teacher:
            if request.user.student != student:
                return HttpResponseForbidden("Forbidden.")
        context = {'student':student}
        context['notes'] = student.note_set.all().order_by('-datetime')



@method_decorator(student_or_teacher_required, name='dispatch')
class StudentView(generic.DetailView):
    model = Student
    template_name = 'schoolregister/student_details.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class TaughtView(generic.DetailView):
    model = Taught
    template_name = 'schoolregister/taught_details.html'


@method_decorator(student_or_teacher_required, name='dispatch')
class TeacherView(generic.DetailView):
    model = Teacher
    template_name = 'schoolregister/teacher_details.html'


class UnactiveUserView(View):
    pass
