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
        if 'user' in request.POST:
            loginuser = request.POST['user']
            loginpass = request.POST['pword']
            if(dbconnect.loginvalid(loginuser, loginpass)):
                getname = dbconnect.getfname(loginuser)
                date = dbconnect.getcurrentdate()
                request.session['loggedin'] = True
                request.session['name'] = getname
                request.session['username'] = loginuser
                request.session['date'] = date
                request.session.modified = True
                user = request.session['username']
                year = date[:4]
                month = date[5:7]            
                return render(request, 'unbroke/home.html', {'name': request.session['name'],
                'balance': dbconnect.getbudget(user, year, month)[0], 'deposits':
                dbconnect.getbudget(user, year, month)[1], 'expenses': 
                dbconnect.getbudget(user, year, month)[2], 'date': date, })
            else:
                messages.add_message(request, messages.INFO, "Invalid Username/Password")
                return redirect(reverse('unbroke:index'))
        elif 'bdate' in request.POST:
            date = request.POST['bdate']
            year = date[:4]
            month = date[5:7]
            user = request.session['username']
            request.session['date'] = date
            request.session.modified = True
            return render(request, 'unbroke/home.html', {'name': request.session['name'],
            'balance': dbconnect.getbudget(user, year, month)[0], 'deposits':
            dbconnect.getbudget(user, year, month)[1], 'expenses': 
            dbconnect.getbudget(user, year, month)[2], 'date': date,})
    elif 'loggedin' in request.session:
        if 'date' in request.session:
            date = request.session['date']
            year = date[:4]
            month = date[5:7]
            user = request.session['username']
            return render(request, 'unbroke/home.html', {'name': request.session['name'],
            'balance': dbconnect.getbudget(user, year, month)[0], 'deposits':
            dbconnect.getbudget(user, year, month)[1], 'expenses': 
            dbconnect.getbudget(user, year, month)[2], 'date': date,})
        return render(request, 'unbroke/home.html', {'name': request.session['name'],})
    return redirect(reverse('unbroke:index'))
  
def DepositsView(request):
    if 'loggedin' in request.session:
        date = request.session['date']
        year = date[:4]
        month = date[5:7]
        user = request.session['username']
        if request.method == 'POST':
            if 'bdate' in request.POST:
                date = request.POST['bdate']
                year = date[:4]
                month = date[5:7]
                user = request.session['username']
                request.session['date'] = date
                request.session.modified = True
                return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'depositsdata': dbconnect.getdeposits(user, year, month)},
                )
            elif 'dsort' in request.POST:
                if request.POST['dsort'] == "Descending":
                    return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getddescs(user, year, month),
                    'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                    'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                    'depositsdata': dbconnect.getdeposits2(user, year, month)}
                    )
            elif 'asort' in request.POST:
                if request.POST['asort'] == "Descending":
                    return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getddescs(user, year, month),
                    'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                    'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                    'depositsdata': dbconnect.getdeposits5(user, year, month)}
                    )
                elif request.POST['asort'] == "Ascending":
                    return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getddescs(user, year, month),
                    'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                    'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                    'depositsdata': dbconnect.getdeposits4(user, year, month)}
                    )
            elif 'desc' in request.POST:
                desc = request.POST['desc']
                return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'depositsdata': dbconnect.getdeposits3(user, year, month, desc)}
                )
            elif 'acc' in request.POST:
                acc = request.POST['acc']
                return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'depositsdata': dbconnect.getdeposits6(user, year, month, desc)}
                )
            elif 'ddate' in request.POST:
                if 'recurring' in request.POST:
                    date = request.POST['ddate']
                    desc = request.POST['ddesc']
                    amt = request.POST['damt']
                    acc = request.POST['dacc']
                    note = request.POST['anotes']
                    repeat = request.POST['repeat']
                    dbconnect.insertdeposit2([user, date, desc, amt, acc, note, repeat])
                    messages.add_message(request, messages.INFO, "Entry Inserted!")
                    return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getddescs(user, year, month),
                    'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                    'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                    'depositsdata': dbconnect.getdeposits(user, year, month)})
                else:
                    date = request.POST['ddate']
                    desc = request.POST['ddesc']
                    amt = request.POST['damt']
                    acc = request.POST['dacc']
                    note = request.POST['anotes']
                    dbconnect.insertdeposit([user, date, desc, amt, acc, note])
                    messages.add_message(request, messages.INFO, "Entry Inserted!")
                    return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getddescs(user, year, month),
                    'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                    'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                    'depositsdata': dbconnect.getdeposits(user, year, month)})
            elif 'eddate' in request.POST:
                date = request.POST['eddate']
                desc = request.POST['eddesc']
                amt = request.POST['edamt']
                acc = request.POST['edacc']
                note = request.POST['enotes']
                dID = request.POST['did']                  
                dbconnect.updatedeposit([dID, date, desc, amt, acc, note, user])
                messages.add_message(request, messages.INFO, "Entry Updated!")
                return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'depositsdata': dbconnect.getdeposits(user, year, month)})           
            elif 'dID' in request.POST:
                Did = request.POST['dID']
                return render(request, 'unbroke/deposits2.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'dID': Did, 'entry': dbconnect.getdepositsentry(Did),
                'depositsdata': dbconnect.getdeposits(user, year, month)})           
            elif 'ddelete' in request.POST:
                Did= request.POST['ddelete']
                dbconnect.deletedepositsentry(Did)
                messages.add_message(request, messages.INFO, "Entry Deleted!")
                return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getddescs(user, year, month),
                'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
                'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
                'depositsdata': dbconnect.getdeposits(user, year, month)})           
        return render(request, 'unbroke/deposits.html', {'name': request.session['name'],
        'date': date, 'desc': dbconnect.getddescs(user, year, month),
        'autodesc': dbconnect.getautoddesc(), 'autoacc': dbconnect.getautodacc(),
        'acc': dbconnect.getdaccs(user, year, month), 'total': dbconnect.getdtotal(user, year, month),
        'depositsdata': dbconnect.getdeposits(user, year, month)})
    return redirect(reverse('unbroke:index'))

