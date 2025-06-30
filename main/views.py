from urllib import response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Student, Parent, TermReport
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse
import tempfile
import os
from django.contrib.staticfiles import finders
from django.conf import settings
from django.http import HttpResponseForbidden, Http404
'''import logger'''


def index(request):

    return render(request, "main/index.html")


def teacher_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect('teacher_home')

        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'main/teacher_login.html')


@login_required
def teacher_home(request):

    try:

        teacher = Teacher.objects.get(user=request.user)
        students = Student.objects.filter(class_teacher=teacher)

    except Teacher.DoesNotExist:

        students = []

    return render(request, 'main/teacher_home.html', {
        'students': students
    })


@login_required
def all_students(request):

    grades = {}
    for student in Student.objects.all().order_by('grade', 'surname'):
        grades.setdefault(student.grade, []).append(student)

    return render(request, 'main/all_students.html', {'grades': grades})


@login_required
def student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    return render(request, 'main/student.html', {'student': student})


def student_report(request, student_id):

    student = get_object_or_404(Student, pk=student_id)

    term_report = student.term_reports.order_by('-created_at').first()

    subject_grades = term_report.subject_grades.all() if term_report else []

    context = {
        'student': student,
        'term_report': term_report,
        'subject_grades': subject_grades,
    }

    return render(request, 'main/student_report.html', context)


def parent_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:

            try:

                user_parent = Parent.objects.get(user=user)
                login(request, user)
                return redirect("parent_home")

            except Parent.DoesNotExist:

                messages.error(request, "Not a parent account.")
        else:

            messages.error(request, "Invalid credentials.")

    return render(request, "main/parent_login.html")


def parent_home(request):

    parent = Parent.objects.get(user=request.user)
    children = parent.children.all()
    return render(request, "main/parent_home.html", {"children": children})


def generate_report_pdf(request, student_id):

    student = get_object_or_404(Student, pk=student_id)

    user = request.user

    if hasattr(user, 'parent'):
        if not student in user.parent.children.all():
            return HttpResponseForbidden("You are not allowed to view this report.")

    elif hasattr(user, 'teacher'):
        if student.class_teacher != user.teacher:
            return HttpResponseForbidden("You are not allowed to view this report.")

    elif not user.is_staff and not user.is_superuser:
        return HttpResponseForbidden("You are not allowed to view this report.")

    student = Student.objects.get(id=student_id)
    term_report = student.term_reports.first()
    subject_grades = term_report.subject_grades.all()

    logo_static_path = finders.find('main/images/ship_report_header.jpg')
    if logo_static_path:

        logo_absolute_path = os.path.abspath(logo_static_path).replace('\\', '/')
        logo_url = 'file:///' + logo_absolute_path.lstrip('/')
        '''logger.info(f"Resolved WeasyPrint logo path: {logo_url}")'''
    else:

        logo_url = None
        '''logger.warning("Logo not found for WeasyPrint.")'''

    html_string = render_to_string("main/student_report_pdf.html", {
        "student": student,
        "term_report": term_report,
        "subject_grades": subject_grades,
        "logo_url": logo_url,
    })

    css_path = finders.find("main/styles/report_styles.css")

    html = HTML(string=html_string, base_url=request.build_absolute_uri("/"))
    pdf_file = html.write_pdf(stylesheets=[CSS(css_path)])

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="term_report.pdf"'
    return response
