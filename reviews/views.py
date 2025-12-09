from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Book Review Site 홈 화면!")
