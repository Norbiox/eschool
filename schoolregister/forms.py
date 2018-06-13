from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import *

class GradeForm(forms.Form):

    def __init__(self, user, student, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        if 'subject' not in kwargs:
            self.fields['Subject'] = forms.ModelChoiceField(
                queryset=Taught.objects.filter(teacher=user.teacher).filter(group=student.group)
            )
        self.fields['Rate'] = forms.ModelChoiceField(
            queryset=Rate.objects.all(),
        )
        self.fields['Weight'] = forms.FloatField(
            max_value=2.0, min_value=0.0, initial=1.0
        )
        self.fields['Description'] = forms.CharField(
            widget=forms.Textarea(attrs={'cols':'40', 'rows':'5', 'style':'resize:none;'}),
            max_length=Grade._meta.get_field('description').max_length,
            required = False,
            empty_value=''
        )

    def save(self, user, student, *args, **kwargs):
        grade = Grade(
            student=student,
            given_by=user.teacher,
            datetime=timezone.now(),
            subject=self.cleaned_data['Subject'],
            weight=self.cleaned_data['Weight'],
            rate=self.cleaned_data['Rate'],
            description=self.cleaned_data['Description']
        )
        grade.save()


class LessonForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        if 'taught' not in kwargs:
            self.fields['Class&Subject'] = forms.ModelChoiceField(
                queryset=Taught.objects.filter(teacher=user.teacher)
            )
        self.fields['Topic'] = forms.CharField(
            widget=forms.Textarea(attrs={'cols':'100', 'rows':'2', 'style':'resize:none;'}),
            max_length=Grade._meta.get_field('description').max_length,
            required = False,
            empty_value=''
        )

    def save(self, user, *args, **kwargs):
        lesson = Lesson(
            taught=self.cleaned_data['Class&Subject'],
            teacher=teacher,
            start_time=timezone.now(),
            topic=self.cleaned_data['Topic']
        )
        lesson.save()


class NoteForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['Kind of note'] = forms.ChoiceField(
            choices=[(True, 'POSITIVE'),(False, 'NEGATIVE')]
        )
        self.fields['Description'] = forms.CharField(
            widget= forms.Textarea(attrs={'cols':'40', 'rows':'10', 'style':'resize:none;'}),
            max_length=Note._meta.get_field('text').max_length,
            required = True,
            empty_value=''
        )

    def save(self, user, student, *args, **kwargs):
        note = Note(
            student=student,
            given_by=user.teacher,
            datetime=timezone.now(),
            positive=self.cleaned_data['Kind of note'],
            text=self.cleaned_data['Description']
        )
        note.save()
