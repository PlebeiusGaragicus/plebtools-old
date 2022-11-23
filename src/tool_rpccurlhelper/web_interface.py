from pywebio import output

from .config import *
from .callbacks import *

def cleanup( menu_callback: callable ):
    output.clear('table')
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
        pin.pin_on_change(PIN_USE_COOKIE, use_cookie_callback)
        pin.put_select(PIN_CMD_SELECT, options=BLOCKCHAIN_RPCS, label="RPC Command")

        output.put_button("Generate", onclick=generate)

        # pin.put_textarea(PIN_GENERATED_CMD, label="Generated RPC Curl commands", readonly=True, value="", rows=5)
        # output.put_table
        # pin.put_actions()
