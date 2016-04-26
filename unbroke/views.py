from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages, auth
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
            try:
                dbconnect.insertlogindata(regfn, regln, regun, regpw)
            except IntegrityError:
                messages.add_message(request, messages.INFO, "Username already Taken")
                return redirect(reverse('unbroke:index'))
    elif 'loggedin' in request.session:
        return render(request, 'unbroke/home.html', {'name': request.session['name']})
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
            request.session.modified = True
            return render(request, 'unbroke/home.html', {'name': getname, })
        else:
            messages.add_message(request, messages.INFO, "Invalid Username/Password")
            return redirect(reverse('unbroke:index'))
    elif 'loggedin' in request.session:
        return render(request, 'unbroke/home.html', {'name': request.session['name']})
    return redirect(reverse('unbroke:index'))
  
def DepositsView(request):
    if 'loggedin' in request.session:
        return render(request, 'unbroke/deposits.html', {})
    return redirect(reverse('unbroke:index'))

def ExpensesView(request):
    if 'loggedin' in request.session:
        return render(request, 'unbroke/expenses.html', {})
    return redirect(reverse('unbroke:index'))
    
def WishView(request):
    if 'loggedin' in request.session:
        return render(request, 'unbroke/wish.html', {})
    return redirect(reverse('unbroke:index'))
    
def SettingView(request):
    if 'loggedin' in request.session:
        return render(request, 'unbroke/setting.html', {})
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
