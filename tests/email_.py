import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

RECEIVER_EMAIL=input("who are you sending email to: ")
SENDER_EMAIL=input("what is your email: ")
SENDER_PASSWORD=getpass()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
subject = 'Test email',

message = MIMEMultipart('alternative')
message['Subject'] = 'Test Subject'
message['From'] = SENDER_EMAIL
message['To'] = RECEIVER_EMAIL

text = 'Test body'

message.attach(MIMEText(text, "plain"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    try:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print('Email sent.')
    except Exception as e:
        print('Email failed to send.')
        print(e)