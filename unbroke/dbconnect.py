import sqlite3, hashlib, os, random
from datetime import date, timedelta, datetime
import calendar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def getcurrentdate():
    today = date.today()
    return ("%d-%02d-%d" % ((today.year), (today.month), (today.day)))
    
def insertlogindata(first, last, user, pasd):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    pdigest = passhash(pasd)
    id = str(random.random())
    c.execute('INSERT INTO User VALUES (?, ?, ?, ?, ?);',
    (id[2:], first, last, user, pdigest))
    conn.commit()
    conn.close()
    
def loginvalid(user, pasd):
    valid = False
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    u = (user, )
    pdigest = passhash(pasd)
    query = c.execute('Select * from User where Username=?;', u )
    if query.rowcount != 0:
        for row in query:
            if pdigest == row[4]:
                valid = True
    conn.close()
    return valid
    
def getfname(user):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    u = (user, )
    query = c.execute('Select * from User where Username=?;', u )
    fname = ''
    for row in query:
        fname = row[1]
    conn.close()
    return fname
    
    
def passhash(pasd):
    pdigest = hashlib.sha512()
    pbyte = pasd.encode("utf-8")
    pdigest.update(pbyte)
    return pdigest.digest()
    
def passupdate(user, npass):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    pdigest = passhash(npass)
    c.execute('Update User Set Password = ? where Username=?;', (pdigest, user))
    conn.commit()
    conn.close()
    
def getbudget(user, year, month):
    budget = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select SUM(Amount) from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 7) = ? Group By Deposits.UserID;', (user, year, month))
    for row in query:
        budget.insert(1, row)
    c = conn.cursor()
    query = c.execute('Select Savings from Savings Inner Join User ON Savings.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 7) = ? Group By Savings.UserID;', (user, year, month))
    for row in query:
        budget.insert(0, row)
    conn.close()
    return budget
    
