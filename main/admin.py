from django.contrib import admin
from .models import Student, Teacher, Subject,  Parent, TermReport, ReportSubjectGrade
from .forms import ParentAdminForm


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ('first_name', 'surname', 'grade', 'dob')
    readonly_fields = ('first_name', 'surname', 'grade', 'dob')
    can_delete = False
    show_change_link = True


class TermReportInline(admin.TabularInline):
    model = TermReport
    extra = 0
    fields = ('term', 'days_absent', 'total_marks_obtained',
              'final_percentage', 'overall_grade', 'created_at')
    readonly_fields = ('total_marks_obtained',
                       'final_percentage', 'overall_grade', 'created_at')
    show_change_link = True  # allows clicking through to edit full report


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
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
    inlines = [TermReportInline]


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    form = ParentAdminForm
    list_display = ('user',)
    filter_horizontal = ("children",)


class ReportSubjectGradeInline(admin.TabularInline):
    model = ReportSubjectGrade
    extra = 1
    fields = ('subject', 'total_marks', 'marks_obtained',
              'grade', 'remarks', 'class_average')
    readonly_fields = ('grade', 'remarks', 'total_marks')

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # trigger grade/percentage calculation
        super().save_model(request, obj, form, change)


@admin.register(TermReport)
class TermReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'created_at', 'days_absent',
                    'total_marks_obtained', 'final_percentage', 'overall_grade')
    list_filter = ('term',)
    inlines = [ReportSubjectGradeInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for inline_obj in instances:
            inline_obj.report = form.instance
            inline_obj.save()
        formset.save_m2m()

        # If it's the ReportSubjectGrade formset, compute totals
        if formset.model == ReportSubjectGrade:
            grades = form.instance.subject_grades.all()
            if grades.exists():
                total_marks = sum(g.marks_obtained for g in grades)
                final_percentage = total_marks / grades.count()
                overall_grade = self.get_overall_grade(final_percentage)

                form.instance.total_marks_obtained = total_marks
                form.instance.final_percentage = round(final_percentage, 2)
                form.instance.overall_grade = overall_grade
                form.instance.save()

    def get_overall_grade(self, percentage):
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
