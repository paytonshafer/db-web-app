from django.contrib.auth import authenticate
from django.db.models import Min, Max, Avg
from django.shortcuts import redirect, render
import mysql.connector

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Dept, Instructor, Teaches, Takes, ResearchFunds, Published, Student

mydb = mysql.connector.connect(
    host="128.153.13.175",
    port=3306,
    user="group_b",
    passwd='PayJefJosLog',
    auth_plugin='mysql_native_password',
    database="university_group_b",
)

# get cursor for database
mycursor = mydb.cursor()

#student home
def index_student(request): 
    template = loader.get_template('univdb/student/form.html')
    context = {}

    return HttpResponse(template.render(context, request))

#f6
def course_offerings(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    # SELECT dept, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = 2019 and semester = 1 order by dept;
    if semester == 'fall':
        sql = 'SELECT dept_name, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = ' + year + ' and semester = 1 order by dept_name;'
    else:  # semester == 'spring'
        sql = 'SELECT dept_name, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = ' + year + ' and semester = 2 order by dept_name;'

    mycursor.execute(sql)  # execte sql query on db instance
    data = mycursor.fetchall()  # get all results

    template = loader.get_template('univdb/student/course_offerings.html')
    context = {
        'year': year,
        'sem': semester,
        'rows': data,
    }

    return HttpResponse(template.render(context, request))

#handle login routing
def handle_login(request):
    username = request.GET.get('uname')
    password = request.GET.get('psw')

    user = authenticate(username=username, password=password)
    if user is not None:
        group = str(user.groups.all()[0])
        if group == 'admin':
            response = redirect('/univdb/admin')
        if group == 'instructor':
            response = redirect('/univdb/instructor?user=' + username)
        if group == 'student':
            response = redirect('/univdb/student')
    else:
        response = redirect('/univdb/')
        
    return response
        
#login page
def login(request):
    template = loader.get_template('univdb/login.html')
    context = {}

    return HttpResponse(template.render(context, request))

#admin home
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

    # if statement to prevent going out of bounds
    if count_class == 0:
        count_students = 0
    else:
        x = 0
        # establish variable used in for loop
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


# Feature 4

def course_prof(prof_id): # instructor

    # does the SQL selection given the instructor
    sql = 'SELECT teaches.course_id, teaches.sec_id, teaches.semester, teaches.year, COUNT(student_id) FROM teaches INNER JOIN takes on ( takes.course_id = teaches.course_id AND takes.semester = teaches.semester AND takes.sec_id = teaches.sec_id AND takes.year = teaches.year ) WHERE teacher_id = "' + prof_id + '" GROUP BY course_id, sec_id, semester, year;'

    mycursor.execute(sql)  # execute sql query on db instance
    data = mycursor.fetchall()  # get all results

    return data

# Feature 5
def student_list(prof_id): # instructor

    # does the SQL selection given the instructor
    sql = 'SELECT student.name, teaches.semester, teaches.year FROM teaches INNER JOIN takes on (  takes.course_id = teaches.course_id AND takes.semester = teaches.semester AND takes.sec_id = teaches.sec_id AND takes.year = teaches.year) INNER JOIN student on takes.student_id = student.student_id WHERE teacher_id = "' + prof_id + '";'

    mycursor.execute(sql)  # execute sql query on db instance
    data = mycursor.fetchall()  # get all results

    return data

def instructor(request):
    template = loader.get_template('univdb/instructor/home.html')

    user = request.GET.get('user')

    prof_id = Instructor.objects.filter(name = user).values('id').first()
    # transform id into a string
    prof_id = str(prof_id.get('id'))

    f4data = course_prof(prof_id)
    f5data = student_list(prof_id)

    context = {
        'f4data': f4data,
        'f5data': f5data
    }
    return  HttpResponse(template.render(context, request))
