# modules
import smtplib
from email.message import EmailMessage

def send(host: str, port: str, sender: str, password: str, reciever: str, message: str) -> bool:
    msg = EmailMessage()
    msg['subject'] = 'test subject'
    msg['from'] = sender
    msg['to'] = reciever
    msg.set_content(message)

    server = smtplib.SMTP_SSL(host, port)
    server.login(sender, password)
    server.sendmail(sender, reciever, msg.as_string())
    server.quit()
    