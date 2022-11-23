#!/usr/bin/env python3

import sys
import os
import logging
import dotenv

import pywebio

from . import config
from . import main_menu

def setup_logging() -> None:
    # TODO - how to have multiple env files...? one for debug?  Pass in the env file as a command line arg?
    # dotenv.load_dotenv(".env")

    if os.getenv("DEBUG") == "1":
        config.DEBUG = True
    
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        #format="%(asctime)s %(levelname)s %(message)s",
        format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
        handlers=[logging.FileHandler("debug.log", mode='a'), logging.StreamHandler(sys.stdout)],
    )

    if config.DEBUG:
        #logging.getLogger("pywebio").addHandler([logging.StreamHandler(sys.stdout), logging.FileHandler("debug.log", mode='a')])
        logging.getLogger("pywebio").addHandler(logging.StreamHandler(sys.stdout))

    # don't log the tornado webserver stuff
    logging.getLogger("tornado.access").setLevel(logging.WARNING)

    logging.info("DEBUG MODE: {}".format(config.DEBUG))
    logging.debug("arguments: {}".format(sys.argv))


    logging.warning("hello... is this going to be in the docker logs?")



if __name__ == "__main__":
    setup_logging()

    # https://pywebio.readthedocs.io/en/latest/platform.html?highlight=start_thread#pywebio.platform.tornado_http.start_server
    # pywebio.platform.tornado_http.start_server(main_page.main_page, port=config.PORT, debug=config.DEBUG, cdn=False)
    pywebio.platform.tornado_http.start_server(
        main_menu.main_menu,
        #host="0.0.0.0",
        auto_open_webbrowser=True,
        # open_webbrowser_tab=True,
        port=config.PORT,
        debug=config.DEBUG,
        cdn=False)
