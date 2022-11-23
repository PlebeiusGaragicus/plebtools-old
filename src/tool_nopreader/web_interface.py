import pywebio
from pywebio import output

from . import config
# from .callbacks import *

def web_interface():
    pass

@pywebio.config(title=config.MENU_TITLE, theme='dark')
def main_page(menu_callback: callable):

    with output.use_scope("main", clear=True):
        output.put_button("<<- Main Menu", color='danger', onclick=menu_callback)
        output.put_markdown(f"# {config.MENU_TITLE}")
        # when this is used the callback is given the text of the button pressed
        # output.put_buttons(["Refresh", "or"], onclick=refresh)
