import permission
import sqlite3
import datetime
import time
import sys
import os
from datetime import datetime
from plyer import notification

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def main():
        # Your logic here
            try:
                permission.interact_with_database((resource_path('PRMS.db')))
                con=sqlite3.connect(database=resource_path(r'PRMS.db'))
                cur = con.cursor()
                cur.execute("SELECT * FROM schedules")
                schedules = cur.fetchall()
                con.close()
                for schedule in schedules:
                    name, date = schedule
                    appointment_date = datetime.strptime(date, "%d-%m-%Y")
                    current_date = datetime.now()
                    current_date = datetime.strptime(current_date,"%d-%m-%Y")
                    if current_date == appointment_date:
                         notification.notify(title='Appointment Reminder', message=f'You Have an Appointment Scheduled Today with Mr.Mrs {name}', timeout=30)
                    else:
                        pass
                    while current_date < appointment_date:
                        try:
                            time_diff = appointment_date - current_date
                            days_diff = time_diff.days
                            if days_diff > 0:
                                if days_diff == 1:
                                    message = f'You have an appointment with {name} tomorrow.'
                                elif days_diff == 2:
                                    message = f'You have an appointment with {name} in 2 days.'
                                elif days_diff == 3:
                                    message = f'You have an appointment with {name} in 3 days.'
                                elif days_diff >= 7:
                                    message = f'You have an appointment with {name} in a week.'
                                else:
                                    message = f'You have an appointment with {name} in {days_diff} days.'
                                
                                time.sleep(time_diff.total_seconds())
                                notification.notify(title='Appointment Reminder', message=message, timeout=30)
                            else:
                                notification.notify(title='Appointment Reminder', message=f'Appointment Date with {name} has already passed', timeout=30)
                            
                            current_date = datetime.now()  # Update the current date
                        except Exception as ex:
                            notification.notify(title='Appointment Reminder', message=f"Error due to : {str(ex)}", timeout=30)    
                            time.sleep(60)  # Check every minute
            except Exception as ex:
                notification.notify(title='Error',message=f"Error due to : {str(ex)}",timeout=30)    
    
main()