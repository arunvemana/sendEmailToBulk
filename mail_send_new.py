import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from credits_details import info    

def send_email(sender_mail, send_to,
               email_subject,
               email_message,
               attachment_location=''):


    msg = MIMEMultipart()
    msg['From'] = sender_mail
    msg['To'] = send_to
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_message, 'html'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login(info['sender_mail'], info['password'])
        # server.login('your_login_name', 'your_login_password')
        text = msg.as_string()
        server.sendmail(sender_mail, send_to, text)
        print(f'email sent to {send_to}')
        server.quit()
    except Exception as e:
        print(e)
        print(f'email not sent to {send_to}')
        print("SMPT server connection error")
    return True


with open(info['message_file_name'],'r') as f:
    data = f.read()

for mail_id in info['send_to']:
    send_email( sender_mail=info['sender_mail'],
               send_to=mail_id,
               email_subject=info['email_subject'],
               email_message=data,
               attachment_location=info['attachment_file'])
