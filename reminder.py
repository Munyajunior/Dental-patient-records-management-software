import argparse
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import win32pipe, win32file, pywintypes
import permission
import sqlite3
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

PIPE_NAME = 'mypipe'
'''This Python script is a Windows service that reminds 
the user of an appointment. It uses the win32serviceutil.ServiceFramework 
to create a service that runs in the background. 
The service is named 'ReminderService'.'''

class ReminderService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ReminderService'
    _svc_display_name_ = 'Reminder Service'

    def __init__(self,args=None):
        ''' Initializes the service and sets the 
        is_alive flag to True.'''
        if args is None:
            # If no arguments are provided, start the service automatically
            args = ['start']
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.is_alive = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        '''Stops the service and sets the is_alive flag to False. '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.hWaitStop = False
        

    def SvcDoRun(self):
        '''Logs a message when the service starts.'''
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        while self.hWaitStop:
            try:
                handle = win32file.CreateFile(
                    r'\\.\pipe\{}'.format(PIPE_NAME),
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
                res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
                if res == 0:
                    print(f"SetNamedPipeHandleState")
                    return
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
           

    def show_reminder(self, root, name, appointment_date):
        ''' Shows a reminder for an appointment. It calculates 
        the time difference between the current time and the 
        appointment time, and if the time difference is 
        positive, it waits until it's time to show the 
        reminder. If the appointment date has already passed,
        it shows an error message.'''
        # Calculate the time difference between now and the appointment date
        appointment_date = datetime.strptime(appointment_date, "%d-%m-%Y")
        reminder_date = appointment_date - timedelta(days=2)
        time_diff = reminder_date - datetime.now()
        time_diff_in_sec = time_diff.total_seconds()

        # If the time difference is positive, wait until it's time to show the reminder
        if time_diff_in_sec > 0:
            time.sleep(time_diff_in_sec)
            messagebox.showinfo("Reminder", "You have an appointment with {} in 2 days.".format(name))
            
        else:
            messagebox.showerror("Error","Appointment Date has already passed please enter a future date",parent=self.root)

        # Create a root window and hide it
        root.withdraw()

        
        # Destroy the root window
        root.destroy()

    def schedule_reminder(self, name, appointment_date):
        ''' Schedules the show_reminder function to run every 
        day at a specific time (09:00). It checks 
        if there's a task scheduled for the current 
        moment and runs it.'''
        # Schedule the show_reminder function to run every day at a specific time
        schedule.every().day.at("09:00").do(self.show_reminder, name, appointment_date)

        while True:
            # Check if there's a task scheduled for the current moment and run it
            schedule.run_pending()
            time.sleep(1)

    
        
        
        
    def run_with_args(self):
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM schedules")
            schedules=cur.fetchall()
            con.close()
            for schedule in schedules:
                name,date = schedule
             # Parse command-line arguments
            parser = argparse.ArgumentParser(description='Show a reminder for an appointment.')
            parser.add_argument('--name', required=True, help='The name of the person who has an appointment.')
            parser.add_argument('--date', required=True, help='The date of the appointment in the format dd-mm-yyyy.')

            args = parser.parse_args()
            self.schedule_reminder(args.name, args.date)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)    
           

        
if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ReminderService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ReminderService)
        
        
'''In the main function, it checks if the script is 
running as a service or as a standalone script. 
If it's running as a service, it initializes the 
service manager and starts the service control dispatcher. 
If it's running as a standalone script, it handles the 
command line arguments and creates an instance of 
ReminderService''' 
    
        
   