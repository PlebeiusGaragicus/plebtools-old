import os
import sys
import threading
import logging

import pywebio

from OSINTofBlockchain.Apps.TreasurySimulator import web_interface
#from AppFrontEnd import web_interface


def cleanup():
    """ We call exit to stop the python script and kill the server.
        This gets called when the user closes the tab.
        Close tab -> kill script

    """

    logging.info("The web page was closed - goodbye")
    print("The web page was closed - goodbye")
    exit(0)


def run_calculator():
    """ This function is called by PyWebIO's start_server to get the whole website up and running

    """

    pywebio.session.set_env(title="bitcoin mining profit calculator")

    # we'll make our own thread to keep everything running after the page is 'loaded' and all my python finishes
    # then, we just use callbacks on the input items/buttons to run the dynamic content/results/popups
    t = threading.Thread(group=None, target=pywebio.session.hold)
    pywebio.session.register_thread( t )
    t.start()
    pywebio.session.defer_call(cleanup)

    web_interface.show_user_interface()
    web_interface.refresh()

    # this is where the python script 'ends'
    # everything has been setup and we have a thread running that will call cleanup() when it exits
    # ...good bye ;)


def calculator():
    """ This is the "main" function of this module and is called from the 'run' shell script in the top directory of this project

        This will display an ip address (eg http://192.168.4.71:8080/) in the terminal which the user has to click on / copy-paste into a web browswer

        It can be changed to open automatically.. which actually may be better.. but I can't remember why I picked this way - it's probably in some comment somehwere...
        # TODO look into above line

    """

    # remember: any logging calls before this line will run basicConfig with stupid, default settings and mess up our ability to setup our logger.  Only log from here on down
    if os.getenv('DEBUG') == '1':
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
            handlers=[
                # THIS ENSURES THAT WHAT'S PRINTED TO THE SCREEN COMES IN AS STDOUT, NOT STDERROR - SO THAT I CAN INCLUDE THE 2>/DEV/NULL LINE IN THE .RUN SCRIPT... OH YEAH BABY
                # refer to logging/__init__.py lines 1056-1057: "if stream is None: stream = sys.stderr"
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('debug.log', mode='w')])
        logging.debug("debugging is enabled!")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s] - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('debug.log', mode='w')])
        logging.info("logging for INFO and above...")

    if os.getenv('NO_SERVER') == '1':
        # TODO - this way of running the project won't respond to exit(0)... why the fuck?  no idea...
        run_calculator()
    else:
        # TODO - I do it this way because if you're running it on your node over SSH the webpage won't automatically open
        # Also, this script won't exit when you close the webpage otherwise - probably something to do with the thread running session.hold()
        pywebio.start_server(run_calculator, port=8080, debug=True)




if __name__ == "__main__":
    calculator()











# def calculator(arguments: list = None):
#     """ This is the "main" function of this module and is called from the 'run' shell script in the top directory of this project

#         This will display an ip address (eg http://192.168.4.71:8080/) in the terminal which the user has to click on / copy-paste into a web browswer

#         It can be changed to open automatically.. which actually may be better.. but I can't remember why I picked this way - it's probably in some comment somehwere...
#         # TODO look into above line

#     """
#     # fun fact: this will print out ['-c'] because that is the trigger (argument) given to python in the run shell script - THE MORE YOU KNOW!
#     #print(sys.argv[:1])

#     # the first argument is going to be 'calculator', which we can throw away
#     if arguments == None:
#         arguments = []
#     else:
#         arguments = arguments[1:]

#     # TODO - getopt is kicking my butt
#     # how do i want this to work?
#     # I do want it to give an error on a bad entry... that was it's more generalizable to other apps?
#     # nah, I shouldnt care about that..
#     # https://docs.python.org/3/library/getopt.html
#     # https://docs.python.org/3/library/getopt.html
#     # https://docs.python.org/3/library/getopt.html
#     # https://docs.python.org/3/library/getopt.html
#     # https://docs.python.org/3/library/getopt.html

#     logginglevel = logging.INFO

#     #try:
#     #opts, args = getopt.getopt(args=arguments, shortopts='', longopts=['help', 'debug', 'rpcip=', 'rpcuser='])
#     #opts, args = getopt.getopt(arguments, 'c:', ['condition=', 'output-file=', 'testing'])
#     #opts, args = getopt.getopt(args=arguments, shortopts='', longopts=['help', 'debug'])

#     # print(f"{opts=}")
#     # print(f"{args=}")

