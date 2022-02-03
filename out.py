# modules
import smtplib
from email.message import EmailMessage

# content
msg_body = "Kairos Rides"

# action
msg = EmailMessage()
msg['subject'] = 'test'
msg['from'] = sender
msg['to'] = reciever
msg.set_content(msg_body)

host = 'smtp.gmail.com'
port = 465
server = smtplib.SMTP_SSL(host, port)
server.login(username, password)
server.sendmail(username, reciever, msg.as_string())
server.quit()