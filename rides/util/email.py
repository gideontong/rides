from bs4 import BeautifulSoup
from imap_tools import MailMessage
from typing import Tuple


def process_tmobile(email: MailMessage) -> str:
    soup = BeautifulSoup(email.html, 'html.parser')
    text = soup.body.get_text()
    return ' '.join(text.split())


def process_verizon(email: MailMessage) -> str:
    if len(email.attachments) > 0:
        return email.attachments[0].payload.decode('utf-8')
    else:
        return ''


def process_sprint(email: MailMessage) -> str:
    soup = BeautifulSoup(email.html, 'html.parser')
    text = soup.pre.get_text()
    return ' '.join(text.split())


def process_ting(email: MailMessage) -> str:
    if len(email.attachments) > 0:
        return email.attachments[0].payload.decode('utf-8')
    else:
        return ''


def process_email(seen_emails: set, email: MailMessage) -> Tuple[set, str]:
    '''Returns seen emails'''
    key = str((email.from_, email.date_str))
    seen_emails.add(key)
    
    domain = email.from_.split('@')[-1]
    match domain:
        case 'tmomail.net':
            text = process_tmobile(email)
        case 'vzwpix.com':
            text = process_verizon(email)
        case 'pm.sprint.com':
            text = process_sprint(email)
        case 'mailmymobile.net':
            text = process_ting(email)
        case _:
            # TODO: Unsupported
            text = ''
            pass

    print(key, text)
    return seen_emails, text