#     #except getopt.GetoptError as err:
#         #print("SOMETHING WAS SUPPLIED BUT NOT SUPPLIED...")
#         #print(err)
#         #print(CLI_USAGE_HELP)
#         #exit(1)

#     given_arguments = {}
#     accepted_arguments = ['-help', '-debug', '-rpc-user', '-rpc-pass', '-local', '-data-dir']
#     # for t in arguments:
#     #     #print(f"{t=}")
#     #     #print(f"{ t.split('=')[0] }")
#     #     #try:
#     #     t0 = t.split('=')[0]
#     #     #print(f"{t0=}")
#     #     if t0 not in accepted_arguments:
#     #         # if you pass something that is not caught here... YOU DIE !!!!
#     #         print(f"ERROR: given argument '{t0}' is not supported.")
#     #         print(CLI_USAGE_HELP)
#     #         exit(1)
#     #     #except Exception as e:
#     #     #    print(e.with_traceback)

#     #     if t == '--help':
#     #         print(CLI_USAGE_HELP)
#     #         exit(0)

#     #     if t == '--debug':
#     #         print("Calculator running in debug mode!  (AKA more logging!!!)")
#     #         logginglevel = logging.DEBUG

#     #     #try:
#     #     if t0 == '--rpc-user':
#     #         t1 = f"{t.split('=')[1]}"
#     #         given_arguments[t0] = t1
#     #         print(f"ACCEPTED ARGUMENT: '{t0}' as {t.split('=')[1]}")
#     #     #except Exception as e:
#     #     #    print(e.with_traceback)

#     for t in arguments:
#         t0 = t.split('=')[0]

#         if t0 not in accepted_arguments:
#             # if you pass something that is not caught here... YOU DIE !!!!
#             print(f"ARGUMENT REJECTED: '{t0}' is not supported.")
#             print(CLI_USAGE_HELP)
#             #exit(1) # doesn't fucking work??!?? WHY NOT?! the server still starts up!!
#             #sys.exit(1)
#             #os._exit(1)
#             #exit(0)
#         else:
#             try:
#                 t1 = f"{t.split('=')[1]}"
#             except IndexError:
#                 t1 = True

#             given_arguments[t0] = t1
#             print(f"ARGUMENT ACCEPTED: '{t0}' as {t1}")

#     #print("WHY") # this will print out when any of the above exit(1) functions are called... but WHY!!!?!?!?

#     # go through the sorted list that we made and do things
#     for item in given_arguments.keys():
#         if item == '-debug':
#             print("Calculator running in debug mode!  (AKA more logging!!!)")
#             logginglevel = logging.DEBUG

#         if item == '-help':
#             print(CLI_USAGE_HELP)
#             exit(0)


#         if item == '-local':
#             pass

#         if item == '-data-dir':
#             print('yum - wheres that cookie?')
#             print( f"""{ os.popen(f"cat '{given_arguments['-data-dir']}'/.cookie").read()= }""" )
        
#         #     #try to load cookie
#         #     cookie = os.popen(f"cat {arg}/.cookie").read()
#         #     cookie = cookie.split(':')
#         #     config.cookie = cookie[1]
#         #     print(f"cookie: {cookie}")
#         # elif opt == '--luxor':
#         #     config.apikey = arg
#         # elif opt == '--rpcip':
#         #     config.RPC_ip_port = arg
#         # elif opt == '--rpcuser':
#         #     config.RPC_user_pass = arg

#     log_format = "[%(levelname)s] - %(message)s"
#     if logginglevel == logging.DEBUG:
#         log_format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s"

#     # remember: any logging calls before this line will run basicConfig with stupid, default settings and mess up our ability to setup our logger.  Only log from here on down
#     logging.basicConfig(
#         level=logginglevel,
#         format=log_format,
#         handlers=[logging.StreamHandler(),
#                   logging.FileHandler('debug.log', mode='a')])

#     logging.debug(f"{arguments=}")

#     # if not None in (config.RPC_ip_port, config.RPC_user_pass):
#     #     config.RPC_enabled = True
#     #     logging.info(f"using supplied RPC ip/port of {config.RPC_ip_port}")
#     #     logging.info(f"using supplied RPC user/pass of {config.RPC_user_pass}")

#     # if config.apikey != None:
#     #     logging.info(f"Luxor API key: {config.apikey}")

#     # TODO - I do it this way because if you're running it on your node over SSH the webpage won't automatically open
#     # Also, this script won't exit when you close the webpage otherwise - probably something to do with the thread running session.hold()
#     pywebio.start_server(run_calculator, port=8080, debug=True)

