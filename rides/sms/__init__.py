from rides.util import config
from rides.util.log import logger
from twilio.rest import Client


TWILIO = config['twilio']
SID = TWILIO['sid']
TOKEN = TWILIO['token']
NUMBER = TWILIO['number']

client = Client(SID, TOKEN)

def send_message(text: str, to: str):
    logger.info(f'Texting {text} to {to}')
    message = client.messages.create(body=text, from_=NUMBER, to=to)
