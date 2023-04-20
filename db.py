import sqlite3
import os
user_home = os.path.expanduser('~')
user_path="{}\jdsd.db".format(user_home)

def init_db():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS jdsd(id INTEGER PRIMARY KEY,user TEXT,key TEXT,mail TEXT,count INT,day TEXT)")
    cur.execute('INSERT INTO jdsd VALUES (?,?,?,?,?,?)',(1,"","","",0,""))
    con.commit()
    con.close()
def day_insert(today):
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    sql='update jdsd set day=? where id=?'
    data=(today,1)
    cur.execute(sql,data)
    con.commit()
    con.close()
def day_judge():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    day=cur.execute('SELECT day FROM jdsd').fetchall()[0][0]
    con.close()
    return day
def count_increase():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    count=cur.execute('SELECT count FROM jdsd').fetchall()[0][0]+1
    sql='update jdsd set count=? where id=?'
    data=(count,1)
    cur.execute(sql,data)
    con.commit()
    con.close()
def count_judge():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    count=cur.execute('SELECT count FROM jdsd').fetchall()[0][0]
    con.close()
    return count
def key_install(s):
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    sql='update jdsd set judge=? where id=?'
    data=(s,1)
    cur.execute(sql,data)
    # print(cur.execute('SELECT count FROM jdsd').fetchall())
    con.commit()
    con.close()
def key_judge():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    count=cur.execute('SELECT ca FROM jdsd').fetchall()[0][0]
    con.close()
    if count==1:
        return 1
    else: return 0
def mail_insert(mail):
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    sql='update jdsd set mail=? where id=?'
    data=(mail,1)
    cur.execute(sql,data)
    # print(cur.execute('SELECT count FROM jdsd').fetchall())
    con.commit()
    con.close()
def mail_judge():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    mail=cur.execute('SELECT mail FROM jdsd').fetchall()[0][0]
    con.close()
    return mail
def user_key_insert(user,key):
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    sql='update jdsd set user=?,key=? where id=?'
    data=(user,key,1)
    cur.execute(sql,data)
    # print(cur.execute('SELECT count FROM jdsd').fetchall())
    con.commit()
    con.close()
def user_key_judge():
    con=sqlite3.connect(user_path)
    cur=con.cursor()
    user=cur.execute('SELECT user FROM jdsd').fetchall()[0][0]
    key=cur.execute('SELECT key FROM jdsd').fetchall()[0][0]

    con.close()
    return user,key
