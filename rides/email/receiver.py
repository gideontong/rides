from imap_tools import MailBox
from email.header import decode_header


def retrieve(host: str, username: str, password: str):
    '''Retrieve recent messages from the server'''

    with MailBox(host).login(username, password) as mailbox:
        for email in mailbox.fetch(limit=2, reverse=True, mark_seen=False):
            print(email.date)