from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages, auth
from django.http import HttpRequest
import sqlite3
from . import dbconnect

# Create your views here.

def IndexView(request):
    if request.method == 'POST':
        if bool(request.POST) == True:
            regfn = request.POST['fname']
            regln = request.POST['lname']
            regun = request.POST['uname']
            regpw = request.POST['pword']
            try:
                dbconnect.insertlogindata(regfn, regln, regun, regpw)
            except sqlite3.IntegrityError:
                messages.add_message(request, messages.INFO, "Email already Registered")
                return redirect(reverse('unbroke:register'))
    elif 'loggedin' in request.session:
        return render(request, 'unbroke/home.html', {'name': request.session['name'],})
    return render(request, 'unbroke/index.html', {})
    
def RegisterView(request):
    return render(request, 'unbroke/register.html', {})
    
def HomeView(request):
    if request.method == 'POST':
        loginuser = request.POST['user']
        loginpass = request.POST['pword']
        if(dbconnect.loginvalid(loginuser, loginpass)):
            getname = dbconnect.getfname(loginuser)
            request.session['loggedin'] = True
            request.session['name'] = getname
            request.session['username'] = loginuser
            request.session.modified = True
            return render(request, 'unbroke/home.html', {'name': request.session['name'], })
        else:
            messages.add_message(request, messages.INFO, "Invalid Username/Password")
            return redirect(reverse('unbroke:index'))
    elif 'loggedin' in request.session:
        return render(request, 'unbroke/home.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))
  
def DepositsView(request):
    if 'loggedin' in request.session:
        if request.method == 'POST':
            pass
        return render(request, 'unbroke/deposits.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))

def ExpensesView(request):
    if 'loggedin' in request.session:
        if request.method == 'POST':
            pass
        return render(request, 'unbroke/expenses.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))
    
def WishView(request):
    if 'loggedin' in request.session:
        if request.method == 'POST':
            pass
        return render(request, 'unbroke/wish.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))
    
def SettingView(request):
    if 'loggedin' in request.session:
        if request.method == 'POST':
            oldpass = request.POST['cpass']
            newpass = request.POST['npass']
            cnewpass = request.POST['cnpass']
            user = request.session['username']
            if (newpass != cnewpass):
                messages.add_message(request, messages.INFO, "Confirmation Password does not match New Password!")
                return render(request, 'unbroke/setting2.html', {'name': request.session['name'],})
            else:
                if (dbconnect.loginvalid(user, oldpass)):
                    dbconnect.passupdate(user, newpass)
                    messages.add_message(request, messages.INFO, "Password has been Updated!")
                else:
                    messages.add_message(request, messages.INFO, "Invalid Current Password!")
                    return render(request, 'unbroke/setting2.html', {'name': request.session['name'],})
        return render(request, 'unbroke/setting.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))

def LogoutView(request):
    if request.method == 'POST':
        messages.add_message(request, messages.INFO, "You have Logged Out!")
        del request.session['loggedin']
        del request.session['name']
        request.session.modified = True
        return render(request, 'unbroke/index.html', {})
    else:
        return redirect(reverse('unbroke:index'))
