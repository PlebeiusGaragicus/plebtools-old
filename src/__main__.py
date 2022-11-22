#!/usr/bin/env python3

import sys
import os
import logging
import dotenv

import pywebio

from . import config
from .tool_hello import web_interface

def setup_logging() -> None:
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


def read_candy():
    datadir = "/root/assets/"

    try:
        candyfile = os.path.join(datadir, "candy")
        logging.error("candyfile: {}".format(candyfile))
        with open(candyfile, "r") as f:
            logging.error("CANDY: {}".format(f.read()))
    except FileNotFoundError:
        logging.error("CANDY FILE NOT FOUND")


def main():
    setup_logging()

    read_candy()


    # https://pywebio.readthedocs.io/en/latest/platform.html?highlight=start_thread#pywebio.platform.tornado_http.start_server
    # pywebio.platform.tornado_http.start_server(main_page.main_page, port=config.PORT, debug=config.DEBUG, cdn=False)
    pywebio.platform.tornado_http.start_server(
        web_interface.main_page,
        host="0.0.0.0",
        auto_open_webbrowser=True,
        # open_webbrowser_tab=True,
        port=config.PORT,
        debug=config.DEBUG,
        cdn=False)


if __name__ == "__main__":
    main()
