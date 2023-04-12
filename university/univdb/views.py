from django.db.models import Min, Max, Avg
from django.shortcuts import render
import mysql.connector

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Dept, Instructor, Teaches, Takes, ResearchFunds, Published


def login(request):
    return HttpResponse("Hello, world.\n")


def instructor(request):
    return HttpResponse("Hello, world.\n")


def student(request):
    return HttpResponse("Hello, world.\n")


def index_admin(request):  # Admin
    template = loader.get_template('univdb/admin/form.html')
    context = {}

    return HttpResponse(template.render(context, request))


# Feature 1
def instr_ordered(request):  # Admin
    sort_by = request.GET.get('sort_by', 'name')  # Get the sorting criteria from the request, default to 'name'

    if sort_by == 'dept':
        data = Instructor.objects.all().order_by('dept_name')
    elif sort_by == 'salary':
        data = Instructor.objects.all().order_by('salary')
    else:  # default to sorting by name
        data = Instructor.objects.all().order_by('name')

    template = loader.get_template('univdb/admin/instr_ordered.html')
    context = {
        'rows': data,
    }

    return HttpResponse(template.render(context, request))


# Feature 2
def salary_stats(request):  # Admin
    data = Dept.objects.annotate(
        min_salary=Min('instructor__salary'),
        max_salary=Max('instructor__salary'),
        avg_salary=Avg('instructor__salary'),
    )

    template = loader.get_template('univdb/admin/salary_stats.html')
    context = {
        'rows': data,
    }
    return HttpResponse(template.render(context, request))


def professor_performance(request):  # Admin
    prof_name = request.GET.get('Name', '')
    yr = request.GET.get('Year', '')
    sem = request.GET.get('Semester', '')

    prof_id = Instructor.objects.filter(name=prof_name)
    prof_id = prof_id.values('id')[0]['id']  # gets id of professor entered

    if sem == '' and yr == '':  # if semester and year options are not entered
        prof_course_data = Teaches.objects.filter(teacher_id=prof_id)
    elif sem == '':  # if only semester is left blank
        prof_course_data = Teaches.objects.filter(teacher_id=prof_id, year=yr)
    elif yr == '':  # if only year is left blank
        prof_course_data = Teaches.objects.filter(teacher_id=prof_id, semester=sem)
    else:  # if all data is entered
        prof_course_data = Teaches.objects.filter(teacher_id=prof_id, semester=sem, year=yr)

    # sum of courses professor teaches
    count_class = len(prof_course_data)

    # establish variable used in for loop
    x = 0
    prof_courses = prof_course_data.values()[x]
    student_course_data = (Takes.objects.filter(
        course_id=prof_courses['course_id'],
        semester=prof_courses['semester'],
        year=prof_courses['year'])
    )

    # retrieve all students taking professor's courses
    for i in prof_course_data:
        x = x + 1
        if x < count_class:
            prof_courses = prof_course_data.values()[x]
            student_course_data = student_course_data | (Takes.objects.filter(
                course_id=prof_courses['course_id'],
                semester=prof_courses['semester'],
                year=prof_courses['year'])
            )

    # sum of students professor teaches
    count_students = len(student_course_data)

    # retrieves sum of funds for all professor's research
    y = 0
    prof_funds = 0
    prof_funds_data = ResearchFunds.objects.filter(id=prof_id)
    for f in prof_funds_data:
        prof_funds = prof_funds + prof_funds_data.values('funds')[y]['funds']
        y = y + 1

    # retrieves number of research papers published
    z = 0
    prof_published = 0
    prof_published_data = Published.objects.filter(id=prof_id)
    for p in prof_published_data:
        prof_published = prof_published + prof_published_data.values('published')[z]['published']
        z = z + 1

    template = loader.get_template('univdb/admin/professor_performance.html')
    context = {
        'Name': prof_name,
        'NumCourses': count_class,
        'NumStudents': count_students,
        'TotFunds': prof_funds,
        'TotPublished': prof_published,
    }
    return HttpResponse(template.render(context, request))
