from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.index_student, name='student'),
    path('student/courses', views.course_offerings, name='courses')
]