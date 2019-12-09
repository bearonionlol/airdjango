# from django.shortcuts import render
#
# # Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi, this is where AirPods prices will be compared.")