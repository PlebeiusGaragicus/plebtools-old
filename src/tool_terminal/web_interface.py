from pywebio import output

from . import config
from .callbacks import *


def main_page(menu_callback: callable):

    output.clear('app')
    with output.use_scope('main', clear=True):
        output.put_button("<<- Main Menu", color='danger', onclick=menu_callback)
        output.put_markdown(f"# {config.APP_TITLE}")

        output.put_text("nothing yet...")
