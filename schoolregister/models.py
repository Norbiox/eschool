# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, \
    RegexValidator, MaxLengthValidator
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

    def full_name(self):
        title = self.title if self.title is not None else ''
        return ' '.join([title, self.user.first_name, self.user.last_name])

    def email(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def active_lesson(self):
        lessons = Lesson.objects.filter(teacher=self)
        active = list(filter(lambda l: l.is_active(), lessons))
        if active:
            return active[0]
        return None


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

    def name(self):
        return ' '.join(['Group', self.abbrev])
        name.short_description = 'Group name'

    def number_of_students(self):
        return len(self.student_set.all())

    def students_number(self, student):
        return list(self.student_set.all()).index(student) + 1


class Taught(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.abbrev + ' - ' + self.subject.name

    def __repr__(self):
        return ' '.join([self.subject, 'in', self.group])


class Student(models.Model):

    class Meta:
        ordering = ['user']

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

    def full_name(self):
        return ' '.join([self.user.first_name, self.user.last_name])
        name.short_description = 'Student'

    def email(self):
        return self.user.email

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def number_of(self):
        """Number of student in group list"""
        return self.group.students_number(self)

    def active_lesson(self):
        lessons = Lesson.objects.filter(taught__in=self.group.taught_set.all())
        active = list(filter(lambda l: l.is_active(), lessons))
        if active:
            return active[0]
        return None


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
    weight = models.FloatField(default=1.0)
    description = models.CharField(max_length=200, default='', null=True, \
        blank=True, validators=[MaxLengthValidator(200)])
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['datetime']
        get_latest_by = ['datetime']

    def __str__(self):
        return str(self.student) + ' ' + str(self.student.group) + ' : ' + str(self.rate)

    def __repr__(self):
        return str(self.student) + ' ' + str(self.student.group) + ' : ' + str(self.rate)

    def get_absolute_url(self):
        return reverse('schoolregister:grade_details', kwargs={'pk':self.pk})


class Lesson(models.Model):

    class Meta:
        ordering = ['start_time']
        get_latest_by = ['start_time']

    taught = models.ForeignKey(Taught, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True, blank=True)
    topic = models.CharField(max_length=200)

    def __str__(self):
        return ' '.join([str(self.taught), str(self.start_time)])

    def __repr__(self):
        return ' '.join(['Lesson', str(self.taught), str(self.start_time)])

    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs) # Call the "real" save() method.
        for student in self.taught.group.student_set.all():
            if Presence.objects.filter(lesson=self).filter(student=student):
                continue
            Presence(lesson=self, student=student, state=True).save()

    def is_active(self):
        """Returns True if lesson has not been closed"""
        if self.start_time and not self.end_time:
            return True
        return False

    def number_of(self):
        """Returns number of lesson from specific subject in specific class."""
        previous_lessons = Lesson.objects.filter(taught=self.taught).filter(start_time__lt=self.start_time)
        return len(previous_lessons) + 1


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    given_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    positive = models.BooleanField()
    text = models.CharField(max_length=500)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' '.join([str(self.student), self.text])

    def __repr__(self):
        return ' '.join([str(self.student), self.text])


class Presence(models.Model):

    class Meta:
        ordering = ['student']

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    def __str__(self):
        return str(self.state)
