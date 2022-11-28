# import os
# import logging
# import dotenv

# from . import AdafruitIOHelper
# from . import BraiinsAPI
# from . import EmailHelper
# from . import TwilioHelper

# dotenv.load_dotenv()

# # GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
# # SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
# # STORAGE_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME')




# __all__ = [
#     "update_all_workers"
# ]

# def setup():
#     """
#         This setups up logging and grabs the environment variables

#     """

#     logging.basicConfig(
#         level=logging.DEBUG,
#         format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
#         handlers=[logging.StreamHandler(),
#                   logging.FileHandler('./debug.log', mode='a')])

#     logging.debug(f"{os.getenv('ADAFRUIT_USER')=}")
#     logging.debug(f"{os.getenv('ADAFRUIT_TOKEN')=}")
#     logging.debug(f"{os.getenv('BRAIINS_TOKEN')=}")
#     logging.debug(f"{os.getenv('TWILIO_SID')=}")
#     logging.debug(f"{os.getenv('TWILIO_TOKEN')=}")
#     logging.debug(f"{os.getenv('TWILIO_PHONE_NUMBER')=}")
#     logging.debug(f"{os.getenv('NOTIFY_NUMBER')=}")


# def update_all_workers():
#     """ TODO assume you have a feed name that is called user.worker?
#         TODO - write the documentation ;)

#     """

#     setup()

#     bhelper = BraiinsAPI.BraiinsAPIHelper()
#     workers_and_hashrate = bhelper.list_workers_and_metric('hash_rate_scoring')

#     #### SEND INFO TO ADAFRUIT
#     aio = AdafruitIOHelper.AdafruitIOHelper()

#     success = [ aio.send(n, v) for n, v in workers_and_hashrate ]
#     logging.debug(f"{workers_and_hashrate}")
#     logging.debug(f"{success=}")

#     # format a text message based on results:
#     #   user.worker1=hashrate
#     #   user.worker2=hashrate
#     res = [ f"{n}={round(v,1)}\n" for n, v in workers_and_hashrate ]
#     msg = ''.join(res)

#     receiving_number = os.getenv('NOTIFY_NUMBER')
#     if receiving_number == None:
#         raise Exception("NO RECEIVING NUMBER IS SET")
#     else:
#         logging.info(f"{receiving_number=}")

#     tw = TwilioHelper.TwilioHelper()
#     tw.SMS(msg, receiving_number)

#     if False in success:
#         logging.info("ERRORS OCCURRED")
#     else:
#         logging.info("SUCCESS")




# # def update_one_worker(worker_name: str = None):
# #     """
# #         # TODO - write the documentation ;)

# #     """

# #     setup()

# #     #### GET INFO FROM POOL
# #     if worker_name == None or worker_name == '':
# #         worker_name = input("select which miner to log by entering your poolusername.workername:  ")

# #     bhelper = BraiinsAPI.BraiinsAPIHelper()
# #     hash_rate_scoring = bhelper.query_worker_metric(worker_name, 'hash_rate_scoring')

# #     #### SEND INFO TO ADAFRUIT
# #     aio = AdafruitIOHelper.AdafruitIOHelper()
# #     success = aio.send(worker_name, hash_rate_scoring)

# #     if success:
# #         logging.info("SUCCESS")
# #     else:
# #         logging.info("ERROR")