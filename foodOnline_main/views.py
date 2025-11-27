from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    #return HttpResponse('Hello World')
    return render(request, 'home.html') # Create a folder templates and crete home.html in this folder. Later confiugure the template folder in settings.py
