import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

def send_email(receiver, sender, sender_pw, subject, message_str):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver

    message.attach(MIMEText(message_str, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender, sender_pw)
            server.sendmail(sender, receiver, message.as_string())
            print('Email sent.')
        except Exception as e:
            print('Email failed to send.')
            print(e)


def main():

    RECEIVER_EMAIL=input("who are you sending email to: ")
    SENDER_EMAIL=input("what is your email: ")
    SENDER_PASSWORD=getpass()

    subject = 'test'

    message_str = '''Something went wrong on the webpage
    - test 1 failed
    - test 2 passed
    - test 3 passed
    - test 4 failed
    - test 5 passed
    - test 6 failed
    '''

    send_email(RECEIVER_EMAIL, SENDER_EMAIL, SENDER_PASSWORD, subject, message_str)


if __name__ == '__main__':
    main()
