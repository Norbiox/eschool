from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    re_path(r'^login/$', auth_views.login, {'template_name': 'home/login.html'}, name='login'),
    re_path(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('<int:pk>/profile/', views.ProfileView.as_view(), name='profile'),
]
