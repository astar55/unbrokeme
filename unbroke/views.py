from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpRequest
from . import dbconnect

# Create your views here.

def IndexView(request):
    return render(request, 'unbroke/index.html', {})
    
def IndexView(request, registering):
    if registering == "true":
        pass
    return render(request, 'unbroke/index.html', {})
    
def RegisterView(request):
    return render(request, 'unbroke/register.html', {})
    
def HomeView(request):
    loginuser = request.POST['user']
    loginpass = request.POST['pword']
    
    return render(request, 'unbroke/home.html', {})