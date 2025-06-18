from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher, Student, Parent, Report
from django.shortcuts import render, get_object_or_404
from .forms import ReportUploadForm


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


@login_required
def student_report(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    return render(request, 'main/student_report.html', {'student': student})


def student_report(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
    report = student.reports.filter(term="Term 2").first()
    form = ReportUploadForm()

    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.save(commit=False)
            uploaded.student = student
            uploaded.term = "Term 2"
            uploaded.save()
            return redirect('student_report', student_id=student.id)

    context = {
        'student': student,
        'form': form,
        'term2_report': report
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
