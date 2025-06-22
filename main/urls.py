from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("teachers/login", views.teacher_login, name="teacher_login"),
    path("teachers/home", views.teacher_home, name="teacher_home"),
    path("teachers/all-students/", views.all_students, name="all_students"),
    path("teachers/logout/", LogoutView.as_view(next_page='teacher_login'),
         name="teacher_logout"),
    path("parents/logout/", LogoutView.as_view(next_page='parent_login'),
         name="parent_logout"),
    path('students/<int:student_id>/',
         views.student, name='student'),
    path('student/<int:student_id>/report/',
         views.student_report, name='student_report'),
    path("parents/login/", views.parent_login, name="parent_login"),
    path("parents/home/", views.parent_home, name="parent_home"),

]
