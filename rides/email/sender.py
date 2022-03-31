from email.message import EmailMessage
from smtplib import SMTP_SSL


def send(host: str, port: str, sender: str, password: str, reciever: str, subject: str, content: str) -> bool:
    '''Send an email message'''
    message = EmailMessage()
    message['subject'] = subject
    message['from'] = sender
    message['to'] = reciever
    message.set_content(content)

    with SMTP_SSL(host, port) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, message.as_string())
    
    return True
