from django.db.models import Min, Max, Avg
from django.shortcuts import render
import mysql.connector

# Create your views here.
from django.http import HttpResponse
from django.template import loader

mydb = mysql.connector.connect(
  host="localhost", 
  user="payton",
  passwd='password',
  auth_plugin='mysql_native_password',
  database="university",
)

#get cursor for database
mycursor = mydb.cursor()

# Create your views here.
def index_student(request):  # Admin
    template = loader.get_template('student/form.html')
    context = {}

    return HttpResponse(template.render(context, request))

def course_offerings(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    #SELECT dept, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = 2019 and semester = 1 order by dept;
    if semester == 'fall':
        sql = 'SELECT dept, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = '  + year + ' and semester = 1 order by dept;'
    else: #semester == 'spring'
        sql = 'SELECT dept, section.course_id, title, sec_id, building, room, credits from section join course on section.course_id = course.course_id where year = '  + year + ' and semester = 2 order by dept;'

    mycursor.execute(sql) #execte sql query on db instance
    data = mycursor.fetchall() #get all results
    
    template = loader.get_template('student/course_offerings.html')
    context = {
        'year': year,
        'sem': semester,
        'rows': data,
    }

    return HttpResponse(template.render(context, request))