from pywebio import output, config, session

from .const import *
from .callbacks import *

from src.settings import AppSettings

def cleanup( ):
    # TODO this doesn't work apparently... with the say we are running the sessions (??) look into this
    logging.debug("I HOPE THIS IS NOT GOOD-BYE FOREVER!!! <3 <3 <3")


def load_from_settings():
    appsettings = AppSettings()

    pin.pin_update(name=PIN_USERNAME, value=appsettings['RPC_USER'])
    pin.pin_update(name=PIN_PASSWORD, value=appsettings['RPC_PASS'])
    pin.pin_update(name=PIN_HOST, value=appsettings['RPC_HOST'])
    pin.pin_update(name=PIN_PORT, value=appsettings['RPC_PORT'])

@config(title=APP_TITLE, theme='dark')
def main():
    logging.debug("\n>>>> Starting app: bitcoin-cli RPC curl formatter !!!!!!!!!!!!!")
    session.defer_call(cleanup) # TODO this does not work with thread-based something sessions something something


    with output.use_scope('main', clear=True):
        output.put_link(name='Return to main menu', url="./")
        output.put_markdown("---")
        output.put_markdown(f"# {APP_TITLE}")
        # doing it this way will open the link in a new tab
        # output.put_link() # TODO use this function instead...
        output.put_markdown(APP_DESCRIPTION)
        output.put_html(f"""Refer to the official <a href="https://developer.bitcoin.org/reference/rpc/" target="_blank">RPC API Reference</a> for more information""")
        output.put_markdown("---")

        output.put_row([
            pin.put_input(name=PIN_USERNAME, label="username", value=""),#, placeholder="username"),
            pin.put_input(name=PIN_PASSWORD, label="password", value="")#, placeholder="password")
        ])
        pin.put_checkbox(name=PIN_USE_COOKIE, options=["Use cookie file"], label="", value=False)
        output.put_row([
            pin.put_input(name=PIN_HOST, label="ip address", value=DEFAULT_NODE_IP_ADDRESS),
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

    load_from_settings()
