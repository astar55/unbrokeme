import sqlite3, hashlib, os, random, psycopg2, urlparse
from datetime import date, timedelta, datetime
import calendar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def getcurrentdate():
    today = date.today()
    return ("%d-%02d-%02d" % ((today.year), (today.month), (today.day)))
    
def insertlogindata(first, last, user, pasd):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    pdigest = passhash(pasd)
    id = str(random.random())
    c.execute('INSERT INTO Users VALUES (?, ?, ?, ?, ?);',
    (id[2:], first, last, user, pdigest))
    conn.commit()
    conn.close()
    
def loginvalid(user, pasd):
    valid = False
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    u = (user, )
    pdigest = passhash(pasd)
    query = c.execute('Select * from Users where Username=?;', u )
    if query.rowcount != 0:
        for row in query:
            if pdigest == row[4]:
                valid = True
    conn.close()
    return valid
    
def getfname(user):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    u = (user, )
    query = c.execute('Select * from Users where Username=?;', u )
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
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    pdigest = passhash(npass)
    c.execute('Update Users Set Password = ? where Username=?;', (pdigest, user))
    conn.commit()
    conn.close()
    
def getbudget(user, year, month):
    budget = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select Savings from Savings Inner Join Users ON Savings.UserID= Users.UserID\
     where Username = ? and substr(Date, 4) = ? and substr(Date, 1, 2) = ? Group By Savings.UserID;', (user, year, month))
    for row in query:
        budget.append(row)
    if len(budget) == 0:
        budget.append('0')
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Group By Deposits.UserID;', (user, year, month))
    for row in query:
        budget.append(row)
    while len(budget) < 2:
        budget.append('0')
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Group By Expenses.UserID;', (user, year, month))
    for row in query:
        budget.append(row)
    while len(budget) < 3:
        budget.append('0')
    conn.close()
    return budget
    
