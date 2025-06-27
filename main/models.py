from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

GRADE_CHOICES = [
    ('Grade 7', 'Grade 7'),
    ('Grade 8', 'Grade 8'),
    ('IGCSE', 'IGCSE'),
    ('AS', 'AS'),
    ('GED', 'GED'),
]

GRADE_SCALE = [
    (90, 'A+'),
    (80, 'A'),
    (70, 'B'),
    (60, 'C'),
    (50, 'D'),
    (40, 'E'),
    (0, 'U'),
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
        return f"{self.name} ({self.user.username})" if self.user else self.name


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


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField("Student", related_name='parents')

    def __str__(self):
        return self.user.username if self.user else "Orphaned Parent"


class TermReport(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='term_reports')
    term = models.CharField(max_length=20, default="Term 2")
    days_absent = models.PositiveIntegerField(default=0)

    total_marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    final_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    # E.g. A+, A, B, etc.
    overall_grade = models.CharField(max_length=2, blank=True)

    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.term}"


class ReportSubjectGrade(models.Model):
    report = models.ForeignKey(
        'TermReport', on_delete=models.CASCADE, related_name='subject_grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField(default=100)
    marks_obtained = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.CharField(max_length=100, blank=True)
    class_average = models.PositiveIntegerField(blank=True, null=True)

    def calculate_grade(self):
        if self.total_marks == 0:
            return ""
        percentage = (self.marks_obtained / self.total_marks) * 100
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        elif percentage >= 40:
            return "E"
        else:
            return "U"

    def generate_remarks(self, grade):
        remarks_map = {
            "A+": "Outstanding",
            "A": "Excellent",
            "B": "Good effort",
            "C": "Fair",
            "D": "Satisfactory",
            "E": "Needs work",
            "U": "Ungraded",
        }
        return remarks_map.get(grade, "")

    def clean(self):

        if self.total_marks is not None and self.marks_obtained is not None:

            self.grade = self.calculate_grade()
            self.remarks = self.generate_remarks(self.grade)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.report.student} - {self.subject}"
