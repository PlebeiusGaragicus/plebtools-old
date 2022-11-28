import logging
import dotenv

from myAPI import TwilioHelper

def test_twilio_full():
    dotenv.load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
        handlers=[logging.StreamHandler()])

    print("E164 format: [+] [country code] [subscriber number including area code]")
    print("example 1123456789")
    rn = input("Enter the recieving phone number to run this test: +")

    TwilioHelper.SMS(message="If you get this text - then it WORKS!", receiving_number=rn)
