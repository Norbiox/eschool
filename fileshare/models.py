# -*- coding: utf-8 -*-

import logging
import os

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models

from eschool import settings
from home.models import User


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

    def link(self):
        return '/media/user_{}/{}'.format(self.owner.id, str(self))

    def path(self):
        return settings.MEDIA_ROOT + '/user_{}/{}'.format(self.owner.id, str(self))


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
