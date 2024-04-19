import os
import stat
import sqlite3
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def check_and_modify_permissions(file_path):
    # Check current permissions
    st = os.stat(file_path)
    #print(f"Current permissions: {stat.filemode(st.st_mode)}")

    # Change permissions to 664 (read/write for owner and group, read for others)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)

    # Verify the change
    st = os.stat(file_path)
    #print(f"Updated permissions: {stat.filemode(st.st_mode)}")

def interact_with_database(db_path):
    
    # Connect to the database
    con = sqlite3.connect(database=resource_path(db_path))

    # Create a cursor
    cur = con.cursor()

    # Execute some SQL commands
    cur.execute("CREATE TABLE IF NOT EXISTS patient(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,doctor_name text,address text,phone int,profession text,dob text,gender text,mc text,tooth text,observations varchar,tp text,date varchar)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS treatment(tp_id INTEGER PRIMARY KEY AUTOINCREMENT,tp_name text,tp_code text,tp_price int)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS patientRemind (email text, date text)")
    con.commit()
 
    cur.execute("CREATE TABLE IF NOT EXISTS appointments(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,phone int,email text,appointment text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS schedules (name text, date varchar)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS doctor (doc_id varchar, doc_name text, doc_add varchar, doc_email text, doc_phone int)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS doctor_patient_records (doc_id varchar, doc_name text,pat_name text,intervention text, amount_paid int, date varchar)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS archives(pat_id INTEGER PRIMARY KEY AUTOINCREMENT,name text,doctor_name text,address text,phone int,profession text,dob text,gender text,mc text,tooth text,observations varchar,tp text,date varchar)")
    con.commit()
    # Commit the changes and close the connection
    # Check and modify permissions
    check_and_modify_permissions(db_path)
    
    con.close()

# Usage
#interact_with_database("/path/to/your/database.db")
