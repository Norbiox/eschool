from django.contrib.auth.decorators import user_passes_test
from django.urls import resolve, reverse
from eschool import settings


def student_required(function=None):
    '''
    Decorator for views that checks that the logged in user is a student.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=settings.LOGIN_URL,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def student_or_teacher_required(function=None):
    '''
    Decorator for views that checks that the logged in user is a student or teacher.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_student or u.is_teacher),
        login_url=settings.LOGIN_URL,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None):
    '''
    Decorator for views that checks that the logged in user is a teacher.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=settings.LOGIN_URL,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
