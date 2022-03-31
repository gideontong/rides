from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

responder = Flask(__name__)


@responder.route('/sms', methods=['GET', 'POST'])
def handle_sms():
    '''Send a dynamic reply to an incoming text message'''
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message('Hi!')
    elif body == 'bye':
        resp.message('Goodbye')

    return str(resp)

