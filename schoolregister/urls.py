from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'schoolregister'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # ex: /schoolregister/grade/1/
    path('grade/<int:pk>/', views.GradeView.as_view(), \
        name='grade_details'),
    # ex: /schoolregister/note/1/
    path('note/<int:pk>/', views.NoteView.as_view(), \
        name='note_details'),
    # ex: /schoolregister/lesson/1/
    path('lesson/<int:pk>/', views.LessonView.as_view(), \
        name='lesson_details'),

    # ex: /schoolregister/taught/1/
    path('taught/<int:pk>/', views.TaughtView.as_view(), \
        name='taught_details'),
    # ex: /schoolregister/taught/1/give_grades/
    #path('taught/<int:pk>/give_grades/', views.GiveGradesWholeClassView.as_view(),\
    #    name='give_grades_whole_class'),

    # ex: /schoolregister/my-classes
    path('groups/', views.GroupsList.as_view(), name='groups'),
    # ex: /schoolregister/group/1/
    path('group/<str:abbrev>/', views.GroupView.as_view(), name='group_details'),

    # ex: /schoolregister/student/1/
    path('student/<int:pk>/', views.StudentView.as_view(), \
        name='student_details'),
    # ex: /schoolregister/student/1/grades/
    path('student/<int:pk>/grades/', views.GradesView.as_view(), \
        name='student_grades'),
    # ex: /schoolregister/student/1/notes/
    path('student/<int:pk>/notes/', views.NotesView.as_view(), \
        name='student_notes'),
    # ex: /schoolregister/student/1/give_grade/
    path('student/<int:pk>/give_grade/', views.GiveGradeView.as_view(), \
        name='student_give_grade'),

    # ex: /schoolregister/teacher/1/
    path('teacher/<int:pk>/', views.TeacherView.as_view(), \
        name='teacher_details'),

    # ex: /schoolregister/lesson/
    path('lesson/', views.LessonPortalView.as_view(), name='lesson_portal'),
]
