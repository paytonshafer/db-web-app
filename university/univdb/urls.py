from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views.index_admin, name='index_admin'),
    path('admin/instr_ordered', views.instr_ordered, name='instr_ordered'),
    path('admin/salary_stats', views.salary_stats, name='salary_stats'),
    path('', views.login, name='login'),  # login page
    path('instructor/', views.instructor, name='instructor'),
    path('student/', views.student, name='student'),
]
