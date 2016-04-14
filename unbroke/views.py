from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpRequest
from . import dbconnect

# Create your views here.

def IndexView(request):
    if request.method == 'POST':
        if bool(request.POST) == True:
            regfn = request.POST['fname']
            regln = request.POST['lname']
            regun = request.POST['uname']
            regpw = request.POST['pword']
            dbconnect.insertlogindata(regfn, regln, regun, regpw)
    return render(request, 'unbroke/index.html', {})
    
def RegisterView(request):
    return render(request, 'unbroke/register.html', {})
    
def HomeView(request):
    if request.method == 'POST':
        loginuser = request.POST['user']
        loginpass = request.POST['pword']
        if(dbconnect.loginvalid(loginuser, loginpass)):
            return render(request, 'unbroke/home.html', {'name': dbconnect.getfname(loginuser), })
        else:
            messages.add_message(request, messages.INFO, "Invalid Username/Password")
            return redirect(reverse('unbroke:index'))
    else:
        return redirect(reverse('unbroke:index'))
  