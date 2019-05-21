from django.urls import path, include

from . import views


app_name = "schoolregister"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # ex: /school/lesson/
    path(
        "lesson/",
        include(
            [
                path("", views.LessonPortalView.as_view(), name="lesson_portal"),
                # ex: /school/lesson/1/
                path(
                    "<int:lesson_pk>/",
                    views.LessonView.as_view(),
                    name="lesson_details",
                ),
            ]
        ),
    ),
    # ex: /school/taught/1/
    path("taught/<int:taught_pk>/", views.TaughtView.as_view(), name="taught_details"),
    # ex: /school/my-classes
    path("groups/", views.GroupsList.as_view(), name="groups"),
    # ex: /school/group/1/
    path(
        "group/<str:abbrev>/",
        include(
            [
                path("", views.GroupView.as_view(), name="group_details"),
                # ex: /school/group/1/give_grades/
                path(
                    "give_grades/",
                    views.GiveGroupGradesView.as_view(),
                    name="give_group_grades",
                ),
            ]
        ),
    ),
    # ex: /school/student/1/
    path(
        "student/<int:student_pk>/",
        include(
            [
                path("", views.StudentView.as_view(), name="student_details"),
                # ex: /school/student/1/grades/
                path("grades/", views.GradesView.as_view(), name="grades"),
                # ex: /school/student/1/add-grade/
                path("add-grade/", views.GradeAddView.as_view(), name="grade_add"),
                # ex: /school/student/1/notes/
                path("notes", views.NotesView.as_view(), name="notes"),
                # ex: /school/student/1/add-note/
                path("add-note/", views.NoteAddView.as_view(), name="note_add"),
                # ex: /school/student/1/grade/1/
                path(
                    "grade/<int:grade_pk>/",
                    include(
                        [
                            path("", views.GradeView.as_view(), name="grade_details"),
                            # ex: /school/student/1/grade/1/edit
                            path(
                                "edit/",
                                views.GradeEditView.as_view(),
                                name="grade_edit",
                            ),
                            # ex: /school/student/1/grade/1/delete
                            path(
                                "delete/",
                                views.GradeDeleteView.as_view(),
                                name="grade_delete",
                            ),
                        ]
                    ),
                ),
                # ex: /school/student/1/note/1
                path(
                    "note/<int:note_pk>/",
                    include(
                        [
                            path("", views.NoteView.as_view(), name="note_details"),
                            # ex: /school/student/1/note/1/edit
                            path(
                                "edit/", views.NoteEditView.as_view(), name="note_edit"
                            ),
                            # ex: /school/student/1/note/1/delete
                            path(
                                "delete/",
                                views.NoteDeleteView.as_view(),
                                name="note_delete",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    # ex: /school/teacher/1/
    path(
        "teacher/<int:teacher_pk>/", views.TeacherView.as_view(), name="teacher_details"
    ),
]