def getdeposits(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Date;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def getexpenses(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Date;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getwishlist(user, year, month):
    w = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Wishlist Inner Join User ON Wishlist.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Date;',
    (user, year, month))
    for row in query:
        w.append(row)
    conn.close()
    return w
    
def getdeposits2(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Date Desc;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpenses2(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Date Desc;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdeposits3(user, year, month, desc):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    querystring = 'Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID where Username ='+user+' and substr(Date, 1, 2) ='+year+' and substr(Date, -4) ='+month
    for descrip in desc:
        querystring += ' and Description ='
        querystring += descrip   
    querystring += ' Order by Date Desc;',
    query = c.execute(querystring)
    for row in query:
        d.append(row)
    conn.close()
    return d

def getexpenses3(user, year, month, desc):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    querystring = 'Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID where Username ='+user+' and substr(Date, 1, 2) ='+year+' and substr(Date, -4) ='+month
    for descrip in desc:
        querystring += ' and Description ='
        querystring += descrip   
    querystring += ' Order by Date Desc;',
    query = c.execute(querystring)
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdeposits4(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Amount;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
   
def getexpenses4(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Amount;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e
   
def getdeposits5(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Amount Desc;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpenses5(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? Order by Amount Desc;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e
    
def getdeposits6(user, year, month, desc):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    querystring = 'Select * from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username ='+user+' and substr(Date, 1, 2) ='+year+' and substr(Date, -4) ='+month
    for descrip in desc:
        querystring += ' and Description ='
        querystring += descrip   
    querystring += ' Order by Date Desc;',
    query = c.execute(querystring)
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpensess6(user, year, month, desc):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    querystring = 'Select * from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username ='+user+' and substr(Date, 1, 2) ='+year+' and substr(Date, -4) ='+month
    for descrip in desc:
        querystring += ' and Description ='
        querystring += descrip   
    querystring += ' Order by Date Desc;',
    query = c.execute(querystring)
    for row in query:
        e.append(row)
    conn.close()
    return e
        
def getddescs(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Description from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def getedescs(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Description from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdaccs(user, year, month):
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Account from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def geteaccs(user, year, month):
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Account from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdtotal(user, year, month):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select Sum(Amount) from Deposits Inner Join User ON Deposits.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        total = row
    conn.close()
    if total[0] == None:
        total = 0
    return total
    
def getetotal(user, year, month):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select Sum(Amount) from Expenses Inner Join User ON Expenses.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        total = row
    conn.close()
    if total[0] == None:
        total = 0
    return total
    
def getsavings(user, year, month):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select Savings from Savings Inner Join User ON Savings.UserID= User.UserID\
     where Username = ? and substr(Date, 1, 2) = ? and substr(Date, -4) = ? ;',
    (user, year, month))
    for row in query:
        total = row
    conn.close()
    if total[0] == None:
        total = 0
    return total
    
def getautoddesc():
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Description from Deposits;')
    for row in query:
        d.append(row)
    conn.close()
    return d

def getautoedesc():
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Description from Expenses;')
    for row in query:
        e.append(row)
    conn.close()
    return e

def getautodacc():
    d = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Account from Deposits')
    for row in query:
        d.append(row)
    conn.close()
    return d

def getautoeacc():
    e = []
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select distinct Account from Expenses')
    for row in query:
        e.append(row)
    conn.close()
    return e

def insertdeposit(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row  
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], values[4], UserId, values[5]))
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()

def insertexpense(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row  
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], values[4], UserId, values[5]))
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()

def insertwish(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row  
    c = conn.cursor()
    id = str(random.random())
    remaining = float(values[2])-float(values[3])
    c.execute('INSERT INTO Wishlist VALUES (?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], remaining , UserId))
    conn.commit()
    conn.close()

def insertdeposit2(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    values[0] = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', values[0])
    for row in query:
        UserId = row  
    date = datetime.strptime(values[1], '%Y-%m-%d').date()
    repeat = timedelta(day=1);
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], date, values[2], values[3], values[4], UserId, values[5]))
    upsertsavings(values, UserId)            
    if values[6] == "day":
        id = str(random.random())
        date = date + repeat
        c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
        (id[2:], date, values[2], values[3], values[4], UserId, values[5]))
        datestr = date.isoformat()
        values[1] = datestr
        upsertsavings(values, UserId)        
    elif values[6] == "week":
        for i in range(1,7):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))       
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "month":
        for i in range(1, 30):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "semi":
        for i in range(1, 365//2):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "year":
        for i in range(1, 365):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    conn.commit()
    conn.close()
 
def insertexpense2(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    values[0] = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', values[0])
    for row in query:
        UserId = row  
    date = datetime.strptime(values[1], '%Y-%m-%d').date()
    repeat = timedelta(day=1);
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], date, values[2], values[3], values[4], UserId, values[5]))
    upsertsavings(values, UserId)            
    if values[6] == "day":
        id = str(random.random())
        date = date + repeat
        c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
        (id[2:], date, values[2], values[3], values[4], UserId, values[5]))
        datestr = date.isoformat()
        values[1] = datestr
        upsertsavings(values, UserId)        
    elif values[6] == "week":
        for i in range(1,7):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))       
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "month":
        for i in range(1, 30):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "semi":
        for i in range(1, 365//2):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    elif values[6] == "year":
        for i in range(1, 365):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId, values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            upsertsavings(values, UserId)        
    conn.commit()
    conn.close()
   
def upsertsavings(values, UserId):
    year = values[1][:4]
    month = values[1][5:7]
    date = month+'/'+year
    c.execute("Select SavingsID from Savings where UserID = ? and Date=?", (UserId, date))
    for row in query:
        SavingsId = row
    if SavingsID == None:
        id = str(random.random())
        dtotal = getdtotal(values[0], year, month)
        etotal = getetotal(values[0], year, month)
        savings = dtotal-etotal
        c.execute('Insert Into Savings Values(?, ?, ?, ?, ?, ?)', 
        (id, date, dtotal, etotal, savings , UserId ))
    else:
        dtotal = getdtotal(values[0], year, month)
        etotal = getetotal(values[0], year, month)
        savings = dtotal-etotal
        c.execute('Insert Into Savings Values(?, ?, ?, ?, ?, ?)', 
        (SavingsId, date, dtotal, etotal, savings, UserId ))

def updatedeposit(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    c.execute('Update Deposits SET Date = ?, Description = ?,\
    Amount = ?, Account = ?, Notes = ? where DepositID = ?;',
    (values[1], values[2], values[3], values[4], values[5], values[0]))
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()
    
def updateexpense(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    c.execute('Update Expenses SET Date = ?, Description = ?,\
    Amount = ?, Account = ?, Notes = ? where ExpenseID = ?;',
    (values[1], values[2], values[3], values[4], values[5], values[0]))
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()
    
def updatewish(values):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    c.execute('Update Wish SET Wish = ?, Amount = ?,\
    Saved = ?, Remaining = ?;',
    (values[1], values[2], values[3], values[0]))
    conn.commit()
    conn.close()
    
def getdepositsentry(Did):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Deposits where DepositID = ?;',
    (Did))
    for row in query:
        entry = row
    conn.close()
    return entry[1], entry[2], entry[3], entry[4], entry[6]

def getexpensesentry(Eid):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Expenses where ExpenseID = ?;',
    (Eid))
    for row in query:
        entry = row
    conn.close()
    return entry[1], entry[2], entry[3], entry[4], entry[6]

def getwishentry(Wid):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Select * from Wishlist where WishlistID = ?;',
    (Wid))
    for row in query:
        entry = row
    conn.close()
    return entry[1], entry[2], entry[3], entry[4]

def deletedepositsentry(Did):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Delete from Deposits where DepositID = ?;',
    (Did))
    conn.commit()
    conn.close()
    return entry

def deleteexpensesentry(Eid):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Delete from Expenses where ExpenseID = ?;',
    (Eid))
    conn.commit()
    conn.close()
    return entry

def deletewishentry(Wid):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    query = c.execute('Delete from Wishlist where WishlistID = ?;',
    (Wid))
    conn.commit()
    conn.close()
    return entry
