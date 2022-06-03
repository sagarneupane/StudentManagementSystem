from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["course_name","course_code","course_description","course_university_affiliation","course_url"]
    
# class CourseInline(admin.TabularInline):
#         model = Course.university_affiliation.through   
    
    
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["university_name","university_code","university_description","university_url"]
    
@admin.register(ModelUniversity)
class ModelUniversityAdmin(admin.ModelAdmin):
    list_display = ["university","course","name"]
    

@admin.register(Stu_Subject)

class Stu_SubjectAdmin(admin.ModelAdmin):
    list_display = ["subject_name","subject_code","subject_details",
                    "semester",
                    "course_related",
                    "full_marks","theory_marks","theory_pass_marks","practical_marks",
                    "practical_pass_marks",
                    "pass_marks",
                    "course_detail_file"
                    
                    
                    ]


@admin.register(Student_Details)
class Student_DetailsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "address",
        "image",
        "admission_date",
        "details_updated",
        "previous_college",
        "course_enrolled",
        "semester"
        ]
    
@admin.register(Teacher_Details)
class Teacher_DetailsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "address",
        "image",
        "details_updated",
        "subject_teacher_teaches",
        ]
    
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        "dateTime",
        "subject",
        "assigned_by",
        "assigned_data",
        "posting_date",
        "posting_time",
    ]

@admin.register(SubmitAssignment)
class SubmitAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        'assignment',
        "submitted_by",
        "submitted_date",
        "submitted_time",
        "submitted_data",
        "edited",
        "submision_name"
    ]
@admin.register(AssignmentCheck)
class AssignmentCheckAdmin(admin.ModelAdmin):
    list_display = [
        "assignment","checked_date","correct_status","suggestion_for_wrong","checked_by"
    ]