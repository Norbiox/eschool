from django import forms
from django.db import models
from django.forms import ModelForm

from .models import *

class GiveGrade(ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'rate', 'weight', 'description']


class GiveGradeSubjectSpecified(ModelForm):
    class Meta:
        model = Grade
        fields = ['rate', 'weight', 'description']
