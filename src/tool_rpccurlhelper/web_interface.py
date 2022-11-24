from pywebio import output

from .const import *
from .callbacks import *

def cleanup( menu_callback: callable ):
    output.clear('output')
    output.clear('saved_commands')
    menu_callback()

def main_page(menu_callback: callable):

    output.clear('app')
    with output.use_scope('main', clear=True):
        output.put_button("<<- Main Menu", color='danger', onclick=lambda: cleanup(menu_callback))
        output.put_markdown(f"# {APP_TITLE}")
        # doing it this way will open the link in a new tab
        output.put_html(f"""Refer to the official <a href="https://developer.bitcoin.org/reference/rpc/" target="_blank">RPC API Reference</a> for more information""")
        output.put_markdown(TOP_TEXT)
        output.put_markdown("---")

        output.put_row([
            pin.put_input(name=PIN_USERNAME, label="username", value=""),#, placeholder="username"),
            pin.put_input(name=PIN_PASSWORD, label="password", value="")#, placeholder="password")
        ])
        pin.put_checkbox(name=PIN_USE_COOKIE, options=["Use cookie file"], label="", value=False)
        output.put_row([
            pin.put_input(name=PIN_IPADDRESS, label="ip address", value=DEFAULT_NODE_IP_ADDRESS),
            pin.put_input(name=PIN_PORT, label="port", value=DEFAULT_NODE_PORT)
        ])
        pin.pin_on_change(PIN_USE_COOKIE, use_cookie_callback)
        pin.put_select(PIN_METHOD_SELECT, options=BLOCKCHAIN_RPCS, label="RPC Command")
        pin.pin_on_change(PIN_METHOD_SELECT, onchange=clear_params)
        pin.put_input(name='params', label="Additional Parameters", help_text="", value="")


        output.put_row([
            output.put_button("Format command", color='info', onclick=lambda: add_command( run=False )),
            output.put_button("Format and run!", color='danger', onclick=lambda: add_command( run=True ))
        ])
        output.put_markdown(f"# Command history:")

    # with output.use_scope('history', clear=True):
        # output.put_markdown(f"# Commands:")

    # with output.use_scope('output', clear=True):
    #     output.put_markdown(f"# Output:")

        # globals.saved_commands = []

        # pin.put_textarea(PIN_GENERATED_CMD, label="Generated RPC Curl commands", readonly=True, value="", rows=5)
        # output.put_table
        # pin.put_actions()
