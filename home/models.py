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
