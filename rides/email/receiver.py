from imaplib import IMAP4_SSL

from json import load
import email
from email.header import decode_header

with open('config/keys.json') as fp:
    keys = load(fp)

username = keys['email']['username']
password = keys['email']['password']

imap = IMAP4_SSL('imap.gmail.com')
imap.login(username, password)

status, messages = imap.select('INBOX')

print(status, messages)

res, msg = imap.fetch(str(int(messages[0])), '(RFC822)')

for response in msg:
    if isinstance(response, tuple):
        # parse a bytes email into a message object
        msg = email.message_from_bytes(response[1])
        # decode the email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            # if it's a bytes, decode to str
            subject = subject.decode(encoding)
        # decode email sender
        From, encoding = decode_header(msg.get("From"))[0]
        if isinstance(From, bytes):
            From = From.decode(encoding)
        print("Subject:", subject)
        print("From:", From)
        # if the email message is multipart
        if msg.is_multipart():
            # iterate over email parts
            for part in msg.walk():
                # extract content type of email
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    # get the email body
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # print text/plain emails and skip attachments
                    print(body)
                elif "attachment" in content_disposition:
                    # download attachment
                    filename = part.get_filename()
                    print(f'file is {filename}')
        else:
            # extract content type of email
            content_type = msg.get_content_type()
            # get the email body
            body = msg.get_payload(decode=True).decode()
            if content_type == "text/plain":
                # print only text email parts
                print(body)
        if content_type == "text/html":
            print('content type is html')
        print("="*100)
# close the connection and logout
imap.close()
imap.logout()