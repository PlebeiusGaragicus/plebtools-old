import logging
import json

import pywebio
from pywebio import output, pin

from . import config
from .callbacks import *

def save_settings():
    """Save settings to file"""
    with open(config.SETTINGS_FILE, 'w') as f:
        json.dump(config.settings, f, indent=4)

def load_settings():
    """Load settings from file"""
    try:
        with open(config.SETTINGS_FILE, 'r') as f:
            config.settings = json.load(f)
    except FileNotFoundError:
        logging.warning("No settings file found, creating a new blank one")
        config.settings = {
            # bitcoin core rpc settings
            'RPC_USER': '',
            'RPC_PASS': '',
            'RPC_HOST': '127.0.0.1',
            'RPC_PORT': '8332',

            # braiins pool api
            'BRAIINS_TOKEN': ''
        }
        save_settings()


def save_inputs():
    """Save inputs to settings"""
    config.settings['RPC_USER'] = pin.pin['RPC_USER']
    config.settings['RPC_PASS'] = pin.pin['RPC_PASS']
    config.settings['RPC_HOST'] = pin.pin['RPC_HOST']
    config.settings['RPC_PORT'] = pin.pin['RPC_PORT']

    config.settings['BRAIINS_TOKEN'] = pin.pin['BRAIINS_TOKEN']

    save_settings()

    output.toast("Settings saved")

@pywebio.config(title=config.APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {config.APP_TITLE}")

        output.put_table([[
            output.span([
                output.put_markdown("## Bitcoin Core RPC Settings"),
                output.put_text("This allows PlebTools to access a node and pull blockchain data.  This is more text and I want to see how it wraps etc, etc, etc....  Fill this out completely so that it can span and span and span...!!! <3 <3")
            ], col=4)
        ],[
            pin.put_input('RPC_USER', type='text', label="username"),
            pin.put_input('RPC_PASS', type='text', label="password")
        ],[
            pin.put_input('RPC_HOST', type='text', label="ip address"),
            pin.put_input('RPC_PORT', type='text', label="port")
        ],[
            output.span([
                output.put_markdown("## Braiins Pool Token"),
                output.put_text("Get this from the Braiins pool web interface.")
            ], col=4)
        ],[
            output.span(
                pin.put_input('BRAIINS_TOKEN', type='text', label="Braiins Pool Token")
            , col=4)
        ]])

        # output.put_table([[
        #     output.span([
        #         output.put_markdown("## Braiins Pool Token"),
        #         output.put_text("Get this from the Braiins pool web interface.")
        #     ], col=4)
        # ],[
        #     pin.put_input('BRAIINS_TOKEN', type='text', label="Braiins Pool Token")
        # ]]).style('margin-top: 20px; justify-self: center;')

        output.put_button('Save', onclick=save_inputs, color="success")

    load_settings()
    pin.pin_update(name='RPC_USER', value=config.settings['RPC_USER'])
    pin.pin_update(name='RPC_PASS', value=config.settings['RPC_PASS'])
    pin.pin_update(name='RPC_HOST', value=config.settings['RPC_HOST'])
    pin.pin_update(name='RPC_PORT', value=config.settings['RPC_PORT'])
    pin.pin_update(name='BRAIINS_TOKEN', value=config.settings['BRAIINS_TOKEN'])
