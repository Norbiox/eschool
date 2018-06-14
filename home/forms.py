from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import *
from schoolregister.models import Group

MAX_UPLOAD_SIZE = "10485760" # 10Mb

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('owner', 'uploaded_at')

    def clean_file(self):
        content = self.cleaned_data['file']
        if content._size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(("Please keep file size under %s. Current file size %s")%(MAX_UPLOAD_SIZE, content._size))
        return content


class ShareWithClassForm(forms.Form):

    group = forms.ModelChoiceField(
        queryset=Group.objects.all()
    )

    def clean_group(self):
        group = self.cleaned_data['group']
        return group


class ShareWithUserForm(forms.Form):

    shared_to = forms.ModelChoiceField(
        queryset=User.objects.all()
    )

    def clean_user(self):
        user = self.cleaned_data['user']
        return user
