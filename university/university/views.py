from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    response = redirect('/univdb/')
    return response