def ExpensesView(request):
    if 'loggedin' in request.session:
        date = request.session['date']
        year = date[:4]
        month = date[5:7]
        user = request.session['username']
        if request.method == 'POST':
            if 'bdate' in request.POST:
                date = request.POST['bdate']
                year = date[:4]
                month = date[5:7]
                user = request.session['username']
                request.session['date'] = date
                request.session.modified = True
                return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'expensesdata': dbconnect.getexpenses(user, year, month)},
                )
            elif 'dsort' in request.POST:
                if request.POST['dsort'] == "Descending":
                    return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getedescs(user, year, month),
                    'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                    'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                    'expensesdata': dbconnect.getexpenses2(user, year, month)}
                    )
            elif 'asort' in request.POST:
                if request.POST['asort'] == "Descending":
                    return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getedescs(user, year, month),
                    'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                    'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                    'expensesdata': dbconnect.getexpenses5(user, year, month)}
                    )
                elif request.POST['asort'] == "Ascending":
                    return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getedescs(user, year, month),
                    'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                    'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                    'expensesdata': dbconnect.getexpenses4(user, year, month)}
                    )
            elif 'desc' in request.POST:
                desc = request.POST['desc']
                return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'expensesdata': dbconnect.getexpenses3(user, year, month, desc)}
                )
            elif 'acc' in request.POST:
                acc = request.POST['acc']
                return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'expensesdata': dbconnect.getexpenses6(user, year, month, desc)}
                )
            elif 'ddate' in request.POST:
                if 'recurring' in request.POST:
                    date = request.POST['ddate']
                    desc = request.POST['ddesc']
                    amt = request.POST['damt']
                    acc = request.POST['dacc']
                    note = request.POST['anotes']
                    repeat = request.POST['repeat']
                    dbconnect.insertexpense2([user, date, desc, amt, acc, note, repeat])
                    messages.add_message(request, messages.INFO, "Entry Inserted!")
                    return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getedescs(user, year, month),
                    'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                    'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                    'expensesdata': dbconnect.getexpenses(user, year, month)})
                else:
                    date = request.POST['ddate']
                    desc = request.POST['ddesc']
                    amt = request.POST['damt']
                    acc = request.POST['dacc']
                    note = request.POST['anotes']
                    dbconnect.insertexpense([user, date, desc, amt, acc, note])
                    messages.add_message(request, messages.INFO, "Entry Inserted!")
                    return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                    'date': date, 'desc': dbconnect.getedescs(user, year, month),
                    'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                    'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                    'expensesdata': dbconnect.getexpenses(user, year, month)})
            elif 'eddate' in request.POST:
                date = request.POST['eddate']
                desc = request.POST['eddesc']
                amt = request.POST['edamt']
                acc = request.POST['edacc']
                note = request.POST['enotes']
                eID = request.POST['eid']                  
                dbconnect.updateexpense([eID, date, desc, amt, acc, note, user])
                messages.add_message(request, messages.INFO, "Entry Updated!")
                return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'expensesdata': dbconnect.getexpenses(user, year, month)})           
            elif 'eID' in request.POST:
                Eid = request.POST['eID']
                return render(request, 'unbroke/expenses2.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'eID': Eid, 'entry': dbconnect.getexpensesentry(Eid),
                'expensesdata': dbconnect.getexpenses(user, year, month)})           
            elif 'ddelete' in request.POST:
                Eid= request.POST['ddelete']
                dbconnect.deleteexpensesentry(Eid)
                messages.add_message(request, messages.INFO, "Entry Deleted!")
                return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
                'date': date, 'desc': dbconnect.getedescs(user, year, month),
                'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
                'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
                'expensesdata': dbconnect.getexpenses(user, year, month)})           
        return render(request, 'unbroke/expenses.html', {'name': request.session['name'],
        'date': date, 'desc': dbconnect.getedescs(user, year, month),
        'autodesc': dbconnect.getautoedesc(), 'autoacc': dbconnect.getautoeacc(),
        'acc': dbconnect.geteaccs(user, year, month), 'total': dbconnect.getetotal(user, year, month),
        'expensesdata': dbconnect.getexpenses(user, year, month)})
    return redirect(reverse('unbroke:index'))
    
