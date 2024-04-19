from tkinter import*
import customtkinter as ctk
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import permission
import sqlite3 
import time
import os
import tempfile
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class BillClass(ctk.CTk):
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
        self.cart_list=[]

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
 

        
        
        
        #=================Intervention Main frame================
        InterventionFrame = ctk.CTkFrame(self.root)
        InterventionFrame.pack(padx=10,pady=100, side="left",anchor='n') 

        pTitle=ctk.CTkLabel(InterventionFrame,text="All Interventions",font=("goudy old style",20,"bold"),text_color="#fff",fg_color="#262626",width=380).pack(side=TOP,fill=X)

        #=================Intervention Search frame================
        
        #==========Variables================
        self.var_search=ctk.StringVar()

        lbl_search=ctk.CTkLabel(self.root,text="Search Intervention | By Name ",font=("times new roman",15,"bold")).place(x=10,y=130)

        lbl_search=ctk.CTkLabel(self.root,text="Intervention",font=("times new roman",15,"bold")).place(x=10,y=170)
        txt_search=ctk.CTkEntry(self.root,textvariable=self.var_search,font=("times new roman",15),fg_color="lightyellow",width=150,height=22).place(x=100,y=170)
        btn_search=ctk.CTkButton(self.root,text="Search",command=self.search,font=("goudy old style",15),fg_color="#2196f3",width=100,height=25).place(x=280,y=170)
        btn_show_all=ctk.CTkButton(self.root,text="Show All",command=self.show,font=("goudy old style",15),fg_color="#083531",width=100,height=25).place(x=280,y=140)

        #=====================Intervention Frame============
        InterventionFrame3=ctk.CTkFrame(self.root)
        InterventionFrame3.place(x=10,y=200)

        scolly=Scrollbar(InterventionFrame3,orient=VERTICAL)
        scollx=Scrollbar(InterventionFrame3,orient=HORIZONTAL)

        self.Intervention_Table=ttk.Treeview(InterventionFrame3,columns=("tp_id","tp_name","tp_code","tp_price"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.Intervention_Table.xview)
        scolly.config(command=self.Intervention_Table.yview)

        self.Intervention_Table.heading("tp_id",text="ITV ID")
        self.Intervention_Table.heading("tp_name",text="Intervention") 
        self.Intervention_Table.heading("tp_code",text="Code")
        self.Intervention_Table.heading("tp_price",text="Price")     

        self.Intervention_Table["show"] ="headings" 

        self.Intervention_Table.column("tp_id",width=90)
        self.Intervention_Table.column("tp_name",width=100)
        self.Intervention_Table.column("tp_code",width=80)
        self.Intervention_Table.column("tp_price",width=100)            
        self.Intervention_Table.pack(fill=BOTH,expand=1)
        self.Intervention_Table.bind("<ButtonRelease-1>",self.get_data)

        #============Patient Frame==========
        PatientFrame = ctk.CTkFrame(self.root)
        PatientFrame.place(x=10,y=450)
        pTitle=ctk.CTkLabel(PatientFrame,text="All Patients",font=("goudy old style",17),width=390).pack(side=TOP,fill=X)

        scrolly = Scrollbar(PatientFrame,orient=VERTICAL)
        scrollx = Scrollbar(PatientFrame,orient=HORIZONTAL)

        self.patient_table =ttk.Treeview(PatientFrame,columns=("pat_id","name","contact"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.patient_table.xview)
        scolly.config(command=self.patient_table.yview)

        
        self.patient_table.heading("pat_id",text="PAT ID")
        self.patient_table.heading("name",text="Name") 
        self.patient_table.heading("contact",text="Contact")  
                
        self.patient_table["show"] ="headings" 
               
        self.patient_table.column("pat_id",width=90)
        self.patient_table.column("name",width=100)
        self.patient_table.column("contact",width=80)            
        self.patient_table.pack(fill=BOTH,expand=1)
        self.patient_table.bind("<ButtonRelease-1>",self.get_patient_data)
       
        
        #===========================Customer Frame==============
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=ctk.CTkFrame(self.root)
        CustomerFrame.place(x=410,y=100)
        
        cTitle=ctk.CTkLabel(CustomerFrame,text="Patient Details",font=("helvetica",18),width=520).pack(side=TOP,fill=X)
        
        lbl_name=ctk.CTkLabel(self.root,text="Name",font=("helvetica",15)).place(x=420,y=145)
        txt_name=ctk.CTkEntry(self.root,textvariable=self.var_cname,font=("times new roman",15)).place(x=480,y=145)
        
        lbl_contact=ctk.CTkLabel(self.root,text="Contact No.",font=("helvetica",15)).place(x=640,y=145)
        txt_contact=ctk.CTkEntry(self.root,textvariable=self.var_contact,font=("times new roman",15)).place(x=750,y=145)
        
       
        #====================================Cart Frame===================  
        cart_Frame=ctk.CTkFrame(self.root)
        cart_Frame.place(x=410,y=190)
        self.cartTitle=ctk.CTkLabel(cart_Frame,text="Manage Patient Bill",font=("Adobe Caslon Pro",17,),width=520)
        self.cartTitle.pack(side=TOP,fill=X)
        
        scolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(cart_Frame,columns=("tp_id","tp_name","tp_code","tp_price"),yscrollcommand=scolly.set,xscrollcommand=scollx.set)
        scollx.pack(side=BOTTOM,fill=X)
        scolly.pack(side=RIGHT,fill=Y)
        scollx.config(command=self.CartTable.xview)
        scolly.config(command=self.CartTable.yview)
        self.CartTable.heading("tp_id",text="ITV ID")
        self.CartTable.heading("tp_name",text="Intervention") 
        self.CartTable.heading("tp_code",text="Code")
        self.CartTable.heading("tp_price",text="Price")     
                
        self.CartTable["show"] ="headings" 
               
        self.CartTable.column("tp_id",width=90)
        self.CartTable.column("tp_name",width=100)
        self.CartTable.column("tp_code",width=80)
        self.CartTable.column("tp_price",width=100)            
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
       
       #=======================Add Cart Widgets Frame===================
        #=====Variable=====
        self.var_tp_id=StringVar()
        self.var_tp_name=StringVar()
        self.var_price=StringVar()
        self.var_code=StringVar()
        
        Add_cartWidgetsFrame=ctk.CTkFrame(self.root,width=520,height=200)
        Add_cartWidgetsFrame.place(x=410,y=470)
        
        lbl_p_name=ctk.CTkLabel(Add_cartWidgetsFrame,text="Intervention",font=("times new roman",15)).place(x=5,y=5)       
        txt_p_name=ctk.CTkEntry(Add_cartWidgetsFrame,textvariable=self.var_tp_name,font=("times new roman",15),state='readonly').place(x=5,y=35)
        
        lbl_p_price=ctk.CTkLabel(Add_cartWidgetsFrame,text="Code",font=("times new roman",15)).place(x=200,y=5)       
        txt_p_price=ctk.CTkEntry(Add_cartWidgetsFrame,textvariable=self.var_code,font=("times new roman",15)).place(x=200,y=35)
        
        lbl_p_qty=ctk.CTkLabel(Add_cartWidgetsFrame,text="Price",font=("times new roman",15)).place(x=380,y=5)       
        txt_p_qty=ctk.CTkEntry(Add_cartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),state='readonly').place(x=380,y=35)
        
        btn_clear_cart=ctk.CTkButton(Add_cartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),fg_color="#009688").place(x=200,y=70)      
        btn_add_cart=ctk.CTkButton(Add_cartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),fg_color="orange").place(x=380,y=70)      
 
        lbl_note=ctk.CTkLabel(Add_cartWidgetsFrame,text="Note:'Enter 0 Code to remove Intervention from the Bill'",font=("goudy old style",18),text_color="red").place(x=5,y=120)

        #================Billing Area=====
        billFrame=ctk.CTkFrame(self.root)
        billFrame.place(x=950,y=100)
        
        BTitle=ctk.CTkLabel(billFrame,text="Patient Bill Area",font=("goudy old style",20,"bold"),fg_color="#f44336",text_color="white",width=410).pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrollx=Scrollbar(billFrame,orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        
        self.txt_bill_area=ctk.CTkTextbox(billFrame,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,height=420)
        scrollx.config(command=self.txt_bill_area.xview)
        scrolly.config(command=self.txt_bill_area.yview)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        
        self.bill_img=ctk.CTkImage(dark_image=Image.open(resource_path("images\\emma.png")),
                                   light_image=Image.open(resource_path("images\\emma.png")),size=(50,50))
        
        #+++++++++++++++++++++++++bILLING Button==============
        billMenuFrame=ctk.CTkFrame(self.root,width=410,height=200)
        billMenuFrame.place(x=950,y=570)
 
        self.lbl_amnt=ctk.CTkLabel(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",15,"bold"),fg_color="#3f51b5",text_color="white",width=153,height=70)
        self.lbl_amnt.place(x=2,y=5)
        
        self.lbl_discount=ctk.CTkLabel(billMenuFrame,text='Discount \n[0%]',font=("goudy old style",15,"bold"),fg_color="#abc34a",text_color="white",width=100,height=70)
        self.lbl_discount.place(x=157,y=5)
        
        self.lbl_net_pay=ctk.CTkLabel(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",15,"bold"),fg_color="#607d8b",text_color="white",width=145,height=70)
        self.lbl_net_pay.place(x=260,y=5)
        
        btn_print=ctk.CTkButton(billMenuFrame,text='Save | Print',command=self.print_bill,font=("goudy old style",15,"bold"),fg_color="lightgreen",text_color="white",width=120,height=50)
        btn_print.place(x=2,y=80)
        
        btn_clear_all=ctk.CTkButton(billMenuFrame,text='Clear All',command=self.clear_all,font=("goudy old style",15,"bold"),fg_color="gray",text_color="white",width=120,height=50)
        btn_clear_all.place(x=124,y=80)
        
        btn_generate=ctk.CTkButton(billMenuFrame,text='Generate Bill',command=self.generate_bill,font=("goudy old style",15,"bold"),fg_color="#009688",text_color="white",width=158,height=50)
        btn_generate.place(x=246,y=80)
        
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        
        permission.interact_with_database((os.path.join(os.getcwd(), resource_path('PRMS.db'))))
        self.show()
        self.show_patient()
        self.update_date_time()
        
        #================================All functions==========

    def show(self):
        permission.interact_with_database((os.path.join(os.getcwd(), resource_path('PRMS.db'))))
        con=sqlite3.connect(database=os.path.join(os.getcwd(), resource_path(r'PRMS.db')))
        cur=con.cursor()
        try:
            cur.execute("Select tp_id,tp_name,tp_code,tp_price from treatment")
            rows=cur.fetchall()
            self.Intervention_Table.delete(*self.Intervention_Table.get_children())
            for row in rows:
                self.Intervention_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def show_patient(self):
        permission.interact_with_database((os.path.join(os.getcwd(), resource_path('PRMS.db'))))
        con=sqlite3.connect(database=os.path.join(os.getcwd(), resource_path(r'PRMS.db')))
        cur=con.cursor()
        try:
            cur.execute("Select pat_id,name,phone from patient")
            rows=cur.fetchall()
            self.patient_table.delete(*self.patient_table.get_children())
            for row in rows:
                self.patient_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)        
    
            
    def search(self):
        permission.interact_with_database((os.path.join(os.getcwd(), resource_path('PRMS.db'))))
        con=sqlite3.connect(database=os.path.join(os.getcwd(), resource_path(r'PRMS.db')))
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input is required",parent=self.root)
            else:        
                cur.execute("select tp_id,tp_name,tp_code,tp_price from treatment where tp_name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Intervention_Table.delete(*self.Intervention_Table.get_children())
                    for row in rows:
                        self.Intervention_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.Intervention_Table.focus()
        content=(self.Intervention_Table.item(f))  
        row=content['values']
        self.var_tp_id.set(row[0])
        self.var_tp_name.set(row[1])
        self.var_code.set(row[2])
        self.var_price.set(row[3])
    
    def get_patient_data(self,ev):
        f=self.patient_table.focus()  
        content=(self.patient_table.item(f))    
        row=content['values'] 
        self.var_cname.set(row[1])
        self.var_contact.set(row[2])
                   
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))  
        row=content['values']
        self.var_tp_id.set(row[0])
        self.var_tp_name.set(row[1])
        self.var_code.set(row[2])
        self.var_price.set(row[3])  
                       
    def add_update_cart(self):
        if  self.var_tp_id.get()=='':
            messagebox.showerror('Error',"Please select Intervention from the List",parent=self.root)            
        elif self.var_price.get()=='':
            messagebox.showerror('Error',"Price is Required",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())   
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_tp_id.get(),self.var_tp_name.get(),self.var_code.get(),price_cal]
            
            #=========update cart===============
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_tp_id.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Intervention already present\nDo you want to Add | Remove from the Bill List",parent=self.root)
                if op==True:
                    if self.var_code.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #add existing intervention
                        self.cart_list.append(cart_data)
                        #self.cart_list[index_][2]=price_cal #price
                        #update price in row 3 of bill magement table
                        #self.cart_list[index_][3]=self.var_price.get()
            else:                   
                self.cart_list.append(cart_data)
                
            self.show_cart()
            self.bill_updates()
            
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(int(row[3]))#price is row 2 in cart list
        self.discount=(self.bill_amnt*0)/100   
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.configure(text=f'Bill Amount(XAF)\n{str(self.bill_amnt)}')
        self.lbl_net_pay.configure(text=f'Net Pay(XAF)\n{str(self.net_pay)}')
        self.cartTitle.configure(text=f"Cart \t Total Interventions: [{str(len(self.cart_list))}]")
        
        
            
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Patient Details are required, Select Patient info from All Patients",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add interventions to Patient bill!!!",parent=self.root)
        else:
            #======BILL TOP=====
            self.bill_top()
            #======BILL MIDDLE======
            self.bill_middle()
            #======BILL BOTTOM======
            self.bill_bottom()
            messagebox.showinfo('Congrats',"Bill have been generated",parent=self.root)
            
    
    
    
    def bill_top(self):
        self.invoice=str(time.strftime("%d%m%Y"))
        
        bill_top_temp=f'''
        \t\tEMMANUEL DENTAL CLINIC
\t Phone No: (+237)677170167/697122782, Douala  \n\t\tTradex - Bonamoussadi\n\t\twww.emmanueldentalcare.org
{str("="*52)}
 Patient Name: {self.var_cname.get()}
 Ph No. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*52)}
 Interventions\t\t\tCode\t\tPrice
{str("="*52)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
        self.txt_bill_area.image_create("1.0",image=self.bill_img)
        
        
              
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*52)}
 BIll Amount\t\t\t\t\tXAF.{self.bill_amnt}
 Discount\t\t\t\t\tXAF.{self.discount}
 Net Pay\t\t\t\t\tXAF.{self.net_pay}
{str("="*52)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
 
    def bill_middle(self):
        try:
            for row in self.cart_list:
                name=row[1]
                price=int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END, "\n " + name + "\n\t\t\t" + row[2] + "\n\t\t\t\t\t\\XAF." + price)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
            
    def clear_cart(self):
        self.var_tp_id.set('')
        self.var_tp_name.set('')
        self.var_price.set('')
        self.var_code.set('')  
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.configure(text=f"Cart \t Total Product: [0]")
        self.lbl_amnt.configure(text=f'Bill Amount(XAF)\n [0]')
        self.lbl_net_pay.configure(text=f'Net Pay(XAF)\n [0]')
        self.var_search.set('')
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()   
        
    def update_date_time(self): 
        time_ = time.strftime("%H:%M:%S")
        date_ = time.strftime("%d:%m:%Y")
        self.lbl_clock.configure(text=f"Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200, self.update_date_time)
        

    def exit(self):
        self.is_running = False
        self.root.destroy()

   
        
        
        '''self.is_running that is set to True when the 
        application starts and is set to False 
        when the application exits. The update_date_time 
        function checks this flag before scheduling the 
        next update. If the flag is False, the function 
        returns without scheduling the next update, breaking 
        the loop and preventing the recursion error.'''

        
            
    def print_bill(self):
        file_path=os.path.join(os.getcwd(), resource_path(f'bill\\{str(self.invoice)}.txt'),'w')
        if not os.path.exists(file_path):
            fp=open(file_path)
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been saved in backend",parent=self.root)
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root) 
            new_file=tempfile.mktemp('.txt')  
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')  
        else:
             op=messagebox.askyesno('Bill Exist',"This patient invoice already exist, Do you want to create a new one?",parent=self.root)
             if op==True:
                fp=open(file_path)
                fp.write(self.txt_bill_area.get('1.0',END))
                fp.close()
                messagebox.showinfo('Saved',"Bill has been saved in backend",parent=self.root)
                messagebox.showinfo('Print',"Please wait while printing",parent=self.root) 
                new_file=tempfile.mktemp('.txt')  
                open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
                os.startfile(new_file,'print')
            
    
if __name__=="__main__":
    root=ctk.CTk()
    obj=BillClass(root)
    root.mainloop()