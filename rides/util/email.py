from imap_tools import MailMessage


def process_tmobile(email: MailMessage) -> str:
    pass


def process_email(seen_emails: set, email: MailMessage) -> set:
    '''Returns seen emails'''
    key = str((email.from_, email.date_str))
    seen_emails.add(key)
    
    domain = email.from_.split('@')[-1]
    match domain:
        case 'tmomail.net':
            text = process_tmobile(email)
        case _:
            # TODO: Unsupported
            text = ''
            pass

    return seen_emails, text
