from tkinter import*
import customtkinter as ctk
from customtkinter import*
from tkinter import messagebox
from PIL import Image
from patient import patientClass
from intervention import interventionClass
from all_bill import V_billClass
from bill import BillClass
from consultation import ConsultationClass
from appointment import appointmentClass
from proforma import ProformaClass
from quotes import quoteClass
from archives import archiveClass
from cashbook import cashBookClass
import permission
import sqlite3
import os
import sys
import time
import ctypes
import winreg
from infi.systray import SysTrayIcon

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
 

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class MyTabView(ctk.CTkTabview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.commands = {}

    def add(self, text, command=None):
        super().add(text)
        if command is not None:
            self.commands[text] = command

    def select(self, tab):
        super().select(tab)
        command = self.commands.get(tab)
        if command is not None:
            command()


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the protocol for what happens when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Check if lbl_clock exists before trying to cancel the after command
        if hasattr(self.master, 'lbl_clock') and hasattr(self.master, 'id'):
            self.master.lbl_clock.after_cancel(self.master.id)
        # Then destroy the window
        self.destroy()
 

class SmilescribePro(ctk.CTk):
    def __init__(self,root,icon_path="icon.ico"):
      if not is_admin():
          ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
          sys.exit()
      else:
        self.root = root
        self.systray = None
        self.icon_path = icon_path
        self.root.state('zoomed')
        # Bind the exit method to the window's close button
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        screen_width=self.root.winfo_screenwidth()
        screen_height=self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}')
        self.root.iconbitmap(resource_path('icon.ico'))
        self.root.title("SmileScribePro")
        # Set the window to open in fullscreen
        #self.root.attributes('-fullscreen', True)
        # Maximize the window while keeping the title bar
        self.windows = []
        self.is_clicked=False
        self.tab_view = MyTabView(self.root,)
        self.tabs = ["Main", "Consultation", "Patient Records", 
                    "Interventions", "Appointments", "Billing", 
                    "Proforma", "All Bills","Quotes","Archives","Cash Book"]
        x_offset = 0
        self.tab_view.pack(anchor='w',fill='x')
        for tab in self.tabs:
            button = ctk.CTkButton(self.tab_view, text=tab, 
                            command=lambda tab=tab: self.on_tab_selected(tab),
                            font=("helvetica",12,"bold"),corner_radius=0)
            button_width = button.winfo_reqwidth()  # Get the width of the button
            button.place(x=x_offset, y=0)
            x_offset += button_width + 2  # Add extra space after each button
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
    ).place(anchor='nw', x=0, y=25)
        #=============Btn_Logout================================
        # Calculate the position of the button based on the screen size
        x_position = screen_width - 100  # Adjust this value as needed
        y_position = screen_height - 735  # Adjust this value as needed
        btn_logout = ctk.CTkButton(self.root,text="Exit"
                                    ,command=self.exit
                                    ,font=("calibri",20,"bold")
                                    ,fg_color=("#273c75","#353b48")
                                    ,hover_color="#e84118"
                                    ,height=50,width=screen_width-1200
                                    ,corner_radius=0
                                    ).place(anchor='e', x=x_position, y=60)
        #======================Clock============================
        self.lbl_clock=ctk.CTkLabel(self.root,text="Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS"
                                    ,font=("calibri",18,"bold")
                                    ,fg_color=("#487eb0","#4d636d"),bg_color="#fff"
                                    ,width=screen_width
                                    ,text_color="#fff")
        self.lbl_clock.place(x=0,y=90)
        
        #====================Content==============================  
        x_patient_position = screen_width - 1130  # Adjust this value as needed
        y_patient_position = screen_height - 568  
        self.lbl_patient=ctk.CTkLabel(self.root,text="Total Patients\n[ 0 ]"
                                        ,text_color=("#fff","#1e272e")
                                        ,fg_color=("#33bbf9","#34e7e4")
                                        ,bg_color="white"
                                        ,font=("goudy old style",20,"bold")
                                        ,height=150,width=300)
        self.lbl_patient.place(x=200,y=200)
        x_bill_position = screen_width - 810  # Adjust this value as needed
        y_bill_position = screen_height - 568 
        self.lbl_bill=ctk.CTkLabel(self.root,text="Total BIlls\n[ 0 ]"
                                    ,text_color=("#fff","#1e272e")
                                    ,fg_color=("#ff5722","#58B19F")
                                    ,bg_color="white"
                                    ,font=("goudy old style",20,"bold")
                                    ,height=150,width=300)
        self.lbl_bill.place(x=530,y=200)
        x_appointment_position = screen_width - 490  # Adjust this value as needed
        y_appointment_position = screen_height - 568  
        self.lbl_appointment=ctk.CTkLabel(self.root,text="Total Appointments\n[ 0 ]"
                                            ,text_color=("#fff","#1e272e")
                                            ,fg_color=("#3c40c6","#ccae62")
                                            ,bg_color="white"
                                            ,font=("goudy old style",20,"bold")
                                            ,height=150,width=300)
        self.lbl_appointment.place(x=860,y=200)
        x_proforma_position = screen_width - 1130  # Adjust this value as needed
        y_proforma_position = screen_height - 400 
        self.lbl_proforma=ctk.CTkLabel(self.root,text="Total Proforma\n[ 0 ]"
                                        ,text_color=("#fff","#1e272e")
                                        ,fg_color=("#ffdd59","#c7ecee")
                                        ,bg_color="white"
                                        ,font=("goudy old style",20,"bold")
                                        ,height=150,width=300)
        self.lbl_proforma.place(x=200,y=400)
        self.lbl_archives=ctk.CTkLabel(self.root,text="Total Archives\n[ 0 ]"
                                        ,text_color=("#fff","#1e272e")
                                        ,fg_color=("#eb4d4b","#f0932b")
                                        ,bg_color="white"
                                        ,font=("goudy old style",20,"bold")
                                        ,height=150,width=300)
        self.lbl_archives.place(x=530,y=400 )
        self.lbl_quotes=ctk.CTkLabel(self.root,text="All Quotes\n[ 0 ]"
                                        ,text_color=("#fff","#1e272e")
                                        ,fg_color=("#be2edd","#22a6b3")
                                        ,bg_color="white"
                                        ,font=("goudy old style",20,"bold")
                                        ,height=150,width=300)
        self.lbl_quotes.place(x=860,y=400 )
                
        #==================Footer================
        date_=time.strftime("%Y")
        lbl_footer=ctk.CTkLabel(self.root,text=f"Copyright @ {date_} RootTech", font=("times new roman",12,"bold")).pack(side=BOTTOM,fill=X)
        permission.interact_with_database((resource_path('PRMS.db')))
        self.update_content() 
        self.start()
        self.add_to_startup(resource_path('main.py'))        
      #=============================ALL FUNCTIONS==================
    def start(self):
        menu_options = (("Show/Hide", None, self.toggle_window),)
        self.systray = SysTrayIcon(self.icon_path, "SmileScribePro", menu_options, self.on_quit_callback)
        self.systray.start()
        
    def add_to_startup(self, file_path):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, 'SmileScribePro', 0, winreg.REG_SZ, file_path)
               
    def on_tab_selected(self, tab_name):
      # Destroy any existing toplevel windows
      for win in self.windows:
         win.destroy()
      self.windows = []
      if not self.is_clicked:
         self.is_clicked = True
         return

      # Create a new toplevel window based on the selected tab
      if tab_name == 'Main':
         return
      elif tab_name == 'Consultation':
         self.consultation()
      elif tab_name == 'Patient Records':
         self.patient()
      elif tab_name == 'Interventions':
         self.intervention()
      elif tab_name == 'Appointments':
         self.appointment()
      elif tab_name == 'Billing':
         self.bill()
      elif tab_name == 'All Bills':
         self.all_bill()
      elif tab_name == 'Proforma':
         self.proforma()
      elif tab_name =='Quotes':
          self.quotes()
      elif tab_name=='Archives':
          self.archives()
      elif tab_name=='Cash Book':
          self.cashbook()
      
        
      
    def consultation(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = ConsultationClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def patient(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = patientClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def intervention(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = interventionClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def appointment(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = appointmentClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def bill(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = BillClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def all_bill(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = V_billClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def proforma(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = ProformaClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def quotes(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = quoteClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def archives(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = archiveClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
    def cashbook(self):
        self.toplevel_window = ToplevelWindow(self.root)
        self.new_toplevel_window = cashBookClass(self.toplevel_window)
        self.windows.append(self.toplevel_window)
        self.root.after(200, self.toplevel_window.focus_set)  # Delay setting the focus
        self.toplevel_window.iconbitmap('icon.ico')
        return
        
    
    def update_content(self):
       permission.interact_with_database((resource_path('PRMS.db')))
       con=sqlite3.connect(database=resource_path(r'PRMS.db'))
       cur=con.cursor()
       try:
          cur.execute("select * from patient")
          patient=cur.fetchall()
          self.lbl_patient.configure(text=f'Total Patients\n[ {str(len(patient))} ]')
          
          bill=len(os.listdir('bill'))
          self.lbl_bill.configure(text=f'Total Bills\n[ {str(bill)} ]')
          
          proforma=len(os.listdir('proforma'))
          self.lbl_proforma.configure(text=f'Total Proforma\n[ {str(proforma)} ]')
          
          quote=len(os.listdir('Doctor_Quotes'))
          self.lbl_archives.configure(text=f'All Quotes\n[{str(quote)}]')
          
          cur.execute("select * from archives")
          archive=cur.fetchall()
          self.lbl_archives.configure(text=f'Total Archives\n[ {str(len(archive))} ]')
          
          cur.execute("select * from appointments")
          appointment=cur.fetchall()
          self.lbl_appointment.configure(text=f'Total Appointments\n[ {str(len(appointment))} ]') 
          
          if self.lbl_clock is not None:
            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d:%m:%Y")
            self.lbl_clock.configure(text=f"Welcome to SmileScribePro - Professional Patient Records Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.id = self.lbl_clock.after(200, self.update_content)      
       except Exception as ex:
            messagebox.showerror("Main Content Update Error",f"Error due to : {str(ex)}",parent=self.root)
   
    def exit(self):
        self.is_running = False
        self.root.destroy()        
    
    def toggle_window(self, systray):
        if self.root.state() == "normal":
            self.root.withdraw()
        else:
            self.root.deiconify()   
        
    def on_quit_callback(self, systray):
        self.root.quit()
   
@staticmethod
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
        
        
if __name__=="__main__":
   root =ctk.CTk()
   obj=SmilescribePro(root)
   root.mainloop()