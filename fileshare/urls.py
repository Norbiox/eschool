from django.urls import path, re_path, include

from eschool import settings
from . import views

app_name='fileshare'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', include([
        path('delete/', views.FileDeleteView.as_view(), name='delete'),
        path('download/', views.FileDownloadView.as_view(), name='download'),
        path('share/', views.FileShareView.as_view(), name='share'),
        path('show/', views.FileShowView.as_view(), name='show'),
    ]))
]
