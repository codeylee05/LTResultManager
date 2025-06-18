from django.db import models
from django.contrib.auth.models import User

GRADE_CHOICES = [
    ('US', 'US'),
    ('IGCSE_1', 'IGCSE 1'),
    ('IGCSE_2', 'IGCSE 2'),
    ('AS_1', 'AS Level 1'),
    ('AS_2', 'AS Level 2'),
    ('GED', 'GED'),
]


class Subject(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.SET_NULL, null=True, related_name='teacher_subjects')

    def __str__(self):
        return f"{self.name}"


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    subjects = models.ManyToManyField(
        "Subject", related_name='subject_teachers', blank=True)

    def __str__(self):
        if self.user:
            return f"{self.name} ({self.user.username})"
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    dob = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    class_teacher = models.ForeignKey(
        "Teacher", on_delete=models.SET_NULL, null=True, related_name='class_students')
    subjects = models.ManyToManyField(
        "Subject", related_name='subject_students', blank=True)
    profile_pic = models.ImageField(
        upload_to='student_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class Report(models.Model):

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='reports')
    term = models.CharField(max_length=20, default="Term 2")
    report_file = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.term} Report"


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField("Student", related_name='parents')

    def __str__(self):
        return self.user.username
