import os
import logging

import dotenv

from cdot.answer import a

# from . import AdafruitIO
# from . import BraiinsPool
# from . import twilio

from . import myAPI


def update_all_workers():
    """ TODO assume you have a feed name that is called user.worker?
        TODO - write the documentation ;)

    """

    print(f"THE ANSWER TO LIFE IS {a}")

    workers_and_hashrate = myAPI.BraiinsPool.list_workers_and_metric(metric='hash_rate_scoring')

    success = [ myAPI.AdafruitIO.send_to_feed(feed_name=n, value=v) for n, v in workers_and_hashrate ]
    logging.debug(f"{workers_and_hashrate}")
    logging.debug(f"{success=}")

    # format a text message based on results:
    #   user.worker1=hashrate
    #   user.worker2=hashrate
    res = [ f"{n}={round(v,1)}\n" for n, v in workers_and_hashrate ]
    msg = ''.join(res)

    receiving_number = os.getenv('NOTIFY_NUMBER')
    if receiving_number == None:
        raise Exception("NO RECEIVING NUMBER IS SET")
    else:
        logging.info(f"{receiving_number=}")

    twilio.SMS(message=msg, receiving_number=receiving_number)

    if False in success:
        logging.info("ERRORS OCCURRED")
    else:
        logging.info("SUCCESS")



if __name__ == "__main__":
    dotenv.load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
        handlers=[logging.StreamHandler(),
                    logging.FileHandler('./debug.log', mode='a')])


    logging.debug(f"{os.getenv(AdafruitIO.ADAFRUIT_USER_ENV)=}")
    logging.debug(f"{os.getenv(AdafruitIO.ADAFRUIT_TOKEN_ENV)=}")
    logging.debug(f"{os.getenv(BraiinsPool.BRAIINS_TOKEN_ENV)=}")
    logging.debug(f"{os.getenv(twilio.TWILIO_SID_ENV)=}")
    logging.debug(f"{os.getenv(twilio.TWILIO_TOKEN_ENV)=}")
    logging.debug(f"{os.getenv(twilio.TWILIO_PHONE_NUMBER_ENV)=}")
    logging.debug(f"{os.getenv('NOTIFY_NUMBER')=}")

    update_all_workers()
