from django import forms
from django.db import models
from django.forms import ModelForm

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


class LessonForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)


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
