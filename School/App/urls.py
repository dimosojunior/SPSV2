from django.urls import path
from . import views

#app_name = "polls"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('AllYearsPage/<int:id>/', views.AllYearsPage, name='AllYearsPage'),

    path('AllStudents/<int:id>/', views.AllStudents, name='AllStudents'),
    path('AllClasses/', views.AllClasses, name='AllClasses'),
    path('AllClasses_O_Level/', views.AllClasses_O_Level, name='AllClasses_O_Level'),
    path('search_student_autocomplete/', views.search_student_autocomplete, name='search_student_autocomplete'),

    path('StudentDetailPage/<int:id>/', views.StudentDetailPage, name='StudentDetailPage'),
    path('ReceiveStudentFee/<int:id>/', views.ReceiveStudentFee, name='ReceiveStudentFee'),

    path('ReceiveStudentFee_Semister_01/<int:id>/', views.ReceiveStudentFee_Semister_01, name='ReceiveStudentFee_Semister_01'),
    path('ReceiveStudentFee_Semister_02/<int:id>/', views.ReceiveStudentFee_Semister_02, name='ReceiveStudentFee_Semister_02'),
    path('ReceiveStudentFee_Semister_03/<int:id>/', views.ReceiveStudentFee_Semister_03, name='ReceiveStudentFee_Semister_03'),

    path('AddNewStudent/', views.AddNewStudent, name='AddNewStudent'),
    path('UploadExcellFile/', views.UploadExcellFile, name='UploadExcellFile'),
    path('UpdateStudent/<int:id>/', views.UpdateStudent, name='UpdateStudent'),
    path('DeleteStudent/<int:id>/', views.DeleteStudent, name='DeleteStudent'),

    path('AddNewClass/', views.AddNewClass, name='AddNewClass'),
    path('UpdateClass/<int:id>/', views.UpdateClass, name='UpdateClass'),
    path('DeleteClass/<int:id>/', views.DeleteClass, name='DeleteClass'),

    path('AddNewYear/', views.AddNewYear, name='AddNewYear'),
    path('UpdateYear/<int:id>/', views.UpdateYear, name='UpdateYear'),
    path('DeleteYear/<int:id>/', views.DeleteYear, name='DeleteYear'),


    path('AllPaidStudents/', views.AllPaidStudents, name='AllPaidStudents'),
    path('AllUnPaidStudents/', views.AllUnPaidStudents, name='AllUnPaidStudents'),
        
]
