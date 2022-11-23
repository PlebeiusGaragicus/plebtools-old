import pywebio
from pywebio import output

from . import config
from .callbacks import *

@pywebio.config(title=config.APP_TITLE, theme='dark')
def main_page(menu_callback: callable):

    with output.use_scope("main", clear=True):
        output.put_button("<<- Main Menu", color='danger', onclick=menu_callback)
        output.put_markdown(f"# {config.APP_TITLE}")
        # when this is used the callback is given the text of the button pressed
        # output.put_buttons(["Refresh", "or"], onclick=refresh)
        output.put_button("Refresh", onclick=refresh)

    refresh()
