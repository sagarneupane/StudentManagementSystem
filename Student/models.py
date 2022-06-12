from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

    


# import os

class University(models.Model):
    university_name= models.CharField(max_length=150)
    university_code =  models.CharField(max_length=5)
    university_description = models.TextField()
    university_url = models.URLField()
        
    def __str__(self):
        return self.university_code

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_code =  models.CharField(max_length=5, unique=True)
    course_description = models.TextField()
    course_url =  models.URLField()
    university_affiliation=models.ManyToManyField(University,related_name='university', through='ModelUniversity')
    
    def course_university_affiliation(self):
        return [str(u) for u in self.university_affiliation.all()]
    
    def __str__(self):
        return self.course_name

class ModelUniversity(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(on_delete=models.CASCADE, to='Student.course')
    university = models.ForeignKey(on_delete=models.CASCADE, to='Student.university')

    def __str__(self):
        return self.name

semester = (('First Sem', 'First Semster'),
            ('Second Sem', 'Second Semester'), ('Third Sem', 'Third Semester'),
            ('Fourth Sem', 'Fourth Semester'), ('Fifth Sem', 'Fifth Semester'),
            ('Sixth Sem', 'Sixth Semester'), 
            ('Seventh Sem', 'Seventh Semester'), ('Eighth Sem', 'Eighth Semester'))


class Stu_Subject(models.Model):
    subject_name= models.CharField(max_length=150)
    subject_code= models.CharField(max_length=10)
    subject_details= models.TextField()
    full_marks= models.IntegerField(validators=[MaxValueValidator(101),MinValueValidator(0)])
    theory_marks= models.IntegerField(validators=[MinValueValidator(0)])
    theory_pass_marks= models.IntegerField(validators=[MinValueValidator(0)])
    practical_marks= models.IntegerField(validators=[MinValueValidator(0)])
    practical_pass_marks= models.IntegerField(validators=[MinValueValidator(0)])
    semester = models.CharField(choices=semester,max_length=20)
    course_related = models.ForeignKey(ModelUniversity,on_delete=models.CASCADE)
    course_detail_file = models.FileField(upload_to="files/",default=None)
    def __str__(self):
        return self.subject_code

    def pass_marks(self):
        return self.practical_pass_marks + self.theory_pass_marks
    
class Teacher_Details(models.Model):
    address = models.CharField(max_length=150)
    image = models.ImageField(default='none', upload_to='img/')
    details_updated = models.DateTimeField(auto_now_add=True)
    subject_taught = models.ManyToManyField(to='Student.stu_subject')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
        
    def __str__(self):
        return self.user.first_name

    def subject_teacher_teaches(self):
        return [str(s) for s in self.subject_taught.all()]

class Student_Details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='none', upload_to='img/')
    details_updated = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=150)
    admission_date = models.DateField()
    previous_college = models.CharField(max_length=150)
    course_enrolled = models.ForeignKey(ModelUniversity,on_delete=models.CASCADE)
    semester = models.CharField(max_length=20,choices=semester,default=None)
        
    def __str__(self):
        return self.user.first_name
    


class Assignment(models.Model):
    name = models.CharField(max_length=200)
    dateTime = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Stu_Subject, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Teacher_Details,null=True, on_delete=models.SET_NULL)
    assigned_data = models.FileField(upload_to="assignment/")
    posting_date = models.DateField()
    posting_time = models.TimeField()
    
    def __str__(self):
        return self.name

class SubmitAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, null =True,on_delete=models.SET_NULL)  
    submitted_date = models.DateField(auto_now_add=True)
    submitted_time = models.TimeField(auto_now_add=True)
    submitted_data = models.FileField(upload_to="assignmentsubmitted/")
    edited = models.IntegerField(default=0)

    def submision_name(self):
        return f'{self.assignment} {self.submitted_by}'
    
    def __str__(self):
        return self.assignment.name

class AssignmentCheck(models.Model):
    assignment = models.ForeignKey(SubmitAssignment, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    checked_status = models.BooleanField(auto_created=True,default=True)
    checked_date = models.DateTimeField(auto_now_add=True)
    correct_status = models.BooleanField()
    suggestion_for_wrong = models.TextField(default=None,blank=True)

from .formatchecker import ContentRestrictiononFileField
    

class CorrectAnswer(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    subject = models.ForeignKey(Stu_Subject, on_delete=models.DO_NOTHING)
    correct_answer = ContentRestrictiononFileField(upload_to="answers/",content_types =["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                                                        "image/jpeg","image/png","image/JPG","image/jpg"]
                                                   ,max_upload_size=1480000
                                                   ,blank=True,null=True)
    
    def __str__(self):
        return self.assignment.name