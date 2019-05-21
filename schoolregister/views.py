# -*- coding: utf-8 -*-
import logging

from django.http import (
    HttpResponseRedirect,
    Http404,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import *
from .decorators import *
from .forms import *

logger = logging.getLogger(__name__)


@method_decorator(teacher_required, name="dispatch")
class GiveGroupGradesView(View):
    template_name = "schoolregister/give_group_grades.html"

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, kwargs["abbrev"])
        return render(request, self.template_name, {"group": group})


@method_decorator(student_or_teacher_required, name="dispatch")
class GradeView(View):
    template_name = "schoolregister/grade_details.html"
    header_template = "schoolregister/_student_header.html"
    form_template = "schoolregister/_grade_form.html"
    form_class = GradeForm

    def get(self, request, *args, **kwargs):
        grade = get_object_or_404(Grade, pk=kwargs["grade_pk"])
        return render(request, self.template_name, {"grade": grade})

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        form = self.form_class(request.user, student, request.POST)
        if form.is_valid():
            form.save(request.user, student)
        return HttpResponseRedirect(
            reverse("schoolregister:student_details", kwargs={"student_pk": student.id})
        )


@method_decorator(teacher_required, name="dispatch")
class GradeAddView(GradeView):
    template_name = "schoolregister/form_base.html"
    title = "Add grade"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        context = {
            "title": self.title,
            "student": student,
            "header_template": self.header_template,
            "form_template": self.form_template,
            "grade_form": self.form_class(request.user, student),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        form = self.form_class(request.user, student, request.POST)
        if form.is_valid():
            form.save(request.user, student)
        return HttpResponseRedirect(
            reverse("schoolregister:student_details", kwargs={"student_pk": student.id})
        )


@method_decorator(teacher_required, name="dispatch")
class GradeEditView(GradeView):
    template_name = "schoolregister/form_base.html"
    title = "Edit grade"


@method_decorator(teacher_required, name="dispatch")
class GradeDeleteView(GradeView):
    template_name = "schoolregister/form_base.html"
    title = "Delete grade"


@method_decorator(student_or_teacher_required, name="dispatch")
class GradesView(View):
    template_name = "schoolregister/grades_view.html"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, id=kwargs["student_pk"])
        logger.debug("grades_view, is teacher: {}".format(request.user.is_teacher))
        if request.user.is_student:
            logger.debug(
                "grades_view, is owner: {}".format(request.user.student == student)
            )
        if request.user.is_teacher or request.user.student == student:
            taughts = student.group.taught_set.all()
            grades = {t: student.grade_set.filter(subject=t) for t in taughts}
            context = {"student": student, "grades": grades, "taughts": taughts}
            return render(request, self.template_name, context)
        return HttpResponseForbidden()


@method_decorator(student_or_teacher_required, name="dispatch")
class GroupsList(View):
    template_name = "schoolregister/groups.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            teacher = request.user.teacher
            context = {"myclass": None, "teaching_in_classes": [], "other_classes": []}
            for group in Group.objects.all():
                is_teaching_in = bool(
                    list(filter(lambda s: s.teacher == teacher, group.taught_set.all()))
                )
                if group.supervisor == teacher:
                    context["myclass"] = group
                elif is_teaching_in:
                    context["teaching_in_classes"].append(group)
                else:
                    context["other_classes"].append(group)
        else:
            student = request.user.student
            context = {"myclass": None, "other_classes": []}
            for group in Group.objects.all():
                if group == student.group:
                    context["myclass"] = group
                else:
                    context["other_classes"].append(group)
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name="dispatch")
class GroupView(View):
    template_name = "schoolregister/group_details.html"

    def get(self, request, *args, **kwargs):
        group_abbrev = kwargs["abbrev"]
        group = (
            Group.objects.all()
            .filter(year=int(group_abbrev[0]))
            .filter(letter=group_abbrev[1])[0]
        )
        if not group:
            raise Http404
        if group:
            context = {"group": group}
            context["students"] = group.student_set.all()
            context["taughts"] = group.taught_set.all()
            return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name="dispatch")
class IndexView(View):
    template_name = "schoolregister/index.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {"user": user})


