import logging
from pywebio import output, pin, config

from .config import *
from .callbacks import *

def load_settings():
    logging.debug("Setting are loaded ;)")


@config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_table([[
            output.span(output.put_text("Bitcoin Core RPC Settings"), col=4)
        ],[
            pin.put_input('bitcoin_user', type='text', label="username"),
            pin.put_input('bitcoin_pass', type='text', label="password")
        ],[
            pin.put_input('bitcoin_ip', type='text', label="ip address"),
            pin.put_input('bitcoin_port', type='text', label="port")
        ]])
