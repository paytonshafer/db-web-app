from django.db.models import Min, Max, Avg
from django.shortcuts import render
import mysql.connector

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Dept, Instructor


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
