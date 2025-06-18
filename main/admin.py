from django.contrib import admin
from .models import Student, Teacher, Subject, Report, Parent
from .forms import ParentAdminForm


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ('first_name', 'surname', 'grade', 'dob')
    readonly_fields = ('first_name', 'surname', 'grade', 'dob')
    can_delete = False
    show_change_link = True


class ReportInline(admin.TabularInline):
    model = Report
    extra = 1


@admin.register(Subject)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name',)
    list_filter = ('teacher',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'grade')
    list_filter = ('grade',)
    search_fields = ('name',)
    filter_horizontal = ('subjects',)
    inlines = [StudentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'grade',
                    'dob', 'class_teacher', 'profile_pic')
    list_filter = ('grade', 'class_teacher')
    search_fields = ('first_name', 'surname')
    filter_horizontal = ('subjects',)
    inlines = [ReportInline]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'uploaded_at')
    list_filter = ('term', 'uploaded_at')
    search_fields = ('student__first_name', 'student__surname')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    form = ParentAdminForm
    list_display = ('user',)
    filter_horizontal = ("children",)
