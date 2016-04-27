import sqlite3, hashlib, os, random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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