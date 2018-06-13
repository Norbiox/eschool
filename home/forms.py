from django import forms
from django.db import models
from django.forms import ModelForm
from django.utils import timezone

from .models import *


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('owner', 'uploaded_at')
