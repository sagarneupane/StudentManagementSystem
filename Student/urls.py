from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
    path('login/',views.signin,name="signin"),
    path('register/',views.signup,name="signup"),
    path('signout/',views.signout,name="signout"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/<int:id>',views.editProfile,name="editprofile"),
    path('viewprofile/<int:id>',views.viewProfile,name="viewprofile"),
    path('viewcourse',views.viewCourses,name="viewCourse"),
    path('coursedetails/<int:id>',views.coursedetails,name="coursedetails"),
    path('subjectdetails/<int:id>',views.subjectdetail,name="subjectdetail"),
    path('intoassignment',views.IntoAssignment,name="intoassignment"),
]
