from pywebio import output, config

from .config import *
from .callbacks import *


@config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")
        output.put_button('Update All Workers', onclick=update_all_workers)


    logging.debug(f"{os.getenv('ADAFRUIT_USER_ENV')=}")
    logging.debug(f"{os.getenv('ADAFRUIT_TOKEN_ENV')=}")
    logging.debug(f"{os.getenv('BRAIINS_TOKEN_ENV')=}")
    logging.debug(f"{os.getenv('TWILIO_SID_ENV')=}")
    logging.debug(f"{os.getenv('TWILIO_TOKEN_ENV')=}")
    logging.debug(f"{os.getenv('TWILIO_PHONE_NUMBER_ENV')=}")
    logging.debug(f"{os.getenv('NOTIFY_NUMBER')=}")
