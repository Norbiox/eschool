from django import forms
from django.db import models
from django.forms import ModelForm

from .models import *

class GiveGrade(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(GiveGrade, self).__init__(*args, **kwargs)
        self.fields['Subject'] = forms.ModelChoiceField(
            queryset=Taught.objects.filter(teacher=user.teacher)
        )
        self.fields['Rate'] = forms.ModelChoiceField(
            queryset=Rate.objects.all()
        )
        self.fields['Weight'] = forms.FloatField(
            max_value=2.0, min_value=0.0, initial=1.0
        )
        descr_max_len = Grade._meta.get_field('description').max_length
        self.fields['Description'] = forms.CharField(
            widget= forms.Textarea(attrs={'cols':'40', 'rows':'5', 'style':'resize:none;'}),
            max_length=Grade._meta.get_field('description').max_length,
            required = False,
            empty_value=''
        )


class GiveGradeSubjectSpecified(ModelForm):
    class Meta:
        model = Grade
        fields = ['rate', 'weight', 'description']
