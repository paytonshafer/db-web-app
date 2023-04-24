from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views.index_admin, name='index_admin'),
    path('admin/instr_ordered', views.instr_ordered, name='instr_ordered'),
    path('admin/salary_stats', views.salary_stats, name='salary_stats'),
    path('admin/professor_performance', views.professor_performance, name='professor_performance'),
    path('', views.login, name='login'),  # login page
    path('handlelogin/', views.handle_login, name='handle_login'),
    path('instructor/', views.instructor, name='instructor'),
    #path('instructor/course_prof', views.course_prof, name='course_prof'),
    #path('instructor/student_list', views.student_list, name='student_list'),
    path('student/', views.index_student, name='student'),
    path('student/courses', views.course_offerings, name='courses'),
]
