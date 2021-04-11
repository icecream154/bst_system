from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404


def index(request):
    return HttpResponse("Hello, world. You're at the bts index.")
