# -*- coding: utf-8 -*-

import logging
import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models


class User(AbstractUser):

    class Meta:
        ordering = ['last_name']

    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    is_writer = models.BooleanField('teacher status', default=False)

    def __str__(self):
        return self.full_name()

    def __repr__(self):
        return self.full_name()

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_last_actions(self):
        """Gets last actions interesting for user.
        If user is student last actions are false-presences, grades and notes.
        If user is teacher last actions are false-presences, grades and notes of
            students of class that user is supervising, or nothing if user
            is not supervisor of any class."""
        if self.is_student:
            return None
        elif self.is_teacher:
            return None


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class File(models.Model):
    class Meta:
        ordering = ['owner','uploaded_at']

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return os.path.basename(self.file.name)

    def __repr__(self):
        return os.path.basename(self.file.name)


class Share(models.Model):
    class Meta:
        ordering = ['shared_to','file']

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file.owner)+'/'+str(self.file)+\
            ' shared to: '+str(self.shared_to.full_name())

    def __repr__(self):
        return str(self.file.owner)+'/'+str(self.file)+\
            ' shared to: '+str(self.shared_to.full_name())

    def owner(self):
        return self.file.owner.full_name()
