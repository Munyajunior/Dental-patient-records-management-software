from tkinter import*
import customtkinter as ctk
from customtkinter import*
from PIL import Image
from tkinter import ttk,messagebox
import sqlite3
import os
import email_pass
import smtplib #pip install smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime,time
from datetime import datetime,timedelta
import permission
import threading
import sys
import schedule
from plyer import notification
import win32com.client
import pythoncom


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")



class ReminderService(ctk.CTk): 

    def show_reminder(self, name, date):
        ''' Shows a reminder for an appointment. It calculates 
        the time difference between the current time and the 
        appointment time, and if the time difference is 
        positive, it waits until it's time to show the 
        reminder. If the appointment date has already passed,
        it shows an error message.'''
        # Calculate the time difference between now and the appointment date
        appointment_date = datetime.strptime(date, "%d-%m-%Y")
        reminder_date = appointment_date - timedelta(days=2)
        time_diff = reminder_date - datetime.now()
        time_diff_in_sec = time_diff.total_seconds()

        notification.notify(title='Appointment Scheduled', message=f'An Appointment has been Scheduled with {name} on the {date}\nYou will be notified a few days before the appointment day is due', timeout=60)
        # If the time difference is positive, wait until it's time to show the reminder
        if time_diff_in_sec > 0:
            time.sleep(time_diff_in_sec)
            notification.notify(title='Reminder', meassage="You have an appointment with {} in 2 days.".format(name),timeout=45)
             # Create a root window and hide it
            root.withdraw()
        else:
            notification.notify(title='Reminder Missed',message="Appointment Date has already passed please enter a future date",timeout=45)
            # Destroy the root window
            root.destroy()


    def schedule_reminder(self, name, date):
        ''' Schedules the show_reminder function to run every 
        day at a specific time (09:00). It checks 
        if there's a task scheduled for the current 
        moment and runs it.'''
        # Schedule the show_reminder function to run every day at a specific time
        schedule.every().day.at("09:00").do(self.show_reminder, name, date)

        while True:
            # Check if there's a task scheduled for the current moment and run it
            schedule.run_pending()
            time.sleep(1)
   
    def run_with_args(self,name,date):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM schedules")
            schedules=cur.fetchall()
            con.close()
            for schedule in schedules:
                name,date = schedule
             
            self.schedule_reminder(name, date)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=root)    
    
    def create_task(self):
        pythoncom.CoInitialize()
        computer_name = ""  # leave all blank for current computer, current user
        computer_username = ""
        computer_userdomain = ""
        computer_password = ""
        action_id = "Schedule Appointment"  # an arbitrary action ID
        action_path =resource_path(r"doctor_reminder_task.bat")  # path to your Python script
        action_arguments = ''  # arguments for the script
        action_workdir =resource_path(r"")  # working directory for action executable
        task_id = "Appointment Reminder"  # an arbitrary task ID
        task_hidden = False  # task will be visible in task scheduler

        # connect to the task scheduler (Vista/Server 2008 and above only)
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
        root_folder = scheduler.GetFolder("\\")

        # define the information for the task
        task_def = scheduler.NewTask(0)
        col_actions = task_def.Actions
        action = col_actions.Create(0)
        action.ID = action_id
        action.Path = action_path
        action.WorkingDirectory = action_workdir
        action.Arguments = action_arguments

        info = task_def.RegistrationInfo
        info.Author = "SmileScribePro"
        info.Description = "Reminds Secretary or Doctor of Scheduled Appointment with patient before the date is due"

        settings = task_def.Settings
        settings.Enabled = True
        settings.Hidden = task_hidden

        # run the task every day
        trigger = task_def.Triggers.Create(2)  # 2 means "daily" trigger
        trigger.DaysInterval = 1
        trigger.StartBoundary = "2024-04-1T10:00:00"  # start the task on this date

        # register the task (create or update, just keep the task name the same)
        result = root_folder.RegisterTaskDefinition(task_id, task_def, 6, "", "", 3)

        return result
    
    def create_patient_reminder_task(self):
        pythoncom.CoInitialize()
        computer_name = ""  # leave all blank for current computer, current user
        computer_username = ""
        computer_userdomain = ""
        computer_password = ""
        action_id = "Remind Patient of Appointment"  # an arbitrary action ID
        action_path =resource_path(r"remindPatient.bat")  # path to your Python script
        action_arguments = ''  # arguments for the script
        action_workdir =resource_path(r"")  # working directory for action executable
        task_id = "Pateint Appointment Reminder"  # an arbitrary task ID
        task_hidden = False  # task will be visible in task scheduler

        # connect to the task scheduler (Vista/Server 2008 and above only)
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
        root_folder = scheduler.GetFolder("\\")

        # define the information for the task
        task_def = scheduler.NewTask(0)
        col_actions = task_def.Actions
        action = col_actions.Create(0)
        action.ID = action_id
        action.Path = action_path
        action.WorkingDirectory = action_workdir
        action.Arguments = action_arguments

        info = task_def.RegistrationInfo
        info.Author = "SmileScribePro"
        info.Description = "Reminds Patient of Scheduled Appointment with patient before the date is due"

        settings = task_def.Settings
        settings.Enabled = True
        settings.Hidden = task_hidden

        # run the task every day
        trigger = task_def.Triggers.Create(2)  # 2 means "daily" trigger
        trigger.DaysInterval = 1
        trigger.StartBoundary = "2024-04-1T10:00:00"  # start the task on this date

        # register the task (create or update, just keep the task name the same)
        result = root_folder.RegisterTaskDefinition(task_id, task_def, 6, "", "", 3)

        return result
    
    


