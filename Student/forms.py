from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *



class RegisterUser(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Enter Your Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Your Password")
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Enter Your Password")
    

class UserEditForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['first_name',"last_name","email"]
        
        widgets = {
            "first_name":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Firstname Here"}),
            "last_name":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Last Name Here"}),
            "email":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Email Here"}),
        }
        

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class AssignmentForm(forms.ModelForm):
    class Meta:
        model =  Assignment
        fields = ["name","assigned_data","posting_date","posting_time"]
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control myinput","placeholder":"Enter Assignment Name: Practice Question"}),
            "assigned_data":forms.FileInput(attrs={"class":"form-control myimage"}),
            "posting_date":DateInput(attrs={"class":"form-control mydateinput"}),
            "posting_time":TimeInput(attrs={"class":"form-control mytimeinput"}),
        }
        
class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model =  SubmitAssignment
        fields = ["submitted_data"]
        widgets = {
            
            "submitted_data":forms.FileInput(attrs={"class":"form-control myimage"}),

        }
        
class AssignmentCheckForm(forms.ModelForm):
    class Meta:
        model = AssignmentCheck
        fields = ["correct_status","suggestion_for_wrong"]
        labels = {
            "correct_status":"Are all the answers Correct?",
            "suggestion_for_wrong":"Write Reviews to student.."
        }
    
class CorrectAnswerForm(forms.ModelForm):
    class Meta:
        model = CorrectAnswer
        fields = ["correct_answer"]
        labels = {
            "correct_answer":"Upload Your Correct Answer For Given Question",
        }
        help_text = {
            "correct_answer":"Make Sure That Your answer is correct"  + 
            "You can Submit Your answer only once.",
        }