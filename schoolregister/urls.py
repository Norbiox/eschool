from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'schoolregister'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # ex: /schoolregister/groups/
    path('groups/', views.GroupsList.as_view(), name='groups'),
    # ex: /schoolregister/group/1
    path('group/<str:abbrev>/', views.GroupView.as_view(), name='group_details'),
    # ex: /schoolregister/student/1/
    path('student/<int:pk>/', views.StudentView.as_view(), \
        name='student_details'),
    # ex: /schoolregister/teacher/1/
    path('teacher/<int:pk>/', views.TeacherView.as_view(), \
        name='teacher_details'),
]