@method_decorator(student_or_teacher_required, name="dispatch")
class LessonPortalView(View):
    template_name = "schoolregister/lesson_portal.html"
    form_class = LessonForm

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            teacher = request.user.teacher
            context = {
                "teacher": teacher,
                "active_lesson": teacher.active_lesson(),
                "taughts": teacher.taught_set.all(),
                "add_lesson_form": self.form_class(request.user),
            }
        else:
            student = request.user.student
            context = {"student": student, "active_lesson": student.active_lesson()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = request.user.teacher
        if not teacher.active_lesson():
            form = self.form_class(request.user, request.POST)
            if form.is_valid():
                form.save(request.user)
                return HttpResponseRedirect(
                    reverse(
                        "schoolregister:lesson_details",
                        kwargs={"lesson_pk": teacher.active_lesson().id},
                    )
                )
        return HttpResponseRedirect(reverse("schoolregister:lesson_portal"))


@method_decorator(student_or_teacher_required, name="dispatch")
class LessonView(View):
    template_name = "schoolregister/lesson_details.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context["lesson"] = get_object_or_404(Lesson, pk=kwargs["lesson_pk"])
        context["presences"] = context["lesson"].presence_set.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=kwargs["lesson_pk"])
        presences = lesson.presence_set.all()
        logger.info("POST: {}".format(request.POST))
        if request.POST.get("submit"):
            present_student_ids = list(map(int, request.POST.getlist("present")))
            for presence in presences:
                if presence.student.id in present_student_ids:
                    presence.state = True
                else:
                    presence.state = False
                presence.save()
            context = {"lesson": lesson, "presences": presences}
        elif request.POST.get("end_lesson"):
            lesson.end_time = timezone.now()
            lesson.save()
            logger.info("Lesson save with end_time {}".format(lesson.end_time))
            context = {"lesson": lesson}
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name="dispatch")
class NoteView(View):
    template_name = "schoolregister/note_details.html"
    header_template = "schoolregister/_student_header.html"
    form_template = "schoolregister/_note_form.html"
    form_class = NoteForm

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs["note_pk"])
        return render(request, self.template_name, {"note": note})

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        form = self.note_form_class(request.user, request.POST)
        if form.is_valid():
            form.save(request.user, student)
        return HttpResponseRedirect(
            reverse("schoolregister:student_details", kwargs={"student_pk": student.id})
        )


@method_decorator(teacher_required, name="dispatch")
class NoteAddView(NoteView):
    template_name = "schoolregister/note_details.html"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        context = {
            "title": self.title,
            "student": student,
            "header_template": self.header_template,
            "form_template": self.form_template,
            "grade_form": self.form_class(request.user, student),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        form = self.form_class(request.user, student, request.POST)
        if form.is_valid():
            form.save(request.user, student)
        return HttpResponseRedirect(
            reverse("schoolregister:student_details", kwargs={"student_pk": student.id})
        )


@method_decorator(teacher_required, name="dispatch")
class NoteEditView(View):
    template_name = "schoolregister/note_details.html"

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs["note_pk"])
        return render(request, self.template_name, {"note": note})


@method_decorator(teacher_required, name="dispatch")
class NoteDeleteView(View):
    template_name = "schoolregister/note_details.html"

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs["note_pk"])
        return render(request, self.template_name, {"note": note})


@method_decorator(student_or_teacher_required, name="dispatch")
class NotesView(View):
    template_name = "schoolregister/notes_view.html"

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, id=kwargs["student_pk"])
        logger.debug("notes_view, is teacher: {}".format(request.user.is_teacher))
        if request.user.is_student:
            logger.debug(
                "notes_view, is owner: {}".format(request.user.student == student)
            )
        if request.user.is_teacher or request.user.student == student:
            notes = student.note_set.all()
            context = {"student": student, "notes": notes}
            return render(request, self.template_name, context)
        return HttpResponseForbidden()


@method_decorator(student_or_teacher_required, name="dispatch")
class StudentView(View):
    template_name = "schoolregister/student_details.html"
    grade_form_class = GradeForm
    note_form_class = NoteForm

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        context = {"student": student}
        if request.user.is_teacher:
            context["grade_form"] = GradeForm(request.user, student)
            context["note_form"] = NoteForm(request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=kwargs["student_pk"])
        if "grade-submit" in request.POST:
            form = self.grade_form_class(request.user, student, request.POST)
            if form.is_valid():
                form.save(request.user, student)
        elif "note-submit" in request.POST:
            form = self.note_form_class(request.user, request.POST)
            if form.is_valid():
                form.save(request.user, student)
        return HttpResponseRedirect(
            reverse("schoolregister:student_details", kwargs={"student_pk": student.id})
        )


@method_decorator(student_or_teacher_required, name="dispatch")
class TaughtView(View):
    template_name = "schoolregister/taught_details.html"

    def get(self, request, *args, **kwargs):
        taught = get_object_or_404(Taught, pk=kwargs["taught_pk"])
        lessons = Lesson.objects.filter(taught=taught)
        context = {"taught": taught, "lessons": lessons}
        return render(request, self.template_name, context)


@method_decorator(student_or_teacher_required, name="dispatch")
class TeacherView(View):
    template_name = "schoolregister/teacher_details.html"

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, pk=kwargs["teacher_pk"])
        return render(request, self.template_name, {"teacher": teacher})