def getdeposits(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Date;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def getexpenses(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Date;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getwishlist(user):
    w = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Wishlist Inner Join Users ON Wishlist.UserID= Users.UserID\
     where Username = ?;', (user,))
    for row in query:
        w.append(row)
    conn.close()
    return w
    
def getdeposits2(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Date Desc;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpenses2(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Date Desc;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdeposits3(user, year, month, desc):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    querystring = 'Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID where Username ="'+user+'" and substr(Date, 1, 4) ="'+year+'" and substr(Date, 6, 2) ="'+month+'"'
    for descrip in desc:
        querystring += ' and Description ="'
        querystring += descrip + '"'   
    querystring += ' Order by Date Desc;'
    query = c.execute(querystring)
    for row in query:
        d.append(row)
    conn.close()
    return d

def getexpenses3(user, year, month, desc):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    querystring = 'Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID where Username ="'+user+'" and substr(Date, 1, 4) ="'+year+'" and substr(Date, 6, 2) ="'+month+'"'
    for descrip in desc:
        querystring += ' and Description ="'
        querystring += descrip + '"'   
    querystring += ' Order by Date Desc;'
    query = c.execute(querystring)
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdeposits4(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Amount;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
   
def getexpenses4(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Amount;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e
   
def getdeposits5(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Amount Desc;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpenses5(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? Order by Amount Desc;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e
    
def getdeposits6(user, year, month, desc):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    querystring = 'Select * from Deposits Inner Join Users ON Deposits.UserID= Users.UserID where Username ="'+user+'" and substr(Date, 1, 4) ="'+year+'" and substr(Date, 6, 2) ="'+month+'"'
    for descrip in desc:
        querystring += ' and Account ="'
        querystring += descrip + '"'   
    querystring += ' Order by Date Desc;'
    query = c.execute(querystring)
    for row in query:
        d.append(row)
    conn.close()
    return d
    
def getexpenses6(user, year, month, desc):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    querystring = 'Select * from Expenses Inner Join Users ON Expenses.UserID= Users.UserID where Username ="'+user+'" and substr(Date, 1, 4) ="'+year+'" and substr(Date, 6, 2) ="'+month+'"'
    for descrip in desc:
        querystring += ' and Account ="'
        querystring += descrip + '"'   
    querystring += ' Order by Date Desc;'
    query = c.execute(querystring)
    for row in query:
        e.append(row)
    conn.close()
    return e
        
def getddescs(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Description from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def getedescs(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Description from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdaccs(user, year, month):
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Account from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        d.append(row)
    conn.close()
    return d

def geteaccs(user, year, month):
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Account from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        e.append(row)
    conn.close()
    return e

def getdtotal(user, year, month):
    total = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        total.append(row)
    conn.close()
    return total[0]

def getdtotal2(userID, year, month):
    total = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Deposits Inner Join Users ON Deposits.UserID= Users.UserID\
     where Deposits.UserID = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (userID, year, month))
    for row in query:
        total.append(row)
    conn.close()
    return total[0]
    
def getetotal(user, year, month):
    total = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Username = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (user, year, month))
    for row in query:
        total.append(row)
    conn.close()
    return total[0]

def getetotal2(userID, year, month):
    total = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select total(Amount) from Expenses Inner Join Users ON Expenses.UserID= Users.UserID\
     where Expenses.UserID = ? and substr(Date, 1, 4) = ? and substr(Date, 6, 2) = ? ;',
    (userID, year, month))
    for row in query:
        total.append(row)
    conn.close()
    return total[0]
    
def getsavings(user, year, month):
    total = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select Savings from Savings Inner Join Users ON Savings.UserID= Users.UserID\
     where Username = ? and substr(Date, 4) = ? and substr(Date, 1, 2) = ? ;',
    (user, year, month))
    for row in query:
        total.append(row)
    conn.close()
    return total
    
def getautoddesc():
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Description from Deposits;')
    for row in query:
        d.append(row)
    conn.close()
    return d

def getautoedesc():
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Description from Expenses;')
    for row in query:
        e.append(row)
    conn.close()
    return e

def getautodacc():
    d = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Account from Deposits')
    for row in query:
        d.append(row)
    conn.close()
    return d

def getautoeacc():
    e = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select distinct Account from Expenses')
    for row in query:
        e.append(row)
    conn.close()
    return e

def insertdeposit(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row  
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], values[4], UserId[0], values[5]))
    conn.commit()
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()

def insertexpense(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row  
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], values[4], UserId[0], values[5]))
    conn.commit()
    upsertsavings(values, UserId)
    conn.commit()
    conn.close()

def insertwish(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    user = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', user)
    for row in query:
        UserId = row
    c = conn.cursor()
    id = str(random.random())
    remaining = float(values[2])-float(values[3])
    c.execute('INSERT INTO Wishlist VALUES (?, ?, ?, ?, ?, ?);',
    (id[2:], values[1], values[2], values[3], remaining , UserId[0]))
    conn.commit()
    conn.close()

def insertdeposit2(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    uname = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', uname)
    for row in query:
        UserId = row  
    date = datetime.strptime(values[1], '%Y-%m-%d').date()
    repeat = timedelta(1);
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))
    conn.commit()
    upsertsavings(values, UserId)            
    if values[6] == "day":
        id = str(random.random())
        date = date + repeat
        c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
        (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))
        datestr = date.isoformat()
        values[1] = datestr
        conn.commit()
        upsertsavings(values, UserId)        
    elif values[6] == "week":
        for i in range(1,7):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))       
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "month":
        for i in range(1, 30):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "semi":
        for i in range(1, 365//2):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "year":
        for i in range(1, 365):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Deposits VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    conn.commit()
    conn.close()
 
def insertexpense2(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    uname = (values[0], )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', uname)
    for row in query:
        UserId = row  
    date = datetime.strptime(values[1], '%Y-%m-%d').date()
    repeat = timedelta(1);
    c = conn.cursor()
    id = str(random.random())
    c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
    (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))
    conn.commit()
    upsertsavings(values, UserId)            
    if values[6] == "day":
        id = str(random.random())
        date = date + repeat
        c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
        (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))
        datestr = date.isoformat()
        values[1] = datestr
        conn.commit()
        upsertsavings(values, UserId)        
    elif values[6] == "week":
        for i in range(1,7):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))       
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "month":
        for i in range(1, 30):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "semi":
        for i in range(1, 365//2):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    elif values[6] == "year":
        for i in range(1, 365):
            id = str(random.random())
            date = date + repeat
            c.execute('INSERT INTO Expenses VALUES (?, ?, ?, ?, ?, ?, ?);',
            (id[2:], date, values[2], values[3], values[4], UserId[0], values[5]))   
            datestr = date.isoformat()
            values[1] = datestr
            conn.commit()
            upsertsavings(values, UserId)        
    conn.commit()
    conn.close()
   
def upsertsavings2(values, UserId):
    SavingsId = [None, ]
    year = values[1][:4]
    month = values[1][5:7]
    date = month+'/'+year
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute("Select SavingsID from Savings where UserID = ? and Date=?", (UserId[0], date))
    for row in query:
        SavingsId = row
    if SavingsId[0] == None:
        id = str(random.random())
        dtotal = getdtotal(values[6], year, month)
        etotal = getetotal(values[6], year, month)
        savings = float(dtotal[0])-float(etotal[0])
        c.execute('Insert Into Savings Values(?, ?, ?, ?, ?, ?)', 
        (id[2:], date, dtotal[0], etotal[0], savings , UserId[0] ))
        conn.commit()
    else:
        dtotal = getdtotal(values[6], year, month)
        etotal = getetotal(values[6], year, month)
        savings = float(dtotal[0])-float(etotal[0])
        c.execute('Update Savings Set Deposit = ?, Expense = ?, Savings= ? where\
        SavingsID = ? and Date= ? and UserID= ?', 
        (dtotal[0], etotal[0], savings, SavingsId[0], date, UserId[0]))
        conn.commit()
    conn.close()

def upsertsavings(values, UserId):
    SavingsId = [None, ]
    year = values[1][:4]
    month = values[1][5:7]
    date = month+'/'+year
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute("Select SavingsID from Savings where UserID = ? and Date=?", (UserId[0], date))
    for row in query:
        SavingsId = row
    if SavingsId[0] == None:
        id = str(random.random())
        dtotal = getdtotal(values[0], year, month)
        etotal = getetotal(values[0], year, month)
        savings = float(dtotal[0])-float(etotal[0])
        c.execute('Insert Into Savings Values(?, ?, ?, ?, ?, ?)', 
        (id[2:], date, dtotal[0], etotal[0], savings , UserId[0] ))
        conn.commit()
    else:
        dtotal = getdtotal(values[0], year, month)
        etotal = getetotal(values[0], year, month)
        savings = float(dtotal[0])-float(etotal[0])
        c.execute('Update Savings Set Deposit = ?, Expense = ?, Savings= ? where\
        SavingsID = ? and Date= ? and UserID= ?', 
        (dtotal[0], etotal[0], savings, SavingsId[0], date, UserId[0]))
        conn.commit()
    conn.close()

def updatedeposit(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    UserId = getuserid(values[6])
    c.execute('Update Deposits SET Date = ?, Description = ?,\
    Amount = ?, Account = ?, Notes = ? where DepositID = ?;',
    (values[1], values[2], values[3], values[4], values[5], values[0]))
    conn.commit()
    upsertsavings2(values, UserId)
    conn.close()
    
def updateexpense(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    UserId = getuserid(values[6])
    c.execute('Update Expenses SET Date = ?, Description = ?,\
    Amount = ?, Account = ?, Notes = ? where ExpensesID = ?;',
    (values[1], values[2], values[3], values[4], values[5], values[0]))
    conn.commit()
    upsertsavings2(values, UserId)
    conn.commit()
    conn.close()
    
def updatewish(values):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    c.execute('Update Wishlist SET Wish = ?, Amount = ?,\
    Saved = ?, Remaining = ? where WishlistID = ?;',
    (values[1], values[2], float(values[3])+float(values[4]),
     float(values[2])-(float(values[3])+float(values[4])), values[0]))
    conn.commit()
    conn.close()
    
def getdepositsentry(Did):
    entry = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits where DepositID = ?;',
    (Did, ))
    for row in query:
        for i in row:
            entry.append(i)
    conn.close()
    return entry[1], entry[2], entry[3], entry[4], entry[6]

def getexpensesentry(Eid):
    entry = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    id = (Eid,)
    query = c.execute('Select * from Expenses where ExpensesID = ?;',
    id)
    for row in query:
        for i in row:
            entry.append(i)
    conn.close()
    return entry[1], entry[2], entry[3], entry[4], entry[6]

def getwishentry(Wid):
    entry = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Wishlist where WishlistID = ?;',
    ((Wid,)))
    for row in query:
        for i in row:
            entry.append(i)
    conn.close()
    return entry[1], entry[2], entry[3], entry[4]

def deletedepositsentry(Did):
    id = Did
    values = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Deposits where DepositID = ?;',
    (id,))
    for row in query:
        for i in row:
            values.append(i)
    c = conn.cursor()
    query = c.execute('Delete from Deposits where DepositID = ?;',
    (Did,))
    conn.commit()
    c = conn.cursor()
    dtotal = getdtotal2(values[5], values[1][:4], values[1][5:7])
    etotal = getetotal2(values[5], values[1][:4], values[1][5:7])
    savings = float(dtotal[0])-float(etotal[0])
    date = values[1][5:7]+'/'+values[1][:4]
    c.execute('Update Savings Set Deposit = ?, Expense = ?, Savings= ? where\
    Date= ? and UserID= ?', (dtotal[0], etotal[0], savings, date, values[5]))
    conn.commit()
    conn.close()

def deleteexpensesentry(Eid):
    id = Eid
    values = []
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select * from Expenses where ExpensesID = ?;',
    (id,))
    for row in query:
        for i in row:
            values.append(i)
    c = conn.cursor()
    query = c.execute('Delete from Expenses where ExpensesID = ?;',
    (Eid,))
    conn.commit()
    c = conn.cursor()
    dtotal = getdtotal2(values[5], values[1][:4], values[1][5:7])
    etotal = getetotal2(values[5], values[1][:4], values[1][5:7])
    savings = float(dtotal[0])-float(etotal[0])
    date = values[1][5:7]+'/'+values[1][:4]
    c.execute('Update Savings Set Deposit = ?, Expense = ?, Savings= ? where\
    Date= ? and UserID= ?', (dtotal[0], etotal[0], savings, date, values[5]))
    conn.commit()
    conn.close()

def deletewishentry(Wid):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Delete from Wishlist where WishlistID = ?;',
    (Wid,))
    conn.commit()
    conn.close()

def getuserid(Username):
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    c = conn.cursor()
    query = c.execute('Select UserID from Users where Username = ?', (Username,))
    for row in query:
        UserId = row  
    return UserId