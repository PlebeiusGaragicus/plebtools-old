import os
import logging

import pywebio
from pywebio import output

from . import config
from . import tool_dashboard
from . import tool_rpccurlhelper
from . import tool_nopreader

def read_candy():
    datadir = "/root/assets/"

    try:
        candyfile = os.path.join(datadir, "candy")
        logging.error("candyfile: {}".format(candyfile))
        with open(candyfile, "r") as f:
            logging.error("CANDY: {}".format(f.read()))
    except FileNotFoundError:
        logging.error("CANDY FILE NOT FOUND")

    output.put_text("check the logs...")


def nothing():
    output.put_text("nothing happens")


@pywebio.config(title=config.APP_TITLE, theme='dark')
def main_menu():

    with output.use_scope("main", clear=True):
        if config.DEBUG:
            output.put_text(f"DEBUG: {config.DEBUG}"),

        output.put_markdown(f"# {config.APP_TITLE}")

        # when this is used the callback is given the text of the button pressed
        # output.put_buttons(["Refresh", "or"], onclick=refresh)
        output.put_button("Dashboard", onclick=lambda: tool_dashboard.web_interface.main_page(main_menu))
        output.put_button("NO OP Return Reader", onclick=lambda: tool_nopreader.web_interface.main_page(main_menu))
        # ... TESTING ...
        output.put_button("RPC Curl Formatter", onclick=lambda:tool_rpccurlhelper.web_interface.main_page(main_menu))
        output.put_button("terminal", onclick=nothing)
        output.put_button("eat candy", read_candy)
