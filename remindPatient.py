import datetime
from datetime import datetime,timedelta
import schedule
from plyer import notification
import email_pass
import smtplib #pip install smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import permission
import sys
import os
import sqlite3

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




'''def reminder_send_email():
    try:
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur = con.cursor()
        cur.execute("SELECT * FROM patientRemind")
        patients = cur.fetchall()
        con.close()
        for patient in patients:
            email, date = patient
            email_=email_pass.email_.strip()
            pass_=email_pass.pass_
            # Convert the appointment date to a datetime object
            appointment_date = datetime.strptime(date, "%d-%m-%Y")
            current_date = datetime.now()
            while current_date < appointment_date:
                time_diff = appointment_date - current_date
                days_diff = time_diff.days
                future_date = current_date + timedelta(days=days_diff)
                # Define the job to be scheduled
                def job():
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = email_
                        msg['To'] = email.strip()
                        msg['Subject'] =f'Appointment Reminder\nRappel de rendez-vous'''
                        #body =f'''Dear,Cher Mr/Mrs/Mme/sir,\n\nJust to remind you that you have an appointment on {appointment_date} with your dentist.
                        #\n\nJuste pour vous rappeler que vous avez un rendez-vous le {appointment_date} avec votre dentiste'''
'''
                        msg.attach(MIMEText(body, 'plain'))

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                    
                        server.login(email_, pass_)
                        text = msg.as_string()
                        server.sendmail(email_, email, text)
                        notification.notify(title="Email Sent",message=f"Appointment Reminder Email has been sent to Patient!!!!!",timeout=45)
                        server.quit()
                    except smtplib.SMTPException as ex:
                        notification.notify(title="Patient Reminder Error",message=f"Error due to : {str(ex)}",timeout=45)
                    # Schedule the job at the reminder date
                formatted_date=future_date.strftime('%H:%M')
                schedule.every().day.at(formatted_date).do(job)
    except Exception as ex:
        notification.notify(title="Error",message=f"Error due to : {str(ex)}",timeout=45)'''        

#reminder_send_email()


def send_email(email_, pass_, email, appointment_date):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_
        msg['To'] = email.strip()
        msg['Subject'] = 'Appointment Reminder\nRappel de rendez-vous'
        body = f'''Dear,Cher Mr/Mrs/Mme/sir,\n\nJust to remind you that you have an appointment on {appointment_date} with your dentist.
        \n\nJuste pour vous rappeler que vous avez un rendez-vous le {appointment_date} avec votre dentiste'''
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_, pass_)
        server.sendmail(email_, email, text)
        notification.notify(title="Email Sent",message=f"Appointment Reminder Email has been sent to Patient!!!!!",timeout=45)
    except smtplib.SMTPException as ex:
        notification.notify(title="Patient Reminder Error",message=f"Error due to : {str(ex)}",timeout=45)

def reminder_send_email():
    try:
        permission.interact_with_database((resource_path('PRMS.db')))
        con=sqlite3.connect(database=resource_path(r'PRMS.db'))
        cur = con.cursor()
        cur.execute("SELECT * FROM patientRemind")
        patients = cur.fetchall()
        email_=email_pass.email_.strip()
        pass_=email_pass.pass_
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_, pass_)
        for patient in patients:
            email, date = patient
            # Convert the appointment date to a datetime object
            appointment_date = datetime.strptime(date, "%d-%m-%Y")
            current_date = datetime.now()
            while current_date < appointment_date:
                time_diff = appointment_date - current_date
                days_diff = time_diff.days
                future_date = current_date + timedelta(days=days_diff)
                # Schedule the job at the reminder date
                formatted_date=future_date.strftime('%H:%M')
                schedule.every().day.at(formatted_date).do(send_email, email_=email_, pass_=pass_, email=email, appointment_date=appointment_date)
        server.quit()
        con.close()
    except Exception as ex:
        notification.notify(title="Error",message=f"Error due to : {str(ex)}",timeout=45)   

reminder_send_email()