def WishView(request):
    if 'loggedin' in request.session:
        user = request.session['username']
        date = request.session['date']
        year = date[:4]
        month = date[5:7]
        if request.method == 'POST':
            if "wID" in request.POST:
                WId = request.POST['wID']                
                return render(request, 'unbroke/wish2.html', {'name': request.session['name'],
                'date': date, 'total': dbconnect.getsavings(user, year, month),
                'wID': WId, 'entry': dbconnect.getwishentry(WId),
                'wishdata': dbconnect.getwishlist(user),})
            elif "dwish" in request.POST:
                wish = request.POST['dwish']
                amt = request.POST['damt']
                saved = request.POST['dsaved']
                dbconnect.insertwish([user, wish, amt, saved])
                messages.add_message(request, messages.INFO, "Entry Inserted!")
                return render(request, 'unbroke/wish.html', {'name': request.session['name'],
                'date': date, 'total': dbconnect.getsavings(user, year, month),
                'wishdata': dbconnect.getwishlist(user),})
            elif 'edwish' in request.POST:
                wish = request.POST['edwish']
                amt = request.POST['edamt']
                saved = request.POST['edsaved']
                save = request.POST['edsave']
                wID = request.POST['wid']
                if float(save) < (0-float(saved)):
                    messages.add_message(request, messages.INFO, "Amount to Save cannot exceed Saved Amount!")
                    return render(request, 'unbroke/wish2.html', {'name': request.session['name'],
                    'date': date, 'total': dbconnect.getsavings(user, year, month),
                    'wID': wID, 'entry': dbconnect.getwishentry(wID),
                    'wishdata': dbconnect.getwishlist(user),})
                else:
                    dbconnect.updatewish([wID, wish, amt, saved, save])
                    messages.add_message(request, messages.INFO, "Entry Updated!")
                    return render(request, 'unbroke/wish.html', {'name': request.session['name'],
                    'date': date, 'total': dbconnect.getsavings(user, year, month),
                    'wishdata': dbconnect.getwishlist(user),})
            elif 'ddelete' in request.POST:
                wID = request.POST['ddelete']
                dbconnect.deletewishentry(wID)
                messages.add_message(request, messages.INFO, "Entry Deleted!")
                return render(request, 'unbroke/wish.html', {'name': request.session['name'],
                'date': date, 'total': dbconnect.getsavings(user, year, month),
                'wishdata': dbconnect.getwishlist(user),})
        return render(request, 'unbroke/wish.html', {'name': request.session['name'],
        'date': date, 'total': dbconnect.getsavings(user, year, month),
        'wishdata': dbconnect.getwishlist(user),})
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
        del request.session['date']
        request.session.modified = True
        return render(request, 'unbroke/index.html', {})
    else:
        return redirect(reverse('unbroke:index'))
