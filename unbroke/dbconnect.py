import sqlite3, hashlib, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def insertdata(first, last, user, pasd):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    pdigest = passhash(pasd)
    c.execute('INSERT INTO User VALUES (?, ?, ?, ?)', (first, last, user, pdigest))
    conn.commit()
    conn.close()
    
def loginvalid(user, pasd):
    valid = False
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    u = (user, )
    pdigest = passhash(pasd)
    query = c.execute('Select * from User where Username=?', u )
    if query.rowcount != 0:
        for row in query:
            if pdigest == row[3]:
                valid = True
    return valid
    
def getfname(user):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'unbroke\db.sqlite3'))
    c = conn.cursor()
    u = (user, )
    query = c.execute('Select * from User where Username=?', u )
    fname = ''
    for row in query:
        fname = row[0]
    return fname
    
    
def passhash(pasd):
    pdigest = hashlib.sha512()
    pbyte = pasd.encode("utf-8")
    pdigest.update(pbyte)
    return pdigest.digest()