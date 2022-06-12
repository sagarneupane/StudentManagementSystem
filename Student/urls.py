from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('login/',views.signin,name="signin"),
    path('register/',views.signup,name="signup"),
    path('signout/',views.signout,name="signout"),
    path('profile/',views.profile,name="profile"),
    path('404notFound/',views.page_not_found,name="404error"),
    path('editprofile/<int:id>',views.editProfile,name="editprofile"),
    path('viewprofile/<int:id>',views.viewProfile,name="viewprofile"),
    path('viewcourse',views.viewCourses,name="viewCourse"),
    path('coursedetails/<int:id>',views.coursedetails,name="coursedetails"),
    path('subjectdetails/<int:id>',views.subjectdetail,name="subjectdetail"),
    path('teacherStudent',views.myTeacher,name="myTeacher"),
    path('myStudent',views.myStudent,name="myStudent"),
    path('intoassignment',views.IntoAssignment,name="intoassignment"),
    path('assigntask/<int:id>',views.assigntask,name="assigntask"),
    path('viewassignment/<int:id>',views.viewassignment,name="viewassignment"),
    path('submitassignment/<int:id>',views.submitassignment,name="submitassignment"),
    path('editsubmission/<int:id>',views.editsubmission,name="editsubmission"),
    path('prevassignedtask/<int:id>',views.prevassignedtask,name="prevassignedtask"),
    path('viewsubmission/<int:id>',views.viewsubmission,name="viewsubmission"),
    path('checkassignment/<int:id>',views.checkassignment,name="checkassignment"),
    path('submitanswers/<int:sub_id>/<int:ass_id>',views.CorrectAnswerSubmission,name="submitanswers"),
    # path('readpdf/<str:url>',views.show_pdf,name="readpdf"),
]
