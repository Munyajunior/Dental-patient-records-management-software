import sqlite3
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_db():
    con=sqlite3.connect(database=resource_path(r'PRMS.db'))
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS patient(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,address text,phone text,profession text,dob text,gender text,mc text,observations text,tp text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS treatment(tp_id INTEGER PRIMARY KEY AUTOINCREMENT,tp_name text,tp_code text,tp_price text)")
    con.commit()
 
    cur.execute("CREATE TABLE IF NOT EXISTS appointments(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,phone text,email text,appointment text)")
    con.commit()
 
        
create_db()