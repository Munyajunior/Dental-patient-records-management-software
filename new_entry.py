from tkinter import*
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
import time
from datetime import datetime
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import win32print
import win32api
import os
import permission
from plyer import notification
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class PlaceholderEntry(ctk.CTkEntry):
    def __init__(self, master=None, placeholder_text="PLACEHOLDER", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder_text

    def get(self):
        # If the Entry is empty, return the placeholder
        if super().get() == "":
            return self.placeholder
        else:
            return super().get()




class entryClass(ctk.CTk):
    def __init__(self,root):
        self.root=root
        self.root.state('zoomed')
        # Bind the exit method to the window's close button
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        screen_width=self.root.winfo_screenwidth()
        screen_height=self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}')
        self.root.iconbitmap(resource_path('icon.ico'))
        self.root.title("SmileScribePro")
        self.con = sqlite3.connect(database=os.path.join(os.getcwd(),resource_path(r'PRMS.db')))
        self.cur = self.con.cursor()
        permission.interact_with_database((resource_path('PRMS.db')))
        #=============All Variables=======
        self.var_searchtxt=ctk.StringVar()        
        
        self.var_pat_id=ctk.StringVar()
        self.var_name=ctk.StringVar()
        self.var_address=ctk.StringVar()
        self.var_phone=ctk.StringVar()
        self.var_prof=ctk.StringVar()
        self.var_dob=ctk.StringVar()
        self.var_gender=ctk.StringVar()
        self.var_mc=ctk.StringVar()
        self.var_tp=ctk.StringVar()
        self.var_tooth=ctk.StringVar()
        self.var_doctor=ctk.StringVar()
        
       
        self.tp_list=[]
        self.doc_list=[]
        self.fetch_tp()
        self.fetch_doctor()
               
        #============================Title======================
        self.icon_title=ctk.CTkImage(dark_image=Image.open(resource_path("images\\logo.png")),
                                    light_image=Image.open(resource_path("images\\logo.png")),size=(50,50))
        title = ctk.CTkLabel(
        self.root,
        text="SmileScribePro",
        image=self.icon_title,
        compound=LEFT,
        font=("sans-serif", 40, "bold"),
        fg_color=("#3498db","#fff"),
        text_color=("#fff","#3498db"),
        anchor='w',
        width=screen_width,  # Set the width to be the screen width
        height=68,padx=20
    ).place(anchor='nw', x=0, y=0)
        #=============Btn_Logout================================
        # Calculate the position of the button based on the screen size
        x_position = screen_width - 100  # Adjust this value as needed
        y_position = screen_height - 735  # Adjust this value as needed
        btn_logout = ctk.CTkButton(self.root,text="Exit"
                                    ,command=self.exit
                                    ,font=("calibri",20,"bold")
                                    ,fg_color=("#273c75","#353b48")
                                    ,hover_color="#e84118"
                                    ,height=50,width=140
                                    ,corner_radius=0
                                    ).place(anchor='e', x=x_position, y=30)
        #======================Clock============================
        self.lbl_clock=ctk.CTkLabel(self.root,text="Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS"
                                    ,font=("calibri",18,"bold")
                                    ,fg_color=("#487eb0","#4d636d"),bg_color="#fff"
                                    ,width=screen_width
                                    ,text_color="#fff")
        self.lbl_clock.place(x=0,y=65)

        
        #===================title=========
        title=ctk.CTkLabel(self.root,text="PATIENT DETAILS",font=("goudy old style",20,"bold"),fg_color="#0f4d7d",text_color="#fff",width=1000).place(x=170,y=100)
       
        #================search Frame=============
        #==========search==============
        lbl_serach=ctk.CTkLabel(self.root,text="Search Patient",font=("calibri",17,"bold")).place(x=400,y=150)
        txt_search=ctk.CTkEntry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),fg_color="lightyellow").place(x=540,y=150)
        btn_search=ctk.CTkButton(self.root,command=self.search,text="Search",font=("goudy old style",18,"bold"),fg_color="#4caf50",width=150,height=30).place(x=700,y=150)
        
        #===============content=====================
        self.current_date=datetime.now().strftime("%d.%m.%Y")
        lbl_date=ctk.CTkLabel(self.root,text="Date",font=("goudy old style",17)).place(x=50,y=190)
        self.txt_date = PlaceholderEntry(self.root, placeholder_text=self.current_date, font=("goudy old style",15,"bold"), fg_color="lightyellow", width=180)
        self.txt_date.place(x=100, y=190)
        #============row1=============
        lbl_name=ctk.CTkLabel(self.root,text="Full Name",font=("goudy old style",17)).place(x=50,y=240)
        lbl_address=ctk.CTkLabel(self.root,text="Address",font=("goudy old style",17)).place(x=360,y=240)
        lbl_phone=ctk.CTkLabel(self.root,text="Phone No.",font=("goudy old style",17)).place(x=660,y=240)
             
        txt_name=ctk.CTkEntry(self.root,textvariable=self.var_name,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=150,y=240)
        txt_address=ctk.CTkEntry(self.root,textvariable=self.var_address,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=460,y=240)
        txt_phone=ctk.CTkEntry(self.root,textvariable=self.var_phone,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=760,y=240)
       
        #===================row2=================
         
        lbl_prof=ctk.CTkLabel(self.root,text="Profession",font=("goudy old style",17)).place(x=50,y=290)
        lbl_dob=ctk.CTkLabel(self.root,text="Age",font=("goudy old style",17)).place(x=360,y=290)
        lbl_gender=ctk.CTkLabel(self.root,text="Gender",font=("goudy old style",17)).place(x=660,y=290)
        
        txt_prof=ctk.CTkEntry(self.root,textvariable=self.var_prof,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=150,y=290)
        txt_dob=ctk.CTkEntry(self.root,textvariable=self.var_dob,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=410,y=290)
        self.cmb_gender = ctk.CTkComboBox(self.root, values=("Select", "Male", "Female"),fg_color="lightyellow", state='readonly', justify=CENTER, font=("calibri",15), width=180)
        self.cmb_gender.set("Select")
        self.cmb_gender.place(x=760, y=290)
        #===================row3=================
        
        lbl_mc=ctk.CTkLabel(self.root,text="Main Complain",font=("goudy old style",17)).place(x=50,y=340)
        lbl_doctor=ctk.CTkLabel(self.root,text="Doctor",font=("goudy old style",17)).place(x=360,y=340)
        
        txt_mc=ctk.CTkEntry(self.root,textvariable=self.var_mc,font=("goudy old style",15),fg_color="lightyellow",width=180).place(x=170,y=340)
        btn_doctor=ctk.CTkButton(self.root,text="Select",font=("goudy old style",12,"bold"),command=self.show_doctor_listbox,corner_radius=0,fg_color="#2ecc71", hover_color="#f1c40f",width=110)
        btn_doctor.place(x=450,y=340)
        self.lsb_doc = tk.Listbox(self.root, selectmode="multiple", exportselection=0)
        self.lsb_doc.place(x=-500, y=-500)  # Place the listbox outside the visible area
        self.lsb_doc.bind("<<ListboxSelect>>", self.update_doc_combobox)

        for value in self.doc_list:
            self.lsb_doc.insert(tk.END, value)
            
        lbl_tooth=ctk.CTkLabel(self.root,text="Tooth",font=("goudy old style",17)).place(x=660,y=340)
        self.tooth_type = ttk.Combobox(self.root,textvariable=self.var_tooth,values=["Select","Primary","Permanent"],state='readonly', justify=CENTER)
        self.tooth_type.set(["Select"])
        self.tooth_type.bind("<<ComboboxSelected>>", self.on_tooth_type_selected)
        self.tooth_type.place(x=760,y=340,width=200)

        self.tooth_selection = tk.Listbox(self.root,selectmode="multiple",exportselection=0, state='disabled')  # Initially disable the listbox
        self.tooth_selection.bind("<<ListboxSelect>>", self.on_tooth_selected)  # Bind the selection event
        self.tooth_selection.place(x=960,y=300,height=100)

                
        
        
        #===================row4=================
        
        lbl_obs=ctk.CTkLabel(self.root,text="Observations",font=("goudy old style",17)).place(x=50,y=380)
        lbl_tp=ctk.CTkLabel(self.root,text="Intervention",font=("goudy old style",17)).place(x=500,y=380)
        
        self.txt_obs = ctk.CTkTextbox(self.root, font=("goudy old style", 15), fg_color="lightyellow", width=300, height=60,border_width=1)
        self.txt_obs.place(x=170,y=380)

        self.btn_tp = ctk.CTkButton(self.root, text="Select", command=self.show_listbox,font=("arial",12,"bold"),corner_radius=0, hover_color="#f1c40f",width=110)
        self.btn_tp.place(x=620,y=380)

        self.lsb_tp = tk.Listbox(self.root, selectmode="multiple", exportselection=0)
        self.lsb_tp.place(x=-500, y=-500)  # Place the listbox outside the visible area
        self.lsb_tp.bind("<<ListboxSelect>>", self.update_combobox)

        for value in self.tp_list:
            self.lsb_tp.insert(tk.END, value)
    
       
        
        #=============Buttons============
        btn_add=ctk.CTkButton(self.root,text="NEW_ENTRY",command=self.append_entry,font=("arial",15),fg_color="#2196f3",width=130,height=28).place(x=800,y=420)
        btn_save=ctk.CTkButton(self.root,text="SAVE_NEW_REC",command=self.other,font=("arial",15),fg_color="#6ab04c",width=110,height=28).place(x=980,y=420)
        #=====================Patient Details============
        pat_frame=ctk.CTkFrame(self.root)
        pat_frame.place(x=10,y=470)
        
        scolly=Scrollbar(pat_frame,orient=VERTICAL)
        scollx=Scrollbar(pat_frame,orient=HORIZONTAL)
        
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))
              
        self.PatientTable=ttk.Treeview(pat_frame,columns=("pat_id","name","doctor_name","address","phone","profession","dob","gender","mc","tooth","observations","tp","date"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.PatientTable.xview)
        scolly.config(command=self.PatientTable.yview)
        
        columns = {"pat_id":"PAT_ID","name":"PAT_NAME","doctor_name":"DOC_NAME","address":"ADDRESS","phone":"PHONE","profession":"PROFESSION","dob":"DATE OF BIRTH","gender":"GENDER","mc":"MAIN COMPLAIN","tooth":"TOOTH","observations":"OBSERVATIONS","tp":"TREATMENT PLAN","date":"DATE"}
        for k,v in columns.items():
            self.PatientTable.heading(k,text=v, command=lambda _col=k: treeview_sort_column(self.PatientTable,_col,False))
            
        self.PatientTable["show"] ="headings" 
        self.PatientTable.column("pat_id",width=50)
        self.PatientTable.column("name",width=100)
        self.PatientTable.column("doctor_name",width=100)
        self.PatientTable.column("address",width=100)
        self.PatientTable.column("phone",width=100)
        self.PatientTable.column("profession",width=100)
        self.PatientTable.column("dob",width=100)
        self.PatientTable.column("gender",width=60)
        self.PatientTable.column("mc",width=130)
        self.PatientTable.column("tooth",width=100)
        self.PatientTable.column("observations",width=150)
        self.PatientTable.column("tp",width=150)
        self.PatientTable.column("date",width=100)
        self.PatientTable.pack(fill=BOTH,expand=1)
        self.PatientTable.bind("<ButtonRelease-1>",self.get_data)
        
             
        
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        self.txt_date.configure(placeholder_text=self.current_date)
        self.update_date_time()
        self.show_data('patient', clear=True)
        self.show_data('archives', clear=False)
        #=====================All functions=================
   
            
    def on_tooth_type_selected(self, event):
        self.tooth_selection['state'] = 'normal'  # Enable the listbox when a selection is made
        self.tooth_selection.delete(0, tk.END)
        tooth_type = self.tooth_type.get()
        if tooth_type == "Primary":
            self.teeth = ["#51", "#52", "#53","#54","#55","#61","#61","#62","#63",
                        "#64","#65","#71","#72","#73","#74","#75","#81","#82","#83","#84","#85"]  
        else:
            self.teeth = ["#18","#17","#16","#15","#14","#13","#12","#11",
                        "#21","#22","#23","#24","#25","#26","#27","#28","#48",
                        "#47","#46","#45","#44","#43","#42","#41","#31","#32","#33",
                        "#34","#35","#36","#37","#38"] 
        for tooth in self.teeth:
            self.tooth_selection.insert(tk.END, tooth)

    def on_tooth_selected(self, event):  # New function to handle selection event
        selected_teeth = [self.tooth_selection.get(idx) for idx in self.tooth_selection.curselection()]
        self.var_tooth.set(", ".join(selected_teeth))
        
    def show_listbox(self):
        screen_width=self.root.winfo_screenwidth()
        screen_height=self.root.winfo_screenheight()
        if self.lsb_tp.winfo_x() < 0:  # If the listbox is outside the visible area
            self.lsb_tp.place(x=730,y=350, width=200)  # Move it to the desired position
        else:
            self.lsb_tp.place(x=-500, y=-500)  # Move it outside the visible area
    
    def show_doctor_listbox(self):
        screen_width=self.root.winfo_screenwidth()
        screen_height=self.root.winfo_screenheight()
        if self.lsb_doc.winfo_x() < 0:  # If the listbox is outside the visible area
            self.lsb_doc.place(x=560,y=340, width=200)  # Move it to the desired position
            self.lsb_doc.lift()  # Bring the widget to the top of the stacking order
        else:
            self.lsb_doc.place(x=-500, y=-500)  # Move it outside the visible area
     
    def update_combobox(self, event=None):
        selected_values = [self.lsb_tp.get(idx) for idx in self.lsb_tp.curselection()]
        self.var_tp.set(", ".join(selected_values))  # Store the selected values in self.var_tp  
                
    def update_doc_combobox(self, event=None):
        selected_values = [self.lsb_doc.get(idx) for idx in self.lsb_doc.curselection()]
        self.var_doctor.set(", ".join(selected_values))
    
    def fetch_tp(self):
        self.tp_list.append("Empty")
        try:
            self.cur.execute("Select tp_name from treatment")
            cat = self.cur.fetchall()
            if cat:
                self.tp_list = ["Select"] + [i[0] for i in cat]
        except sqlite3.Error as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def fetch_doctor(self):
        self.doc_list.append("Empty")
        try:
            self.cur.execute("Select doc_name from doctor")
            cat = self.cur.fetchall()
            if cat:
                self.doc_list = ["Select"] + [i[0] for i in cat]
        except sqlite3.Error as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)            
    
            
    def show_data(self, table_name, clear=True):
        try:
            # Execute the query
            self.cur.execute(f"SELECT * FROM {table_name}")
            rows = self.cur.fetchall()

            # Clear the table if needed
            if clear:
                self.PatientTable.delete(*self.PatientTable.get_children())

            # Insert the new rows
            for row in rows:
                self.PatientTable.insert('', END, values=row)
        except sqlite3.Error as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    
    def get_data(self,ev):
        f=self.PatientTable.focus()
        content=(self.PatientTable.item(f))  
        row=content['values'] 
        self.var_pat_id.set(row[0])
        self.var_name.set(row[1])  
        self.var_doctor.set(row[2])                                            
        self.var_address.set(row[3])
        self.var_phone.set(row[4])
        self.var_prof.set(row[5])                                                
        self.var_dob.set(row[6])
        self.cmb_gender.set(row[7])                                                
       
         
    def append_entry(self):
        try:
            if not self.var_name.get():
                messagebox.showerror("Error","Patient Name is required",parent=self.root)
                return
            self.cur.execute("Select * from patient where name=?", (self.var_name.get(),))
            row = self.cur.fetchone()
            if row == None:
                messagebox.showerror("Error","This Patient is not registered, please add as new",parent=self.root)
            else:
                # Get the existing observations
                existing_obs = row[10]  #  'observations' is the 10th column
                # Append the new observations
                new_obs = existing_obs + '\n' + self.txt_obs.get('1.0',END)
                self.cur.execute("Update patient set doctor_name=?, mc=?, tooth=?, observations=?, tp=?, date=? where name=?", (
                                            self.var_doctor.get() + ', ' + row[2],  #  'doctor_name' is the 2nd column
                                            self.var_mc.get() + ', ' + row[8],  #  'mc' is the 8th column
                                            self.var_tooth.get() + ', ' + row[9],  #  'tooth' is the 9th column
                                            new_obs,
                                            self.var_tp.get() + ', ' + row[11],  #  'tp' is the 11th column
                                            self.txt_date.get() + ', ' + row[12],  #  'date' is the 12th column
                                            self.var_name.get()              
                ))
                self.con.commit()
                messagebox.showinfo("Success","Patient Record Updated Successfully",parent=self.root)
                self.show_data('patient', clear=True)
                self.show_data('archives', clear=False)
        except sqlite3.Error as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def search(self):
        try:
            if not self.var_searchtxt.get():
                messagebox.showerror("Error","Search input is required",parent=self.root)
            else:        
                # Search in 'patient' table
                self.cur.execute("select pat_id,name,doctor_name,address,phone,profession,dob,gender,mc,tooth,observations,tp from patient where name LIKE '%"+self.var_searchtxt.get()+"%'")  
                rows=self.cur.fetchall()
                if len(rows)!=0:
                    self.PatientTable.delete(*self.PatientTable.get_children())
                    for row in rows:
                        self.PatientTable.insert('',END,values=row)
                
                # Search in 'archive' table
                self.cur.execute("select pat_id,name,doctor_name,address,phone,profession,dob,gender,mc,tooth,observations,tp from archives where name LIKE '%"+self.var_searchtxt.get()+"%'")  
                rows=self.cur.fetchall()
                if len(rows)!=0:
                    for row in rows:
                        self.PatientTable.insert('',END,values=row)
                
                # If no records found in both tables
                if not self.PatientTable.get_children():
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except sqlite3.Error as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def other(self):
        # Store the values from get() calls in variables at the start of the method
        name = self.var_name.get()
        address = self.var_address.get()
        phone = self.var_phone.get()
      
        if not name or not address or not phone:
            messagebox.showerror("Error","All Patient Details are required, Select patient Data from database below",parent=self.root)
        else:        
            self.create_window()
        
                
    def create_window(self):          
        self.gen_win = Toplevel(self.root)     
        self.gen_win.title('SmileScribePro. GENERATE PATIENT RECORD')
        self.gen_win.iconbitmap(resource_path('icon.ico')) 
        self.gen_win.geometry('450x380+500+100')     
        self.gen_win.focus_force()

        self.amt_due = StringVar()
        self.amt_rcd = StringVar()
        self.amt_ble = StringVar()

        title = Label(self.gen_win,text="ADD BILL DATA",font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)                   
        lbl_amt_due = Label(self.gen_win,text="AMOUNT DUE",font=("times new roman",15)).place(x=20,y=60)
        txt_amt_due = Entry(self.gen_win,textvariable=self.amt_due,font=("times new roman",15),bg='lightyellow').place(x=20,y=100,width=250,height=30)

        lbl_amt_rcd = Label(self.gen_win,text="AMOUNT RECEIVED",font=("times new roman",15)).place(x=20,y=160)
        txt_amt_rcd = Entry(self.gen_win,textvariable=self.amt_rcd,font=("times new roman",15),bg='lightyellow').place(x=20,y=190,width=250,height=30)

        lbl_amt_ble = Label(self.gen_win,text="AMOUNT LEFT",font=("times new roman",15)).place(x=20,y=225)
        txt_amt_ble = Entry(self.gen_win,textvariable=self.amt_ble,font=("times new roman",15),bg='lightyellow').place(x=20,y=260,width=250,height=30)

        lbl_note = Label(self.gen_win,text=f"\t\tNote:'Enter 0 in AMOUNT DUE \n\tIF PATIENT HAS PAID ALL HIS/HER BILL'",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)    

        self.btn_update = Button(self.gen_win,text="SAVE | UPDATE RECORD",command=self.add_doctor_patient_rec,font=("times new roman",15),bg='lightblue')
        self.btn_update.place(x=100,y=300,width=250,height=30)
        
    def add_doctor_patient_rec(self):
        doctor = self.var_doctor.get()
        if not doctor:
            messagebox.showerror("Error", "Doctor Name is required", parent=self.root)
            return

        name = self.var_name.get()
        amt_rcd = self.amt_rcd.get()
        try:
            with sqlite3.connect(database=os.path.join(os.getcwd(), resource_path(r'PRMS.db'))) as con:
                cur = con.cursor()

                # Fetch tp and date from the patient table
                cur.execute("SELECT name, doctor_name, tp, date FROM patient WHERE name=?", (name,))
                patient_record = cur.fetchone()

                if patient_record:
                    name, doctor_name, tp, date = patient_record

                    # Fetch doc_id from the doctor table
                    cur.execute("SELECT doc_id FROM doctor WHERE doc_name=?", (doctor_name,))
                    doc_id_row = cur.fetchone()
                    doc_id = doc_id_row[0] if doc_id_row else None

                    # Check if a record with the same doctor and patient name already exists
                    cur.execute("SELECT doc_id, intervention, amount_paid, date FROM doctor_patient_records WHERE doc_name=? AND pat_name=?", (doctor, name))
                    existing_record = cur.fetchone()

                    # If the record exists and the data is different, insert a new record
                    if existing_record and (existing_record[1] != tp or existing_record[2] != amt_rcd or existing_record[3] != date):
                        params = (doc_id, doctor, name, tp, amt_rcd, date)
                        cur.execute("INSERT INTO doctor_patient_records (doc_id, doc_name, pat_name, intervention, amount_paid, date) VALUES (?, ?, ?, ?, ?, ?)", params)
                        messagebox.showinfo("Success", "Record Updated successfully", parent=self.root)
                    # If the record does not exist, insert a new record
                    elif not existing_record:
                        params = (doc_id, doctor, name, tp, amt_rcd, date)
                        cur.execute("INSERT INTO doctor_patient_records (doc_id, doc_name, pat_name, intervention, amount_paid, date) VALUES (?, ?, ?, ?, ?, ?)", params)
                        messagebox.showinfo("Success", "New record added successfully", parent=self.root)
                else:
                    messagebox.showerror("Error", "No patient record found with the given name", parent=self.root)
                con.commit()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def update_date_time(self):   
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d:%m:%Y")
        self.lbl_clock.configure(text=f"Welcome to SmileScribe Professional Patients Record Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)   
        
        
    def exit(self):
        self.is_running = False
        self.root.destroy() 
    
            
    
        
        
if __name__=="__main__":
    root=ctk.CTk()
    obj=entryClass(root)
    root.mainloop()