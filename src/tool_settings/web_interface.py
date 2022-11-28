import logging
from pywebio import output, pin, config

from .config import *
from .callbacks import *

def load_settings():
    logging.debug("Setting are loaded ;)") # but not really.


@config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_table([[
            output.span([
                output.put_markdown("## Bitcoin Core RPC Settings"),
                output.put_text("This allows PlebTools to access a node and pull blockchain data.  This is more text and I want to see how it wraps etc, etc, etc....  Fill this out completely so that it can span and span and span...!!! <3 <3")
            ], col=4)
        ],[
            pin.put_input('bitcoin_user', type='text', label="username"),
            pin.put_input('bitcoin_pass', type='text', label="password")
        ],[
            pin.put_input('bitcoin_ip', type='text', label="ip address"),
            pin.put_input('bitcoin_port', type='text', label="port")
        ]])
