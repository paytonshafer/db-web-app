from django.db.models import Min, Max, Avg
from django.shortcuts import render
import mysql.connector

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Dept, Instructor


mydb = mysql.connector.connect(
  host="128.153.13.175", 
  port= 3306,
  user="group_b",
  passwd='PayJefJosLog',
  auth_plugin='mysql_native_password',
  database="university_group_b",
)

#get cursor for database
mycursor = mydb.cursor()

# Create your views here.
def index_student(request):  # Admin
    template = loader.get_template('univdb/student/form.html')
    context = {}

    return HttpResponse(template.render(context, request))

def course_offerings(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    #SELECT dept, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = 2019 and semester = 1 order by dept;
    if semester == 'fall':
        sql = 'SELECT dept_name, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = '  + year + ' and semester = 1 order by dept_name;'
    else: #semester == 'spring'
        sql = 'SELECT dept_name, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = '  + year + ' and semester = 2 order by dept_name;'

    mycursor.execute(sql) #execte sql query on db instance
    data = mycursor.fetchall() #get all results
    
    template = loader.get_template('univdb/student/course_offerings.html')
    context = {
        'year': year,
        'sem': semester,
        'rows': data,
    }

    return HttpResponse(template.render(context, request))

def login(request):
    return HttpResponse("Hello, world.\n")


def instructor(request):
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
