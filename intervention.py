from tkinter import*
import customtkinter as ctk
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import time
import permission
import sqlite3
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class interventionClass(ctk.CTk):
    def __init__(self,root):
        self.root=root
        self.root.state('zoomed')
        self.root.geometry("1100x600+220+130")
        self.root.iconbitmap(resource_path('icon.ico'))
        self.root.title("SmileScribePro")
        #======================Variables=====================
        self.var_tp_id=StringVar()
        self.var_tp_name=StringVar()
        self.var_tp_code=StringVar()
        self.var_tp_price=StringVar()
        
        #===================title================
        lbl_title=ctk.CTkLabel(self.root,text="Manage Interventions And Doctors",font=("goudy old style",30),fg_color="#184a45",text_color="white").pack(side=TOP,fill=X,padx=10,pady=10)
        
        lbl_name=ctk.CTkLabel(self.root,text="Intervention Name",font=("goudy old style",15)).place(x=50,y=100)
        txt_name=ctk.CTkEntry(self.root,textvariable=self.var_tp_name,font=("goudy old style",18),fg_color="lightyellow",width=230).place(x=50,y=130)
        
        lbl_code=ctk.CTkLabel(self.root,text="Code",font=("goudy old style",15)).place(x=300,y=100)
        txt_code=ctk.CTkEntry(self.root,textvariable=self.var_tp_code,font=("goudy old style",18),fg_color="lightyellow",width=100).place(x=300,y=130)
        
        lbl_price=ctk.CTkLabel(self.root,text="Price",font=("goudy old style",15)).place(x=430,y=100)
        txt_price=ctk.CTkEntry(self.root,textvariable=self.var_tp_price,font=("goudy old style",18),fg_color="lightyellow",width=200).place(x=430,y=130)
        
        
        btn_add=ctk.CTkButton(self.root,text="ADD",command=self.add,font=("goudy old style",15),fg_color="#4caf50",text_color="white",width=100,height=30).place(x=50,y=180)
        btn_update=ctk.CTkButton(self.root,text="Update",command=self.update,font=("goudy old style",15),fg_color="blue",text_color="white",width=100,height=30).place(x=160,y=180)
        btn_delete=ctk.CTkButton(self.root,text="Delete",command=self.delete,font=("goudy old style",15),fg_color="red",text_color="white",width=100,height=30).place(x=270,y=180)
                
        #=====================Category Details============
        
        tp_frame=ctk.CTkFrame(self.root,width=380,height=200)
        tp_frame.place(x=900,y=80)
        
        scolly=Scrollbar(tp_frame,orient=VERTICAL)
        scollx=Scrollbar(tp_frame,orient=HORIZONTAL)
        
        self.TreatmentTable=ttk.Treeview(tp_frame,columns=("tp_id","tp_name","tp_code","tp_price"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.TreatmentTable.xview)
        scolly.config(command=self.TreatmentTable.yview)
        
        self.TreatmentTable.heading("tp_id",text="ITV ID")
        self.TreatmentTable.heading("tp_name",text="Intervention") 
        self.TreatmentTable.heading("tp_code",text="Code")
        self.TreatmentTable.heading("tp_price",text="Price")             
        self.TreatmentTable["show"] ="headings"        
        self.TreatmentTable.column("tp_id",width=90)
        self.TreatmentTable.column("tp_name",width=100)
        self.TreatmentTable.column("tp_code",width=80)
        self.TreatmentTable.column("tp_price",width=100)            
        self.TreatmentTable.pack(fill=BOTH,expand=1)
        self.TreatmentTable.bind("<ButtonRelease-1>",self.get_data)
        
        #===================Doctors=========================
        #==========================Variables======================================
        self.var_doc_id=StringVar()
        self.var_doc_name=StringVar()
        self.var_doc_add=StringVar()
        self.var_doc_email=StringVar()
        self.var_doc_phone=StringVar()
        lbl_doctor_id=ctk.CTkLabel(self.root,text="Doctor ID",font=("goudy old style",15)).place(x=50,y=250)
        txt_doctor_id=ctk.CTkEntry(self.root,textvariable=self.var_doc_id,font=("goudy old style",18),fg_color="lightyellow",width=100).place(x=50,y=280)
        
        lbl_doctor_name=ctk.CTkLabel(self.root,text="Doctor Name",font=("goudy old style",15)).place(x=160,y=250)
        txt_doctor_name=ctk.CTkEntry(self.root,textvariable=self.var_doc_name,font=("goudy old style",18),fg_color="lightyellow",width=250).place(x=160,y=280)
        
        lbl_address=ctk.CTkLabel(self.root,text="Address",font=("goudy old style",15)).place(x=430,y=250)
        txt_address=ctk.CTkEntry(self.root,textvariable=self.var_doc_add,font=("goudy old style",18),fg_color="lightyellow",width=200).place(x=430,y=280)
        
        lbl_email=ctk.CTkLabel(self.root,text="Email",font=("goudy old style",15)).place(x=50,y=320)
        txt_email=ctk.CTkEntry(self.root,textvariable=self.var_doc_email,font=("goudy old style",18),fg_color="lightyellow",width=200).place(x=50,y=350)
        
        lbl_phone=ctk.CTkLabel(self.root,text="Phone",font=("goudy old style",15)).place(x=300,y=320)
        txt_phone=ctk.CTkEntry(self.root,textvariable=self.var_doc_phone,font=("goudy old style",18),fg_color="lightyellow",width=200).place(x=300,y=350)
        
        btn_add=ctk.CTkButton(self.root,text="ADD",font=("goudy old style",15),command=self.add_doctor,fg_color="#f1c40f",text_color="white",width=100,height=30).place(x=50,y=400)
        btn_update=ctk.CTkButton(self.root,text="Update",font=("goudy old style",15),command=self.update_doctor,fg_color="#27ae60",text_color="white",width=100,height=30).place(x=160,y=400)
        btn_delete=ctk.CTkButton(self.root,text="Delete",font=("goudy old style",15),command=self.delete_doctor,fg_color="#8e44ad",text_color="white",width=100,height=30).place(x=270,y=400)
        
        
         #=====================Doctor Details============
        
        doctor_frame=ctk.CTkFrame(self.root,width=400,height=200)
        doctor_frame.place(x=900,y=330)
        
        scolly=Scrollbar(doctor_frame,orient=VERTICAL)
        scollx=Scrollbar(doctor_frame,orient=HORIZONTAL)
        
        self.DoctorTable=ttk.Treeview(doctor_frame,columns=("doc_id","doc_name","doc_add","doc_email","doc_phone"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.DoctorTable.xview)
        scolly.config(command=self.DoctorTable.yview)
        
        self.DoctorTable.heading("doc_id",text="DOC ID")
        self.DoctorTable.heading("doc_name",text="Doctor Name") 
        self.DoctorTable.heading("doc_add",text="Address")
        self.DoctorTable.heading("doc_email",text="Email")
        self.DoctorTable.heading("doc_phone",text="Phone")             
        self.DoctorTable["show"] ="headings"        
        self.DoctorTable.column("doc_id",width=50)
        self.DoctorTable.column("doc_name",width=100)
        self.DoctorTable.column("doc_add",width=100)
        self.DoctorTable.column("doc_email",width=100)
        self.DoctorTable.column("doc_phone",width=100)            
        self.DoctorTable.pack(fill=BOTH,expand=1)
        self.DoctorTable.bind("<ButtonRelease-1>",self.get_doctor_data)
        
        
        #========================images==================
        '''self.img1=Image.open(resource_path("images\\tp1.png"))
        self.img1=self.img1.resize((500,200),Image.LANCZOS)
        self.img1=ImageTk.PhotoImage(self.img1)
        
        self.lbl_img1=Label(self.root,image=self.img1,bd=2,relief=RAISED)
        #self.lbl_img1.place(x=50,y=220)
        
        self.img2=Image.open(resource_path("images\\tp2.jpeg"))
        self.img2=self.img2.resize((500,200),Image.LANCZOS)
       # self.img2=ImageTk.PhotoImage(self.img2)
        
        self.lbl_img2=Label(self.root,image=self.img2,bd=2,relief=RAISED)
        #self.lbl_img2.place(x=580,y=280)
        
        
        '''
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        
        permission.interact_with_database((resource_path('PRMS.db')))
        self.show()
        self.show_doctor()
    
   
    def add(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_tp_name.get()=="" or self.var_tp_code.get()=="" or self.var_tp_price.get()=="":
                messagebox.showerror("Error","All Entries are required",parent=self.root)
            else:
                cur.execute("Select * from treatment where tp_name=?",(self.var_tp_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Intervention already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into treatment (tp_name,tp_code,tp_price) values(?,?,?)",(
                                        self.var_tp_name.get(),
                                        self.var_tp_code.get(),
                                        self.var_tp_price.get()
                                        ))
                    con.commit()
                    messagebox.showinfo("Success","Intervention Added Successfully",parent=self.root)
                    self.show()
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def show(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("select * from treatment")
            rows=cur.fetchall()
            self.TreatmentTable.delete(*self.TreatmentTable.get_children())
            for row in rows:
                self.TreatmentTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def get_data(self,ev):
        f=self.TreatmentTable.focus()
        content=(self.TreatmentTable.item(f))  
        row=content['values'] 
        self.var_tp_id.set(row[0])
        self.var_tp_name.set(row[1])
        self.var_tp_code.set(row[2])
        self.var_tp_price.set(row[3])
        
    def delete(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_tp_id.get()=="":
                messagebox.showerror("Error","Please select Intervention from the list",parent=self.root)
            else:
                cur.execute("Select * from treatment where tp_id=?",(self.var_tp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:                        
                        cur.execute("delete from treatment where tp_id=?",(self.var_tp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Intervention Deleted Successfully",parent=self.root)
                        self.show()
                        self.var_tp_id.set("") 
                        self.var_tp_name.set("")               
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def update(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_tp_code.get()=="":
                messagebox.showerror("Error","Intervention code is required",parent=self.root)
            else:
                cur.execute("Select * from treatment where tp_code=?",(self.var_tp_code.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Intervention",parent=self.root)
                else:
                    cur.execute("Update treatment set tp_name=?,tp_code=?,tp_price=?  where tp_id=?",(
                                                self.var_tp_name.get(),
                                                self.var_tp_code.get(),
                                                self.var_tp_price.get(),
                                                self.var_tp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Intervention Record Updated Successfully",parent=self.root)
                    cur.close()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 


    def clear(self):
        self.var_tp_id.set("")
        self.var_tp_name.set("")
        self.var_tp_code.set("")
        self.var_tp_price.set("")   
        
        
    def add_doctor(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_doc_id.get()=="" or self.var_doc_name.get()=="" or self.var_doc_email.get()=="":
                messagebox.showerror("Error","All Entries are required",parent=self.root)
            else:
                cur.execute("Select * from doctor where doc_id=?",(self.var_doc_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Doctor already present, try different",parent=self.root)
                else:
                    cur.execute("Insert into doctor (doc_id,doc_name,doc_add,doc_email,doc_phone) values(?,?,?,?,?)",(
                                        self.var_doc_id.get(),
                                        self.var_doc_name.get(),
                                        self.var_doc_add.get(),
                                        self.var_doc_email.get(),
                                        self.var_doc_phone.get()
                                        ))
                    con.commit()
                    messagebox.showinfo("Success","Doctor Added Successfully",parent=self.root)
                    self.show_doctor()
                self.clear_doctor()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root) 
            
            
    def update_doctor(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_doc_id.get()=="":
                messagebox.showerror("Error","Doctor ID is required",parent=self.root)
            else:
                cur.execute("Select * from doctor where doc_id=?",(self.var_doc_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Doctor Credentials",parent=self.root)
                else:
                    cur.execute("Update doctor set doc_name=?,doc_add=?,doc_email=?,doc_phone=?  where doc_id=?",(
                                                
                                                self.var_doc_name.get(),
                                                self.var_doc_add.get(),
                                                self.var_doc_email.get(),
                                                self.var_doc_phone.get(),
                                                self.var_doc_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Intervention Record Updated Successfully",parent=self.root)
                    cur.close()
                    self.show_doctor()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)   
    
    def delete_doctor(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            if self.var_doc_id.get()=="":
                messagebox.showerror("Error","Please select Doctor from the list",parent=self.root)
            else:
                cur.execute("Select * from doctor where doc_id=?",(self.var_doc_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:                        
                        cur.execute("delete from doctor where doc_id=?",(self.var_doc_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Doctor Deleted Successfully",parent=self.root)
                        self.show_doctor()
                        self.clear_doctor()               
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
                         
            
    def show_doctor(self):
        permission.interact_with_database((resource_path('PRMS.db'))) 
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("select * from doctor")
            rows=cur.fetchall()
            self.DoctorTable.delete(*self.DoctorTable.get_children())
            for row in rows:
                self.DoctorTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
            
            
    def get_doctor_data(self,ev):
        f=self.DoctorTable.focus()
        content=(self.DoctorTable.item(f))  
        row=content['values'] 
        self.var_doc_id.set(row[0])
        self.var_doc_name.set(row[1])
        self.var_doc_add.set(row[2])
        self.var_doc_email.set(row[3])
        self.var_doc_phone.set(row[4])        
    
            
    def clear_doctor(self):
        self.var_doc_id.set("")
        self.var_doc_name.set("")
        self.var_doc_add.set("")
        self.var_doc_email.set("")
        self.var_doc_phone.set("")
                        
if __name__=="__main__":
    root=ctk.CTk()
    obj=interventionClass(root)
    root.mainloop()