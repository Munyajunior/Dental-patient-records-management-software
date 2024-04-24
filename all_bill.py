from tkinter import*
from customtkinter import*
import customtkinter as ctk
from PIL import Image,ImageTk
from tkinter import messagebox
import permission
import os
import sys
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class V_billClass(ctk.CTk):
    def __init__(self,root):
        self.root=root
        self.root.state('zoomed')
        screen_width=self.root.winfo_screenwidth()
        screen_height=self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width-50}x{screen_height-100}')
        self.root.iconbitmap(resource_path('icon.ico'))
        self.root.title("SmileScribePro")
        #=================Variables============
        
        self.bill_list=[]
        self.var_invoice=StringVar()
        
        
        #=========title====================
        lbl_title=ctk.CTkLabel(self.root,text="View Patient Bills",font=("goudy old style",30),fg_color="#184a45",text_color=("#fff","#00f")).pack(side=TOP,fill=X,padx=10,pady=10)
        
        lbl_invoice=ctk.CTkLabel(self.root,text="Invoice No.",font=("arial black",16),text_color=("#125","#fff")).place(x=50,y=100)
        lbl_invoice=ctk.CTkEntry(self.root,textvariable=self.var_invoice,font=("calibri",15),fg_color="lightyellow",width=180,height=28).place(x=160,y=100)
        
        btn_search=ctk.CTkButton(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),text_color="white",hover_color="#184a45",bg_color="#2196f3",width=120,height=28,corner_radius=0).place(x=360,y=100)
        btn_clear=ctk.CTkButton(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),text_color="white",hover_color="#184a45",bg_color="#2196f3",width=120,height=28,corner_radius=0).place(x=490,y=100)
        
        
        #========================Bill List=======================
        vbill_list_frame=ctk.CTkFrame(self.root)
        vbill_list_frame.place(x=50,y=140)
        
        
        self.v_bill_list=Listbox(vbill_list_frame,font=("goudy old style",15),bg="white",width=30,height=20)
        scrolly=Scrollbar(vbill_list_frame,orient=VERTICAL)
        scrollx=Scrollbar(vbill_list_frame,orient=HORIZONTAL)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.pack(side=BOTTOM,fill=X)
        self.v_bill_list.configure(yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrolly.configure(command=self.v_bill_list.yview)
        scrollx.configure(command=self.v_bill_list.xview)
        self.v_bill_list.pack(fill=BOTH,expand=1)
        self.v_bill_list.bind("<ButtonRelease-1>",self.get_data)
        
        #===============BILL AREA==============
        
        vbill_frame=ctk.CTkFrame(self.root)
        vbill_frame.place(x=400,y=140)
        
        lbl_title2=Label(vbill_frame,text="Patient Bill Area",font=("goudy old style",20),width=20).pack(side=TOP,fill=X)
        scrolly2=Scrollbar(vbill_frame,orient=VERTICAL)
        scrollx2=Scrollbar(vbill_frame,orient=HORIZONTAL)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrollx2.pack(side=BOTTOM,fill=X)
        
        
        self.bill_area=ctk.CTkTextbox(vbill_frame,bg_color="lightyellow",width=430,height=420)
        self.bill_area.configure(yscrollcommand=scrolly2.set,xscrollcommand=scrollx2.set)
        scrollx2.configure(command=self.bill_area.xview)
        scrolly2.configure(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        
        #====================Images===============
        self.bill_photo=ctk.CTkImage(dark_image=Image.open(resource_path("images\\bill.jpeg")),
                                     light_image=Image.open(resource_path("images\\bill.jpeg")),
                                     size=(300,250))
        lbl_image=ctk.CTkLabel(self.root,image=self.bill_photo)
        lbl_image.place(x=900,y=140)
        
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        
        self.show()
        permission.interact_with_database((resource_path('PRMS.db')))
#==========================Functions=============================================   
    def show(self):
        del self.bill_list[:]
        self.v_bill_list.delete(0,END)
        #print(os.listdir('..\IMS')) bill1.txt, category.py
        for i in os.listdir('bill'):
            #print(i.split('.'),i.split('.')[-1]) 
            if i.split('.')[-1]=='txt':
                self.v_bill_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])
    
    def get_data(self,ev):
        index_=self.v_bill_list.curselection()
        file_name=self.v_bill_list.get(index_)
        #print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill\\{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()
        
    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice No. is required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                print("yes find the invoice")
                fp=open(f'bill\\{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        self.var_invoice.set("")            
                
                
        
if __name__=="__main__":
    root=ctk.CTk()
    obj=V_billClass(root)
    root.mainloop()