from django.shortcuts import render, HttpResponse,redirect,Http404
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User,Group
from .models import *
from django.urls import reverse

# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, "dashboard.html")
    else:
        return redirect("profile")

def signin(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            fm = LoginForm(request=request,data=request.POST)
            if fm.is_valid():
                user = authenticate(username=fm.cleaned_data['username'],password=fm.cleaned_data['password'])
                if user is not None:
                    login(request,user)
                    return redirect("profile")
        else:      
            fm = LoginForm()
        return render(request,'login.html',{"form":fm})
    else:
        return redirect("profile")


def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = RegisterUser(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,"User Created Successfully")
                return redirect("signin") 
        else:
            fm = RegisterUser()
        return render(request,'register.html',{"form":fm})
    else:
        return redirect("profile")


def profile(request):
    if request.user.is_authenticated:
        
        return render(request,"profile.html")
    else:
        return redirect("signin")
    
def signout(request):
    logout(request)
    return redirect("signin")


def editProfile(request,id=0):
    if request.user.is_authenticated:
        users = User.objects.get(pk=request.user.id)
        
        if request.method=="POST":
            fm = UserEditForm(instance=users,data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,"User Updated Successfully")
                return redirect("profile")
        else:
            fm = UserEditForm(instance=users)
        return render(request,"editprofile.html",{"form":fm})
    else:
        return redirect("signin")
    
# from operator import attrgetter

def viewProfile(request,id=0):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user_group = Group.objects.get(user=user.id)
        context = {"thisuser":user,"user_group":user_group}
        
        if user_group.name == "Student":
            student_details = Student_Details.objects.get(user=request.user.id)
            context["data"] = student_details
        if user_group.name == "Teacher":
            teacher_details = Teacher_Details.objects.get(user=request.user.id)
            context["data"] = teacher_details
        
        return render(request,"viewprofile.html",context)
    else:
        return redirect("signin")


"""
404 Error Page
"""
def page_not_found(request):
    return render(request,"404page/404_err.html")

# End of 404 page

def viewCourses(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        # Most Important for Many To Many Fields 
        for course in courses:
            for university in course.university_affiliation.all():
                print(university.university_url)
        # Not needed Here but One Must Have Concept Of what is happening 
        
        return render(request,'course/course.html',{"courses":courses})
    else:
        return redirect("signin")


def coursedetails(request,id):
    if request.user.is_authenticated:
        subjects = Stu_Subject.objects.all().filter(course_related=id)
        semesters = semester
        # print(semesters)
        subject_field = [f.name for f in Stu_Subject._meta.get_fields()]
        return render(request,'course/coursedetails.html',{"subjects":subjects,"fields":subject_field,"semester":semesters})
    else:
        return redirect("signin")


def subjectdetail(request,id):
    if request.user.is_authenticated:
        subjects = Stu_Subject.objects.all().filter(id=id)
        subject_field = [f.name for f in Stu_Subject._meta.get_fields()]
        for fields in subject_field:
            subject_field.pop(0)
            # subject_field.pop(1)
            if fields == 'id':
                break
        print(subject_field)
        subject_field_dict = {}
        for subject in subjects:
            for field in subject_field:
                if field == "subject_details" or field=="id":
                    continue
                if field == "semester":
                    subject_field_dict["Subject to Study On"] = getattr(subject,field)
                    continue
                if field == "course_related":
                    subject_field_dict["Course"]= getattr(subject,field).course
                    subject_field_dict["university"] = getattr(subject,field).university
                    # subject_field_dict["Subject Enrolled on"] = getattr(subject,field)
                    continue
                else:
                    subject_field_dict[field] = getattr(subject,field)
        # print(subject_field_dict)
        
        return render(request,'course/subjectdetails.html',{"subject_field_dict":subject_field_dict})
    else:
        return redirect("signin")


# Start of View my Teacher View
        
        
def myTeacher(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name == "Student":
                student = Student_Details.objects.all().filter(user=request.user.id)
                for detail in student:
                    sem = detail.semester
                    course = detail.course_enrolled
                    subject = Stu_Subject.objects.all().filter(semester=sem,course_related=course)
                    subjects = []
                    for subjectdetail in subject:
                        subjects.append(subjectdetail.id) 
                    teacher = Teacher_Details.objects.filter(subject_taught__in = subjects).distinct()
                return render(request,"teacherStudent/myTeacher.html",{"teachers":teacher})
            elif group.name == "Admin":
                teacher = Teacher_Details.objects.all()
                return render(request,"teacherStudent/myTeacher.html",{"teachers":teacher})   
            else:
                return redirect("myStudent")
    else:
        return redirect("signin")




#End of View My Teacher View

 
"""
This view first checks the user is authenticated or not. 
then it check if the user who is checking his/her students is a teacher or not?
then after  checking that .
We ensure that the teacher which is logged in right now we fetch that in and check out for the subject that he/she teaches
because 'SUBJECT' has link with 'COURSE' and 'SEMESTER' .. and 'STUDENT' are linked with 'COURSE' and 'SEMESTER' so by this property we can get the 
'STUDENTS' which
are linked with teacher currently logged in.
"""
        
def myStudent(request):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name == "Teacher":
                teacher = Teacher_Details.objects.all().filter(user=request.user.id)
                for teacherdetail in teacher:
                    subject_list = []
                    print(subject_list)
                    semester_list = []
                    for subjects in teacherdetail.subject_taught.all():
                        subject_list.append(subjects.course_related)
                        semester_list.append(subjects.semester)
                    # print(semester_list)
                    # print(subject_list)
                    students = Student_Details.objects.filter(course_enrolled__in = subject_list,semester__in = semester_list).distinct()
                    print(students)
                return render(request,"teacherStudent/myStudent.html",{"students":students})
            elif group.name == "Admin":
                students = Student_Details.objects.all()
                return render(request,"teacherStudent/myStudent.html",{"students":students}) 
            else:
                return redirect("myTeacher")
    else:
        return redirect("signin")

# End of my Student View Function





"""
Function That get triggred when anyone clicks assignment navbar(Any logged user can do it.)
This function returns the template which loads the subject that is been assigned to the teacher and the sudent. 
--> For Student the all the subjects will be shown according to semester they are currently on
--> For Teacher the subjects will be shown according to the subjects that teacher taught irrespective of semester
    -> this is beacause one teacher can teach the subjects that are in cross semester also

"""

def IntoAssignment(request):
    if request.user.is_authenticated:
        subjects = []
        for group in request.user.groups.all():
            if group.name == "Teacher":
                teachers = Teacher_Details.objects.all().filter(user=request.user.id)
                for teacher in teachers:
                    teacher_subject = teacher.subject_taught.all()
                    for subject in teacher_subject:
                        sub = Stu_Subject.objects.all().filter(subject_code=subject)
                        subjects.append(sub)
                        # print(Stu_Subject.objects.all().filter(subject_code=subject))
            
            if group.name == "Student":
                students = Student_Details.objects.all().filter(user=request.user.id)
                for student in students:
                    student_course = student.course_enrolled
                    subject = Stu_Subject.objects.all().filter(course_related=student_course,semester=student.semester)
                    subjects.append(subject)
        print(subjects)
        return render(request,'assignment/assignment.html',{"data_recieved":subjects})
    else:
        return redirect("signin")


"""
Assigning The Assignment To a subject(Done By Teacher's only to their subjects.)
"""
def assigntask(request,id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name == "Teacher":
                subject_name = Stu_Subject.objects.all().filter(id=id)
                
                for subject in subject_name:
                    sub_choosen = subject.id
                    print(sub_choosen)
                teacher_subject = Teacher_Details.objects.all().filter(user=request.user.id)
                for assigned_subject in teacher_subject:
                    teacher_assigned = assigned_subject.subject_taught.all()
                sub = [s.id for s in teacher_assigned]

                if sub_choosen in sub:
                    if request.method=="POST":
                        fm = AssignmentForm(request.POST,request.FILES)
                            
                        if fm.is_valid():
                                
                            data = fm.save(commit=False)
                                # data.name = "Sagar"
                            data.subject = Stu_Subject.objects.get(id=id)
                            data.assigned_by = Teacher_Details.objects.get(user=request.user.id)
                            dat = data.save()
                            messages.success(request,"Assignment Successfully Submitted")
                            return redirect("intoassignment")
                    else:
                        fm = AssignmentForm()
                    return render(request,'assignment/assigntask.html',{"form":fm,"edit":False})
                else:
                    return redirect("intoassignment")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")


"""
Viewing Assignment (Done By both Teacher and Student)
"""
def viewassignment(request,id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name =="Student":
                subject = Stu_Subject.objects.all().filter(id=id)
                subject_name = ""
                subject_course = ""
                semester =  ""
                subject_code = ""
                for subj in subject:
                    subject_name = subj.subject_name
                    subject_course = subj.course_related
                    semester = subj.semester
                    # subject_code = subj.subject_code
                if subject_course != "":
                    student = Student_Details.objects.all().filter(user=request.user.id,semester=semester,course_enrolled=subject_course)
                    myuser = ""
                    for stu in student:
                        myuser = stu.user
                    print(myuser)
                    if myuser!="":
                        assignments = Assignment.objects.all().filter(subject=id)
                        ass_id = 0
                        for ass in assignments:
                            ass_id = ass.id
                        print(ass_id)
                        # print(type(Student_Details.objects.get(user=request.user.id)))
                        submitted_assignments = SubmitAssignment.objects.all().filter(submitted_by=request.user.id,assignment=ass_id)
                        print(submitted_assignments)
                        context = {"subject_name":subject_name,"assignments":assignments,"submitted_assignments":submitted_assignments,"sub_id":id}
                        return render(request,'assignment/viewassignment.html',context)
                    else:
                        return redirect("intoassignment")
                else:
                    return redirect("intoassignment")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")


"""
Editing Assignment(Done By Teacher's only)
assignment -> see prev assigned task -> edit 

"""
def editassignment(request,id):
    if request.user.is_authenticated:
        if Assignment.objects.filter(id=id).exists():
            assignment = Assignment.objects.get(id=id)
            if request.user.username == assignment.assigned_by.user.username:
                if request.method=="POST":
                    fm = AssignmentForm(request.POST,request.FILES,instance=assignment)
                    update_file = request.FILES.get("assigned_data")
                    if fm.is_valid():
                        data = fm.save(commit=False)
                        data.assigned_data = update_file
                        data.save()
                        messages.success(request,f"Assignment {assignment.name} Successfully Edited")
                        return redirect("intoassignment")
                else:
                    fm = AssignmentForm(instance=assignment)
                context = {"form":fm,"edit":True}
                return render(request,'assignment/assigntask.html',context)
            else:
                # return redirect("viewassignment",id)
                return redirect("404error")
        else:
            return redirect("404error")
    else:
        return redirect("signin")

# End of Editing Assignment


"""
Done by Students. on the subjects they have been enrolled.
"""
def submitassignment(request,sub_id,id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name =="Student":
                
                if Stu_Subject.objects.filter(id=sub_id).exists():
                    subject = Stu_Subject.objects.get(id=sub_id)
                    subject_name = subject.subject_name
                    subject_course = subject.course_related
                    semester = subject.semester
                    if Student_Details.objects.filter(user=request.user.id,semester=semester,course_enrolled=subject_course).exists():
                        student = Student_Details.objects.get(user=request.user.id,semester=semester,course_enrolled=subject_course)
                        
                        if Assignment.objects.filter(id=id,subject=sub_id).exists(): 
                            if SubmitAssignment.objects.filter(submitted_by=request.user.id,assignment=id).exists():
                                submisson_exists = SubmitAssignment.objects.get(submitted_by=request.user.id,assignment=id)
                                submission_id = submisson_exists.id
                                return redirect('editsubmission',sub_id,id,submission_id)
                                
                            else:
                                if request.method == "POST":
                                    fm = SubmitAssignmentForm(request.POST,request.FILES)
                                    if fm.is_valid:
                                        data = fm.save(commit=False)
                                        data.submitted_by = User.objects.get(id = request.user.id)
                                        
                                        data.assignment = Assignment.objects.get(id=id)
                                        data.save()
                                        messages.success(request,"Assignment Successfully Submitted")
                                        return redirect("intoassignment")
                                else:
                                    fm = SubmitAssignmentForm()
                                context = {"form":fm,"edit":False}
                                return render(request,'assignment/submitassignment.html',context)
                        else:
                            return redirect("404error")
                    else:
                        return redirect("404error")
                else:
                    return redirect("404error")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")
    



"""
Done by Students. They edit their previous submission
"""
def editsubmission(request,sub_id,id,submission_id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name =="Student":
                
                if Stu_Subject.objects.filter(id=sub_id).exists():
                    subject = Stu_Subject.objects.get(id=sub_id)
                    subject_name = subject.subject_name
                    subject_course = subject.course_related
                    semester = subject.semester
                    if Student_Details.objects.filter(user=request.user.id,semester=semester,course_enrolled=subject_course).exists():
                        student = Student_Details.objects.get(user=request.user.id,semester=semester,course_enrolled=subject_course)
                        
                        if Assignment.objects.filter(id=id,subject=sub_id).exists(): 
                            if not SubmitAssignment.objects.filter(submitted_by=request.user.id,assignment=id).exists():
                                return redirect('submitassignment',sub_id,id)
                                
                            else:
                                assignmentinstance = SubmitAssignment.objects.get(pk=submission_id)
                                if request.method == "POST":
                                    fm = SubmitAssignmentForm(request.FILES,request.POST,instance=assignmentinstance)
                                    updated_data = request.FILES.get("submitted_data")
                                    if fm.is_valid:
                                        data = fm.save(commit=False)
                                        data.submitted_data = updated_data
                                        data.submitted_by = User.objects.get(id = request.user.id)
                                        # data.assignment = Assignment.objects.get(id=assig_id)
                                        data.save()
                                        messages.success(request,"Assignment Successfully Submitted")
                                        return redirect("intoassignment")
                                else:
                                    # print(assignmentinstance.submitted_data)
                                    fm = SubmitAssignmentForm(instance=assignmentinstance)
                                context = {"form":fm,"edit":True}
                                return render(request,'assignment/submitassignment.html',context)
                        else:
                            return redirect("404error")
                    else:
                        return redirect("404error")
                else:
                    return redirect("404error")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")
    




# This will show student and teacher the assignment which were assigned before and submitted assignment and 
# For teacher this view will allow to submit correct answers and see submitted answers .. from students. 
# For Student this view will allow to see the answers that they have submitted and see correct answers.

def prevassignedtask(request,id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name=="Teacher" or group.name=="Student":
                if Stu_Subject.objects.filter(id=id).exists():
                    subjectdetail = Stu_Subject.objects.all().filter(id=id)
                    subject = Stu_Subject.objects.get(id=id).subject_name
                    # For Teacher Entry in assigned Task for Specific Subject
                    if group.name=="Teacher":
                        subcode = []
                        # Filtering out subject id for filtering out teacher
                        for sub in subjectdetail:
                            subcode.append(sub.id)
                        # Filtering out teacher which is logged in and if he/she has gone inside the subject which they are enrolled
                        teacher = Teacher_Details.objects.filter(user=request.user.id,subject_taught__in = subcode)
                        print(teacher)
                        teacher_username = 0
                        # If there is any teacher iterating over it and taking out his/her username to check if they are matching with currently logged user or not
                        for teach in teacher:
                            print(teach.id)
                            teacher_username = teach.id
                        template_name = "assignment/prevassignedassignment.html"
                        data = Assignment.objects.filter(subject=id,assigned_by=teacher_username)
                        context  = {"assignments":data,"subject":subject}
                        return render(request, template_name,context)
                        # else:
                        #     return redirect("intoassignment")
                        
                    # For student Entry in assigned Task for specific subject
                    elif group.name == "Student":
                        subject_course = ""
                        subject_semester = ""
                        # Taking out the subject_course and the semester in which the subject is taught mainly to filter out the student taking that course and semester
                        # Because the students which are enrolled in other courses and other sem. they must not be allowed to see the assignment of 
                        # Subject which they are not enrolled
                        for sub in subjectdetail:
                            subject_course = sub.course_related
                            subject_semester = sub.semester
                        # Checking out student if they are present or not with the same course as subject and sem sem as subject and same user as logged in
                        student = Student_Details.objects.all().filter(user=request.user.id,course_enrolled=subject_course,semester=subject_semester)
                        student_username= "" 
                        
                        for stu in student:
                            student_username = stu.user.username
                        # Checking out filtered username with the logged in username coz if the match we can be sure that the student is enrolled in the course
                        # and he/she is in the sem where that subject is taught
                        if student_username == request.user.username:
                            template_name = "assignment/prevassignedassignment.html"
                            data = Assignment.objects.all().filter(subject=id)
                            # assignment = Assignment.objects.get(subject=id)
                            
                            # my_submission = None
                            # if SubmitAssignment.objects.filter(assignment=assignment.id,submitted_by=request.user.id).exists():
                            #     my_submission = SubmitAssignment.objects.get(assignment=assignment.id,submitted_by=request.user.id)
                            #     print(my_submission.submitted_data.url)
                            
                            # correct_answer = None
                            # if CorrectAnswer.objects.filter(assignment=assignment.id,subject=id).exists():
                            #     correct_answer = CorrectAnswer.objects.get(assignment=assignment.id,subject=id)
                            #     print(correct_answer.correct_answer.url)
                                      
                            context  = {"assignments":data,"subject":subject}
                            return render(request, template_name,context)
                        else:
                            return redirect("intoassignment")
                    else:
                        return redirect("intoassignment")
                else:
                    return redirect("404error")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")




# End of Previous assigned Task


# Previously assigned task details... Student see this function


def prev_assigned_task_detail(request,sub_id,ass_id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name =="Student":
                
                if Stu_Subject.objects.filter(id=sub_id).exists():
                    subject = Stu_Subject.objects.get(id=sub_id)
                    subject_name = subject.subject_name
                    subject_course = subject.course_related
                    semester = subject.semester
                    if Student_Details.objects.filter(user=request.user.id,semester=semester,course_enrolled=subject_course).exists():
                        student = Student_Details.objects.get(user=request.user.id,semester=semester,course_enrolled=subject_course)
                        
                        template_name = "assignment/viewtaskdetails.html"
                        # submission = False
                        submission_data = None
                        correct_data = None
                        assigned_data= None
                        review_on_submission = None
                        if Assignment.objects.filter(id=ass_id,subject=sub_id).exists():
                            assigned_data = Assignment.objects.get(id=ass_id,subject=sub_id)
                            if SubmitAssignment.objects.filter(submitted_by=request.user.id,assignment=ass_id).exists():
                                submission_data = SubmitAssignment.objects.get(submitted_by=request.user.id,assignment=ass_id)

                                if AssignmentCheck.objects.filter(assignment=submission_data.id).exists():
                                    review_on_submission = AssignmentCheck.objects.get(assignment=submission_data.id)
                                
                               
                            else:
                                pass
                            
                            if CorrectAnswer.objects.filter(subject=sub_id,assignment=ass_id).exists():
                                correct_data = CorrectAnswer.objects.get(subject=sub_id,assignment=ass_id)
                                print(correct_data.correct_answer)
                            else:
                                pass
                            
                            context = {
                                        "submission_data":submission_data,
                                        "correct_data":correct_data,"assigned_data":assigned_data,
                                        "review_on_submission":review_on_submission,
                                       }    
                            return render(request,template_name,context)
                        else:
                            return redirect("404error")
                    else:
                        return redirect("404error")
                else:
                    return redirect("404error")
            else:
                return redirect("intoassignment")
    else:
        return redirect("signin")
    



"""
This view will help teacher to see the submission done on the assignment that they have assigned to them

"""

def viewsubmission(request,id):
    if request.user.is_authenticated:
        template_name = "assignment/viewsubmission.html"
        if SubmitAssignment.objects.filter(assignment=id).exists():
            data = SubmitAssignment.objects.all().filter(assignment=id)
            subject = Assignment.objects.get(id=id).name
            assigned_by = Assignment.objects.get(id=id).assigned_by
            print(request.user.username)
            if request.user.username ==  assigned_by.user.username:
                context  = {"assignments":data,"subject":subject}
                return render(request, template_name,context)
            else:
                return redirect("404error")
        else:
            return redirect("404error")
    else:
        return redirect("signin")





"""
This(Check Assignment) view helps teacher to check the assignment assigned by student they can review it. and send feedback. on wrong /right etc.
implementation:
1. checking the user(teacher) is authenticated or not:
2. checking the user belongs to group teache or not. Beacuse students should not be allowed to check the assignment
3. checking the teacher who is currently checking the assignment is enrolled to the subject or not and the assignment is given by them or not
    because the teacher who is not enrolled to the subject and the assignment is not given by him then he/she should not be allowed to check 
    that.
Procedures:
1. First we check user is authenticated or not by using is_authenticated function
2. Then we check user belongs to group or not by taking the group name from manytomany relation that the user have with groups.
3. Then finally the checking for subject is done by using the id taken by the the function checkassignment(). This function takes the id
    of "SubmitAssignment" model. and that model is connected to the "Assignment" model via foreignkey assignment and we take the subject_id from 
    the Assignment model. and check there exists the teacher which is enrolled in subject_id(that subject where the student has submitted assignment.)
4. If there exists we need to check if the teacher currently logged in is that teacher which is enrolled or not.
5. If all these procedures are verified then it will allow teacher to check assignment
"""
def checkassignment(request,ass_id,sub_id):
    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name =="Teacher":
                assig_id = 0 
                
                if Assignment.objects.filter(id=ass_id).exists() and SubmitAssignment.objects.filter(id=sub_id).exists():
                    assignment = Assignment.objects.get(id=ass_id)
                    submission = SubmitAssignment.objects.get(id=sub_id)
                    if assignment.assigned_by.user.username == request.user.username:
                        if not AssignmentCheck.objects.filter(assignment=sub_id,checked_by=request.user.id).exists():
                            if request.method=="POST":
                                fm = AssignmentCheckForm(request.POST)
                                if fm.is_valid():
                                    data = fm.save(commit=False)
                                    data.checked_by = User.objects.get(id=request.user.id)
                                    data.assignment = SubmitAssignment.objects.get(id=sub_id)

                                    data.save()
                                    messages.success(request,"Review Successfully Given")
                                    return redirect("viewsubmission",ass_id)
                            else:
                                fm = AssignmentCheckForm()
                            context = {"form":fm,"edit":False,"submission":submission}
                            return render(request,"assignment/checkassignment.html",context)
                        else:
                            review = AssignmentCheck.objects.get(assignment=sub_id,checked_by=request.user.id)
                            if request.method=="POST":
                                fm = AssignmentCheckForm(request.POST,instance=review)
                                if fm.is_valid():
                                    data = fm.save(commit=False)
                                    data.checked_by = User.objects.get(id=request.user.id)
                                    data.assignment = SubmitAssignment.objects.get(id=sub_id)

                                    data.save()
                                    messages.success(request,"Review Successfully Updated")
                                    
                                    return redirect("viewsubmission",ass_id)
                            else:
                                fm = AssignmentCheckForm(instance=review)
                            context = {"form":fm,"edit":True,"submission":submission}
                            return render(request,"assignment/checkassignment.html",context)
                    else:
                        return redirect("intoassignment")
                else:
                    return redirect("404error")
            else:
                return redirect("404error")
    else:
        return redirect("signin")
        
  
  
  
  
# End of Check Assignment


# Start of Correct answer submission
"""
The Correct answer submission is to be done by teacher.
1. First we need to check if the user is teacher or not:
    a. If User is not teacher the return 404 not found
    b. If User is a teacher then proceed to logic.
        i. First check if the user currently logged in has assigned the given assignment or not.
        ii.  
"""

def CorrectAnswerSubmission(request,sub_id,ass_id):
    if request.user.is_authenticated:
        
        for group in request.user.groups.all():
            if group.name == "Teacher":
                
                if Assignment.objects.filter(id=ass_id).exists():
                    assignment = Assignment.objects.get(id=ass_id)
                    if request.user.username == Assignment.objects.get(id=ass_id).assigned_by.user.username:
                        correct_answers = CorrectAnswer.objects.filter(assignment=ass_id)
                        if correct_answers:
                            correct_answer = CorrectAnswer.objects.get(assignment=ass_id)
                            if request.method=="POST":
                                fm = CorrectAnswerForm(request.POST,request.FILES,instance=correct_answer)
                                updated_data = request.FILES.get("correct_answer")
                                if fm.is_valid():
                                    data = fm.save(commit=False)
                                    data.assignment = assignment
                                    data.subject = Stu_Subject.objects.get(id=sub_id)
                                    data.save()
                                    messages.success(request, "Answer Submission Successfull")
                                    return redirect("intoassignment")
                            else:
                                fm = CorrectAnswerForm(instance=correct_answer)
                            context = {"form":fm}
                            return render(request,'assignment/correctsubmission.html',context)
                            
                        else:
                            if request.method=="POST":
                                fm = CorrectAnswerForm(request.POST,request.FILES)
                                if fm.is_valid():
                                    data = fm.save(commit=False)
                                    data.assignment = assignment
                                    data.subject = Stu_Subject.objects.get(id=sub_id)
                                    data.save()
                                    messages.success(request, "Answer Submission Successfull")
                                    return redirect("intoassignment")
                            else:
                                fm = CorrectAnswerForm()
                            context = {"form":fm}
                            return render(request,'assignment/correctsubmission.html',context)
                    else:
                        return redirect("404error")
                else:
                    return redirect("404error")
            else:
                return redirect("404error")
    else:
        return redirect("signin")
        
    
  
# End of CorrectAnswerSubmission

