from bs4 import BeautifulSoup
from imap_tools import MailMessage
from rides.util.log import logger
from typing import Tuple


def decode_attachments(email: MailMessage) -> str:
    res = ''
    for attachment in email.attachments:
        if attachment.filename.endswith('.txt'):
            res += attachment.payload.decode('utf-8') + ' '
    return res


def process_tmobile(email: MailMessage) -> str:
    soup = BeautifulSoup(email.html, 'html.parser')
    text = soup.body.get_text()
    return ' '.join(text.split())


def process_verizon(email: MailMessage) -> str:
    return decode_attachments(email)


def process_sprint(email: MailMessage) -> str:
    soup = BeautifulSoup(email.html, 'html.parser')
    text = soup.pre.get_text()
    return ' '.join(text.split())


def process_ting(email: MailMessage) -> str:
    return decode_attachments(email)


def process_email(seen_emails: set, email: MailMessage) -> Tuple[set, bool, str]:
    '''Returns seen emails'''
    key = str((email.from_, email.date_str))
    seen = key in seen_emails
    logger.debug(f'Processing an email from {email.from_} at {email.date_str}')
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

    return seen_emails, seen, text
