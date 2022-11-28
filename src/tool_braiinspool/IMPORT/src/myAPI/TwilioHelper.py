import os
import logging

from twilio.rest import Client
"""
https://www.twilio.com/docs/sms/send-messages
https://github.com/TwilioDevEd/api-snippets
https://www.twilio.com/docs/libraries/python
"""

TWILIO_SID_ENV = 'TWILIO_SID'
TWILIO_TOKEN_ENV = 'TWILIO_TOKEN'
TWILIO_PHONE_NUMBER_ENV = 'TWILIO_PHONE_NUMBER'

class TwilioUser:
    # these are the names of the environment variables that TwilioHelper
    # will look for during initialization if they are not supplied
    SID: str
    token: str
    phone_number: str

    def __init__(self, SID: str = None, token: str = None, phone_number: str = None):
        if SID == None:
            SID = os.getenv(TWILIO_SID_ENV)
            if SID == None:
                raise Exception(f"{TWILIO_SID_ENV} environment variable not given and not supplied")
        self.SID = SID

        if token == None:
            token = os.getenv(TWILIO_TOKEN_ENV)
            if token == None:
                raise Exception(f"{TWILIO_TOKEN_ENV} environment variable not given and not supplied")
        self.token = token

        if phone_number == None:
            phone_number = os.getenv(TWILIO_PHONE_NUMBER_ENV)
            if phone_number == None:
                raise Exception(f"{TWILIO_PHONE_NUMBER_ENV} environment variable not given and not supplied")
        self.phone_number = phone_number
    


def SMS(message: str, receiving_number: str, user: TwilioUser = None):
    logging.debug(f"TwilioHelper.SMS({message=}, {receiving_number=})")

    if user == None:
        user = TwilioUser()

    client = Client(user.SID, user.token)

    ret = client.messages.create(
        to=receiving_number,
        from_=user.phone_number,
        body=message)

    logging.debug(f"after text was sent... {ret=}")

