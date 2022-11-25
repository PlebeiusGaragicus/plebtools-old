from pywebio import output, config

from .const import *
from .callbacks import *

# def cleanup( menu_callback: callable ):
#     output.clear('output')
#     output.clear('history')
#     output.clear('help')
#     menu_callback()

@config(title=APP_TITLE, theme='dark')
def main():
    # output.clear('app')
    with output.use_scope('main', clear=True):
        # output.put_button("<<- Main Menu", color='danger', onclick=lambda: cleanup(menu_callback))
        output.put_markdown(f"# {APP_TITLE}")
        # doing it this way will open the link in a new tab
        # output.put_link() # TODO use this function instead...
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

        options = list(BLOCKCHAIN_RPCS.keys())
        pin.put_select(PIN_METHOD_SELECT, options=options, label="RPC Command")
        pin.put_input(name='params', label="Additional Parameters", help_text="", value="")
        pin.pin_on_change(PIN_METHOD_SELECT, onchange=clear_params, init_run=True)


        output.put_row([
            output.put_button("Format command", color='info', onclick=lambda: add_command( run=False )),
            output.put_button("Format and run!", color='danger', onclick=lambda: add_command( run=True ))
        ])
        output.put_markdown(f"# Command history:")
