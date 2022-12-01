from pywebio import output, config

from src.node import verify_node

from .config import *
from .callbacks import *

@config(title=APP_TITLE, theme='dark')
def main():

    tip = verify_node()
    if tip == None:
        return

    with output.use_scope('main', clear=True):
        output.put_link(name='Return to main menu', url="./")
        output.put_markdown("---")
        output.put_markdown(f"# {APP_TITLE}")
        output.put_markdown(APP_DESCRIPTION)
        output.put_markdown("---")

    output.put_text(f"tip: {tip}")
