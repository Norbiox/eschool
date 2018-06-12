from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'schoolregister'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # ex: /schoolregister/lesson/
    path('lesson/', views.LessonPortalView.as_view(), name='lesson_portal'),
    # ex: /schoolregister/lesson/1/
    path('lesson/<int:pk>/', views.LessonView.as_view(), \
        name='lesson_details'),

    # ex: /schoolregister/taught/1/
    path('taught/<int:pk>/', views.TaughtView.as_view(), \
        name='taught_details'),

    # ex: /schoolregister/my-classes
    path('groups/', views.GroupsList.as_view(), name='groups'),
    # ex: /schoolregister/group/1/
    path('group/<str:abbrev>/', views.GroupView.as_view(), name='group_details'),

    # ex: /schoolregister/student/1/
    path('student/<int:student_pk>/', include([
        path('', views.StudentView.as_view(), name='student_details'),
        # ex: /schoolregister/student/1/grade/1/
        path('grade/<int:grade_pk>/', include([
            path('', views.GradeView.as_view(), name='grade_details'),
            # ex: /schoolregister/student/1/grade/1/add
            path('add/', views.GradeAddView.as_view(), name='grade_add'),
            # ex: /schoolregister/student/1/grade/1/edit
            path('edit/', views.GradeEditView.as_view(), name='grade_edit'),
            # ex: /schoolregister.student/1/grade/1/delete
            path('delete/', views.GradeDeleteView.as_view(), name='grade_delete'),
        ])),
        # ex: /schoolregister/student/1/note/1
        path('note/<int:note_pk>/', include([
            path('', views.NoteView.as_view(), name='note_details'),
            # ex: /schoolregister/student/1/note/1/add
            path('add/', views.NoteAddView.as_view(), name='note_add'),
            # ex: /schoolregister/student/1/note/1/edit
            path('edit/', views.NoteEditView.as_view(), name='note_edit'),
            # ex: /schoolregister.student/1/note/1/delete
            path('delete/', views.NoteDeleteView.as_view(), name='note_delete'),
        ]))
    ])),

    # ex: /schoolregister/teacher/1/
    path('teacher/<int:pk>/', views.TeacherView.as_view(), \
        name='teacher_details'),
]
