from imap_tools import MailBox, MailMessage
from typing import FrozenSet, List


def retrieve(host: str, username: str, password: str, numbers: FrozenSet[str], limit: int = 20) -> List[MailMessage]:
    '''Retrieve recent messages from the server'''

    with MailBox(host).login(username, password) as mailbox:
        emails = list()
        for email in mailbox.fetch(limit=limit, reverse=True, mark_seen=False):
            if any(number in email.from_ for number in numbers):
                emails.append(email)
    
    return emails
