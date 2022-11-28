# import os
# import pywebio

# from OSINTofBlockchain.Apps import start_thread

# from . import web_interface

# APP_TITLE = "Treasury Management Simulator"

# def main():
#     pywebio.config(title=APP_TITLE, theme='dark')

#     if os.getenv('NO_SERVER') == '1':
#         # TODO - this way of running the project won't respond to exit(0)... why the fuck?  no idea...
#         start_thread(web_interface.show_interface)
#     else:
#         # TODO TODO TODO - this should be called SSH_COMPATIBLE instead of NO_SERVER...   this should NOT be the default behaviour....
#         # TODO - I do it this way because if you're running it on your node over SSH the webpage won't automatically open
#         # Also, this script won't exit when you close the webpage otherwise - probably something to do with the thread running session.hold()
#         pywebio.start_server(lambda: start_thread(web_interface.show_interface), port=8080, debug=True)

from .web_interface import main
