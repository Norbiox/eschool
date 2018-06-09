# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models as m


class User(AbstractUser):

    class Meta:
        ordering = ['last_name']

    is_student = m.BooleanField('student status', default=False)
    is_teacher = m.BooleanField('teacher status', default=False)
    is_writer = m.BooleanField('teacher status', default=False)

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])