class appointmentClass(ctk.CTk):
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
        self.service=ReminderService()
        self.app_list=[]
        self.pending_tasks = []
       
        
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
                                    ,height=50,width=150
                                    ,corner_radius=0
                                    ).place(anchor='e', x=x_position, y=30)
        #======================Clock============================
        self.lbl_clock=ctk.CTkLabel(self.root,text="Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS"
                                    ,font=("calibri",18,"bold")
                                    ,fg_color=("#487eb0","#4d636d"),bg_color="#fff"
                                    ,width=screen_width
                                    ,text_color="#fff")
        self.lbl_clock.place(x=0,y=65) 

        #==============Patient Frame=========
        PatientFrame1 = ctk.CTkFrame(self.root)
        PatientFrame1.place(x=10,y=100)
        
        pTitle=ctk.CTkLabel(PatientFrame1,text="All Patients",font=("goudy old style",20,"bold"),fg_color="#262626",text_color="white",bg_color="white",width=390).pack(side=TOP,fill=X)
        
        #=====================Product Details Frame============
        PatientFrame2=ctk.CTkFrame(self.root,width=395,height=375)
        PatientFrame2.place(x=10,y=130)
        
        scolly=Scrollbar(PatientFrame2,orient=VERTICAL)
        scollx=Scrollbar(PatientFrame2,orient=HORIZONTAL)
        
        self.Patient_Table=ttk.Treeview(PatientFrame2,columns=("pat_id","name","address","phone"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.Patient_Table.xview)
        scolly.config(command=self.Patient_Table.yview)
        
        self.Patient_Table.heading("pat_id",text="PAT ID")
        self.Patient_Table.heading("name",text="Name") 
        self.Patient_Table.heading("address",text="Address")
        self.Patient_Table.heading("phone",text="Phone")     
                
        self.Patient_Table["show"] ="headings" 
               
        self.Patient_Table.column("pat_id",width=90)
        self.Patient_Table.column("name",width=100)
        self.Patient_Table.column("address",width=80)
        self.Patient_Table.column("phone",width=100)            
        self.Patient_Table.pack(fill=BOTH,expand=1)
        self.Patient_Table.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note=ctk.CTkLabel(PatientFrame2,text=f"Note:'Enter 0 Appointment Date to remove Patient \nfrom the Appointment Manager'",font=("goudy old style",18),anchor='w',fg_color="#d35400").pack(side=BOTTOM,fill=X)
        
        #==============Appointment Frame====
        
        App_Frame=ctk.CTkFrame(self.root)
        App_Frame.place(x=410,y=100)
        self.appTitle=ctk.CTkLabel(App_Frame,text="Manage Appointments",font=("calibri",18,"bold"))
        self.appTitle.pack(side=TOP,fill=X)
        
        scolly=Scrollbar(App_Frame,orient=VERTICAL)
        scollx=Scrollbar(App_Frame,orient=HORIZONTAL)
        
        self.AppTable=ttk.Treeview(App_Frame,columns=("pat_id","name","phone","email","appointment"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.AppTable.xview)
        scolly.config(command=self.AppTable.yview)
        
        self.AppTable.heading("pat_id",text="PAT ID")
        self.AppTable.heading("name",text="Name") 
        self.AppTable.heading("phone",text="Phone")
        self.AppTable.heading("email",text="Email")     
        self.AppTable.heading("appointment",text="Appointment") 
                
        self.AppTable["show"] ="headings" 
               
        self.AppTable.column("pat_id",width=80)
        self.AppTable.column("name",width=100)
        self.AppTable.column("phone",width=100)
        self.AppTable.column("email",width=100)
        self.AppTable.column("appointment",width=100)            
        self.AppTable.pack(fill=BOTH,expand=1)
        self.AppTable.bind("<ButtonRelease-1>",self.get_data_app)
       
       #=======================Add Cart Widgets Frame===================
        #=====Variable=====
        self.var_pat_id=ctk.StringVar()
        self.var_name=ctk.StringVar()
        self.var_phone=ctk.StringVar()
        self.var_email=ctk.StringVar()
        self.var_appointment_date=ctk.StringVar()
        
        Add_appWidgetsFrame=ctk.CTkFrame(self.root,width=510)
        Add_appWidgetsFrame.place(x=400,y=380)
        
        lbl_p_name=ctk.CTkLabel(Add_appWidgetsFrame,text="Name",font=("times new roman",15)).place(x=5,y=10)       
        txt_p_name=ctk.CTkEntry(Add_appWidgetsFrame,textvariable=self.var_name,font=("times new roman",17),state='readonly').place(x=5,y=50)
        
        lbl_p_phone=ctk.CTkLabel(Add_appWidgetsFrame,text="Phone",font=("times new roman",15)).place(x=150,y=10)       
        txt_p_phone=ctk.CTkEntry(Add_appWidgetsFrame,textvariable=self.var_phone,font=("times new roman",17),state='readonly').place(x=150,y=50)
        
        lbl_p_email=ctk.CTkLabel(Add_appWidgetsFrame,text="email",font=("times new roman",15)).place(x=300,y=10)       
        txt_p_email=ctk.CTkEntry(Add_appWidgetsFrame,textvariable=self.var_email,font=("times new roman",17),width=200).place(x=295,y=50)
        
        lbl_p_appointment_date=ctk.CTkLabel(Add_appWidgetsFrame,text="Appointment Date",font=("times new roman",15)).place(x=5,y=100)       
        txt_p_appointment_date=ctk.CTkEntry(Add_appWidgetsFrame,textvariable=self.var_appointment_date,font=("times new roman",17)).place(x=5,y=140)
                
        btn_clear_cart=ctk.CTkButton(Add_appWidgetsFrame,command=self.clear,text="Clear",fg_color="#EA2027",font=("times new roman",15,"bold")).place(x=150,y=140)      
        btn_add_cart=ctk.CTkButton(Add_appWidgetsFrame,command=self.add_update_app,fg_color="#0652DD",hover_color="#6F1E51",text=f"Add | Update \nAppointment",font=("times new roman",15,"bold")).place(x=300,y=140)   
        
        #=====================Patient Appointment Details============
        p_app_frame=ctk.CTkFrame(self.root)
        p_app_frame.place(x=920,y=100)
        self.appTitle=ctk.CTkLabel(p_app_frame,text="ALL Appointments",font=("calibri",18))
        self.appTitle.pack(side=TOP,fill=X)
        
        scolly=Scrollbar(p_app_frame,orient=VERTICAL)
        scollx=Scrollbar(p_app_frame,orient=HORIZONTAL)
        
        self.Patient_AppTable=ttk.Treeview(p_app_frame,columns=("pat_id","name","phone","email","appointment"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.Patient_AppTable.xview)
        scolly.config(command=self.Patient_AppTable.yview)
        
        self.Patient_AppTable.heading("pat_id",text="PAT ID")
        self.Patient_AppTable.heading("name",text="Full Name")
        self.Patient_AppTable.heading("phone",text="Phone")
        self.Patient_AppTable.heading("email",text="Email")
        self.Patient_AppTable.heading("appointment",text="Appointment")
        
        self.Patient_AppTable["show"] ="headings" 
        
        self.Patient_AppTable.column("pat_id",width=90)
        self.Patient_AppTable.column("name",width=100)
        self.Patient_AppTable.column("phone",width=100)
        self.Patient_AppTable.column("email",width=100)
        self.Patient_AppTable.column("appointment",width=100)
          
        self.Patient_AppTable.pack(fill=BOTH,expand=1)
        self.Patient_AppTable.bind("<ButtonRelease-1>",self.app_get_data)
        self.show_p_app()
        
        Add_p_appWidgetsFrame=ctk.CTkFrame(self.root,width=430)
        Add_p_appWidgetsFrame.place(x=920,y=380)
        
        btn_clear_p_app=ctk.CTkButton(Add_p_appWidgetsFrame,command=self.add_app,text="Add Appointment",font=("times new roman",15,"bold"),hover_color="#4cd137",width=180,height=30).place(x=5,y=5)      
        btn_delete_p_app=ctk.CTkButton(Add_p_appWidgetsFrame,command=self.delete,text="Delete Appointment",font=("times new roman",15,"bold"),hover_color="#eb2f06",width=180,height=30).place(x=5,y=40)   
        
           
 
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        permission.interact_with_database((resource_path('PRMS.db')))
        self.show()
        self.show_p_app()
        self.update_date_time()
    #===========================ALL FUNCTIONS==================   
        
        
   


    
        
    def update_date_time(self): 
            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d:%m:%Y")
            self.lbl_clock.configure(text=f"Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200, self.update_date_time)
            

    def exit(self):
        self.is_running = False
        self.root.destroy()
       
    def show(self):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("Select pat_id,name,address,phone from patient")
            rows=cur.fetchall()
            self.Patient_Table.delete(*self.Patient_Table.get_children())
            for row in rows:
                self.Patient_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
       
    def show_app(self):
        try:
            self.AppTable.delete(*self.AppTable.get_children())
            for row in self.app_list:
                self.AppTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
               
            
    def show_p_app(self):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("select * from appointments")
            rows=cur.fetchall()
            self.Patient_AppTable.delete(*self.Patient_AppTable.get_children())
            for row in rows:
                self.Patient_AppTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)       
            
    def add_update_app(self):
        self.remind_patient(self.var_email.get(),self.var_appointment_date.get())
        self.appointments=self.var_appointment_date.get()  
        try:
            if  self.var_pat_id.get()=='':
                messagebox.showerror('Error',"Please select Patient from the List",parent=self.root)            
            elif self.var_appointment_date.get()=='':
                messagebox.showerror('Error',"Appointment Date is Required",parent=self.root)
            else:
                cart_data=[self.var_pat_id.get(),self.var_name.get(),self.var_phone.get(),self.var_email.get(),self.var_appointment_date.get()]
                
                #=========update cart===============
                present='no'
                index_=0
                for row in self.app_list:
                    if self.var_pat_id.get()==row[0]:
                        present='yes'
                        break
                    index_+=1
                if present=='yes':
                    op=messagebox.askyesno('Confirm',"Intervention already present\nDo you want to Update | Remove from the Bill List",parent=self.root)
                    if op==True:
                        if self.var_appointment_date.get()=="0":
                            self.app_list.pop(index_)
                        else:
                            self.app_list[index_][3]=self.var_email.get()
                            self.app_list[index_][4]=self.var_appointment_date.get()
                            self.send_email(self.appointments)
                            self.service.create_patient_reminder_task()
                            self.remind_doctor(self.var_name.get(),self.appointments)
                            return
                else:                   
                    self.app_list.append(cart_data)
                
                
                self.show_app()   
                

                if self.appointments=='0':
                    return
                else:   
                    self.send_email(self.appointments) 
                    self.service.create_patient_reminder_task()
                    self.remind_doctor(self.var_name.get(),self.appointments)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)       
                   
                 
            
    def add_app(self):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Patient Name is required",parent=self.root)
            else:
                cur.execute("Select * from appointments where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Patient already has an appointment Scheduled, to update patient appointment info, delete patient in all appointments then click Add or Update Appointment",parent=self.root)
                else:
                    cur.execute("Insert into appointments (pat_id,name,phone,email,appointment) values(?,?,?,?,?)",(
                                                self.var_pat_id.get(),
                                                self.var_name.get(),  
                                                self.var_phone.get(),
                                                self.var_email.get(), 
                                                self.var_appointment_date.get(),                 
                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Patient Appointment Added Successfully",parent=self.root)
                    
                    self.show_p_app()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
    
    def delete(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("Select * from appointments where name=?",(self.var_name.get(),))
            row=cur.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Patient Name",parent=self.root)
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                if op==True:                        
                    cur.execute("delete from appointments where name=?",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Delete","Patient Appointment Deleted Successfully",parent=self.root)
                    self.show_p_app()               
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
            
            
        
    def get_data(self,ev):
        f=self.Patient_Table.focus()
        content=(self.Patient_Table.item(f))  
        row=content['values']
        if row:
            self.var_pat_id.set(row[0])
            self.var_name.set(row[1])
            self.var_phone.set(row[3])
            self.var_email.set('')  
            self.var_appointment_date.set('')   
        
    def get_data_app(self,ev):
        f=self.AppTable.focus()
        content=(self.AppTable.item(f))  
        row=content['values']
        self.var_pat_id.set(row[0])
        self.var_name.set(row[1])
        self.var_phone.set(row[2])
        self.var_email.set(row[3]) 
        self.var_appointment_date.set(row[4])     
    
    def app_get_data(self,ev):
        f=self.Patient_AppTable.focus()
        content=(self.Patient_AppTable.item(f))  
        row=content['values'] 
        self.var_pat_id.set(row[0])
        self.var_name.set(row[1])
        self.var_phone.set(row[2])
        self.var_email.set(row[3]) 
        self.var_appointment_date.set(row[4])               
    
    
    def clear(self):
        self.var_pat_id.set('')
        self.var_name.set('')
        self.var_phone.set('')
        self.var_email.set('')
        self.var_appointment_date.set('')


    def send_email(self, appointment_date): 
        self.name=self.var_name.get() 
        self.email=self.var_email.get()
        email_=email_pass.email_.strip()
        pass_=email_pass.pass_
        try:
            msg = MIMEMultipart()
            msg['From'] = email_
            msg['To'] = self.email.strip()
            msg['Subject'] =f'Appointment Confirmation\nConfirmation de rendez-vous'
            body =f'''Dear,Cher {self.name},\n\nYou have an appointment scheduled on {appointment_date}
            \n\nVous avez un rendez-vous prévu le {appointment_date}'''

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
        
            server.login(email_, pass_)
            text = msg.as_string()
            server.sendmail(email_, self.email, text)
            messagebox.showinfo("Email Sent",f"Appointment Email has been sent to {self.name.upper()}!!!!!",parent=self.root)
            server.quit()
        except smtplib.SMTPException as ex:
            messagebox.showerror("Connection Error",f"Error due to : {str(ex)}",parent=self.root)    

    def remind_patient(self,email,date):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("INSERT INTO patientRemind VALUES (?, ?)", (email, date))
            con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror("Remind Patient Database Error",f"Error due to : {str(ex)}",parent=self.root) 
           
    def remind_doctor(self, name, date):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("INSERT INTO schedules VALUES (?, ?)", (name, date))
            con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror("Remind Doctor Error",f"Error due to : {str(ex)}",parent=self.root) 
        x1=threading.Thread(target=self.service.run_with_args,args=(name,date)) 
        x2=threading.Thread(target=self.service.create_task)
        x1.start()
        x2.start()
        
    
 
  
    
if __name__=="__main__":
    root=ctk.CTk()
    obj=appointmentClass(root)
    root.mainloop()
    
