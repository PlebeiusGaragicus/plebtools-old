#!/usr/bin/env python3

import sys
import os
import logging
import dotenv

from flask import Flask, render_template
import pywebio

from . import config
from . import tool_dashboard
from . import tool_rpccurlhelper
from . import tool_miningcalcs
from . import tool_opreturn

app = Flask(__name__)
# TODO tidy up
# app = Flask(__name__,
#             static_url_path='', 
#             static_folder='web/static',
#             template_folder='web/templates')

@app.route("/")
def index():
    return render_template("index.html", title=config.APP_TITLE)


def setup_logging() -> None:
    # TODO - how to have multiple env files...? one for debug?  Pass in the env file as a command line arg?
    # dotenv.load_dotenv(".env")

    if os.getenv("DEBUG") == "1":
        config.DEBUG = True

    logging.basicConfig(
        # level=logging.DEBUG if config.DEBUG else logging.INFO, # TODO put this back once it's done, done
        level=logging.DEBUG,
        format="%(name)s [%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",

        ### TODO CRASHED! PermissionError: [Errno 13] Permission denied: '/debug.log'
        handlers=[logging.FileHandler("debug.log", mode='a'), logging.StreamHandler(sys.stdout)] if config.DEBUG == True else [logging.StreamHandler(sys.stdout)],
    )

    if config.DEBUG:
        #logging.getLogger("pywebio").addHandler([logging.StreamHandler(sys.stdout), logging.FileHandler("debug.log", mode='a')])
        logging.getLogger("pywebio").addHandler(logging.StreamHandler(sys.stdout))

    # don't log the tornado webserver stuff
    logging.getLogger("tornado.access").setLevel(logging.WARNING)

    logging.info("DEBUG MODE: {}".format(config.DEBUG))
    logging.debug("arguments: {}".format(sys.argv))



if __name__ == "__main__":
    setup_logging()

    app.add_url_rule('/dashboard', 'dashboard', pywebio.platform.flask.webio_view( tool_dashboard.main ), methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
    app.add_url_rule('/curl_formatter', 'curl_formatter', pywebio.platform.flask.webio_view( tool_rpccurlhelper.main ), methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
    app.add_url_rule('/mining_calcs', 'mining_calcs', pywebio.platform.flask.webio_view( tool_miningcalcs.main ), methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
    app.add_url_rule('/opreturn', 'opreturn', pywebio.platform.flask.webio_view( tool_opreturn.main ), methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)

    # OLD WAY OF DOING THINGS
    # # https://pywebio.readthedocs.io/en/latest/platform.html?highlight=start_thread#pywebio.platform.tornado_http.start_server
    # # pywebio.platform.tornado_http.start_server(main_page.main_page, port=config.PORT, debug=config.DEBUG, cdn=False)
    # pywebio.platform.tornado_http.start_server(
    #     main_menu.main_menu,
    #     host="0.0.0.0",
    #     # auto_open_webbrowser=True, # TODO don't use when debugging... it's annoying!
    #     # open_webbrowser_tab=True,
    #     port=config.PORT,
    #     debug=config.DEBUG,
    #     cdn=False)
