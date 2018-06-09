# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator
from django.db import models

from home.models import User

logger = logging.getLogger(__name__)


class Subject(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    abbrev = models.CharField(max_length=7)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Teacher(models.Model):
    NONE = ''
    ENGINEER = 'Inż.'
    MASTER = 'Mgr'
    MASTER_ENGINEER = 'Mrg Inż'
    TITLES = (
        (NONE, ''),
        (ENGINEER, 'Inżynier'),
        (MASTER, 'Magister'),
        (MASTER_ENGINEER, 'Magister Inżynier')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=TITLES, default=NONE, \
        null=True, blank=True
    )
    specialization = models.ForeignKey(Subject, on_delete=models.CASCADE, \
        null=True, blank=True
    )
    birth_date = models.DateField()
    PESEL = models.CharField(max_length=11, unique=True, default='')
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=17)

    def __str__(self):
        return ' '.join([self.user.first_name, self.user.last_name])

    def __repr__(self):
        return ' '.join(['Teacher', self.user.first_name, self.user.last_name])

    def __eq__(self, other):
        return self.id == other.id

    def full_name(self):
        title = self.title if self.title is not None else ''
        return ' '.join([title, self.user.first_name, self.user.last_name])

    def email(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Group(models.Model):
    year = models.IntegerField(validators=[MinValueValidator(0),
                                           MaxValueValidator(8)])
    letter = models.CharField(max_length=3)
    supervisor = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    @property
    def abbrev(self):
        return str(self.year) + self.letter

    def __str__(self):
        return self.abbrev

    def __repr__(self):
        return ' '.join(['Group', self.abbrev])

    def __eq__(self, other):
        return self.id == other.id

    def name(self):
        return ' '.join(['Group', self.abbrev])
        name.short_description = 'Group name'

    def number_of_students(self):
        return len(list(filter(lambda s: s.group == self, Student.objects.all())))

    def students(self):
        students_list = list(filter(lambda s: s.group == self, Student.objects.all()))
        return sorted(students_list, key=lambda s: s.user.last_name)

class Taught(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject.name

    def __repr__(self):
        return ' '.join([self.subject, 'in', self.group])

    def __eq__(self, other):
        return self.id == other.id

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, \
    null=True
    )
    birth_date = models.DateField()
    PESEL = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=17)

    def __str__(self):
        return ' '.join([self.user.first_name, self.user.last_name])

    def __repr__(self):
        return ' '.join([Student, self.user.first_name, self.user.last_name, ',', self.group])

    def __eq__(self, other):
        return self.id == other.id

    def full_name(self):
        return ' '.join([self.user.first_name, self.user.last_name])
        name.short_description = 'Student'

    def email(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Rate(models.Model):
    value = models.IntegerField(default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Taught, on_delete=models.CASCADE)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, null=True, blank=True, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' : '.join([str(self.subject), self.get_mark_display()])

    def __repr__(self):
        return ' : '.join([str(self.subject), self.get_mark_display()])


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=True)
    topic = models.CharField(max_length=200)

    def __str__(self):
        return ' '.join([str(self.subject), str(self.date)])

    def __repr__(self):
        return ' '.join(['Lesson', str(self.subject), str(self.date)])


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    positive = models.BooleanField()
    text = models.CharField(max_length=500)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' '.join([str(self.notes_card.student), self.text, str(self.datetime)])

    def __repr__(self):
        return ' '.join([self.notes_card, self.text, str(self.datetime)])


class Presence(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.state
