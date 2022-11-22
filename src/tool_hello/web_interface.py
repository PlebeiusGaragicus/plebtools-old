import pywebio
from pywebio import output

from .. import config

from .callbacks import *

@pywebio.config(title=config.APP_TITLE, theme='dark')
def main_page():
    output.put_markdown(f"# {config.APP_TITLE}")

    with output.use_scope("menu", clear=True):
        # when this is used the callback is given the text of the button pressed
        # output.put_buttons(["Refresh", "or"], onclick=refresh)
        output.put_button("Refresh", onclick=refresh)

    refresh()
