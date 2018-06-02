from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from home.views import LoginView, LogoutView

app_name = 'schoolregister'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # ex: /school/student/1/
    path('student/<int:pk>/', views.StudentView.as_view(), \
        name='student_details'),
    # ex: /school/teacher/1/
    path('teacher/<int:pk>/', views.TeacherView.as_view(), \
        name='teacher_details'),
    path('groups/', views.GroupsList.as_view(), name='groups_list'),
]
