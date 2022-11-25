import os
import logging

import Adafruit_IO

# TODO - write the documentation ;)
# I need to include the required environment variables in the documentation
# very important!
ADAFRUIT_USER_ENV: str = 'ADAFRUIT_USERNAME'
ADAFRUIT_TOKEN_ENV: str = 'ADAFRUIT_APITOKEN'

class AdafruitUser:
    """ You can init this class with any user/api_token or...
            leave the init parameters blank to pull from environment variables
                so, ensure you run `dotenv.load_dotenv()` before setting up
    """
    # these are the names of the environment variables that AdafruitIOHelper
    # will look for during initialization if they are not supplied
    user_name: str
    api_token: str

    def __init__(self, user_name: str = None, api_token: str = None):
        if user_name == None:
            user_name = os.getenv(ADAFRUIT_USER_ENV)
            if user_name == None:
                raise Exception(f"{ADAFRUIT_USER_ENV} environment variable not given and not supplied")
        self.user_name = user_name

        if api_token == None:
            api_token = os.getenv(ADAFRUIT_TOKEN_ENV)
            if api_token == None:
                raise Exception(f"{ADAFRUIT_TOKEN_ENV} environment variable not given and not supplied")
        self.api_token = api_token



def send_to_feed(feed_name: str, value, user: AdafruitUser = None) -> bool:
    logging.info(f"Adafruit_IO_Helper.send({feed_name=}, {value=})")

    if user == None:
        user = AdafruitUser()

    aio = Adafruit_IO.Client(user.user_name, user.api_token)

    # we have to do this because Adafruit will replace a dot '.' with literally '-dot-' *sigh*
    feed_name_ada_friendly = feed_name.replace('[', '')
    feed_name_ada_friendly = feed_name_ada_friendly.replace(']', '')
    feed_name_ada_friendly = feed_name_ada_friendly.replace('.', '-dot-')

    try:
        ret = aio.send(feed_name_ada_friendly, value)
    except Adafruit_IO.errors.RequestError:
        logging.exception("ADAFRUIT ERROR: YOU PROBABLY HAVE THE WRONG FEED NAME, ... OR YOUR API KEY IS WRONG... could be a few things...")
        return False
    
    logging.info(f"Adafruit_IO_Helper.send() returns:\n{ret}")

    return True



# if __name__ == "__main__":
#     import dotenv
#     dotenv.load_dotenv()
#     print( os.getenv( AdafruitUser.ADAFRUIT_USER_ENV ) )
#     print( os.getenv( AdafruitUser.ADAFRUIT_TOKEN_ENV ) )

#     user = AdafruitUser()
#     print(user.user_name, user.api_token)

#     user = AdafruitUser(user_name="some user", api_token="TOKENZZZZSCHWEE")
#     print(user.user_name, user.api_token)

#     # TODO - ask for feed name etc etc and try to update a feed below...
#         # this way we can test this module
