from pywebio import output, config

from .config import *
from .callbacks import *


@config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_text("nothing yet...")
