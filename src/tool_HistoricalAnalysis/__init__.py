import os
import pywebio

from PlebTools.Apps import start_thread

from . import web_interface

APP_TITLE = "Block clock"

def main():

    pywebio.config(title=APP_TITLE, theme='dark')

    if os.getenv('SSH_COMPATIBLE') == '1':
        pywebio.start_server(lambda: start_thread(web_interface.show_interface), port=8080)
    else:
        start_thread(web_interface.show_interface)
