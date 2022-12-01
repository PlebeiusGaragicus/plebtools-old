from pywebio import output, config

from .config import *
from .callbacks import *

APP_TITLE = "Currency converter"
APP_DESCRIPTION = "Convert between bitcoin and fiat currencies"

@config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_link(name='Return to main menu', url="./")
        output.put_markdown("---")
        output.put_markdown(f"# {APP_TITLE}")
        output.put_text(APP_DESCRIPTION)
        output.put_markdown("---")

    currency_converter()
