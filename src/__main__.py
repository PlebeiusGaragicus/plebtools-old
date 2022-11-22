#!/usr/bin/env python3

import sys
import os
import logging
import dotenv

# from typing import Callable
# import threading

import pywebio

from . import config
from . import main_page

def main():
    if os.getenv("DEBUG") == "1":
        config.DEBUG = True
    
    logging.basicConfig()

    logging.error("arguments: {}".format(sys.argv))

    # how to have multiple env files...? one for debug?  Pass in the env file as a command line arg?
    # dotenv.load_dotenv(".env")

    # don't log the tornado webserver stuff
    # logging.getLogger("tornado.access").setLevel(logging.WARNING)
    # this is so that errors are printed to the console
    if config.DEBUG:
        logging.getLogger("pywebio").addHandler([logging.StreamHandler(sys.stdout, logging.FileHandler("debug.log"))])

    # refer to logging/__init__.py lines 1056-1057: "if stream is None: stream = sys.stderr"
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if config.DEBUG else logging.INFO)
    handler.setFormatter(logging.Formatter("%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s"))
    logging.getLogger().addHandler(handler)


    logging.error("hello... is this going to be in the docker logs?")
    logging.info("STARTING APP <{}>".format(config.APP_TITLE)) # but this isn't for some reason... FUCK
    logging.info("DEBUG MODE: {}".format(config.DEBUG))



    # https://pywebio.readthedocs.io/en/latest/platform.html?highlight=start_thread#pywebio.platform.tornado_http.start_server
    # pywebio.platform.tornado_http.start_server(main_page.main_page, port=config.PORT, debug=config.DEBUG, cdn=False)
    pywebio.platform.tornado_http.start_server(main_page.main_page, host="0.0.0.0", port=config.PORT, debug=config.DEBUG, cdn=False)

    # we don't need this becuase we are using a webserver
    # pywebio.session.hold()
    ## --- OR --- ##
    # t = threading.Thread(group=None, target=pywebio.session.hold)
    # pywebio.session.register_thread( t )
    # t.start()


if __name__ == "__main__":
    main()

    # # this is set inside docker-compose.yml in the environment section
    # logging.error("TEST_ENV_VAR: {}".format(os.getenv("TEST_ENV_VAR")))

    # datadir = os.getenv("HELLOWORLD_DATA_DIR")
    # if datadir is None:
    #     logging.error("HELLOWORLD_DATA_DIR is not set")
    #     datadir = "/home/umbrel/umbrel/app-data/plebtools-hello-world/data"

    # try:
    #     candyfile = os.path.join(datadir, "candy")
    #     logging.error("candyfile: {}".format(candyfile))
    #     with open(candyfile, "r") as f:
    #         logging.info("CANDY: {}".format(f.read()))
    # except FileNotFoundError:
    #     logging.error("CANDY FILE NOT FOUND")