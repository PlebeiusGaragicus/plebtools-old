import datetime
import subprocess
import requests
import logging
import json
from functools import partial

from src.api.authproxy import AuthServiceProxy

import pyperclip

from pywebio import output, pin

from .const import *

def generate_command():
    """ Reads the pin values and generates the curl command """

    username = str( pin.pin[PIN_USERNAME] )
    password = str( pin.pin[PIN_PASSWORD] )

    if "" in (username, password):
        output.toast("Please enter a username and password", color='danger')
        return

    ip_address = str( pin.pin[PIN_HOST] )
    port = str( pin.pin[PIN_PORT] )

    if "" in (ip_address, port):
        output.toast("Please enter an IP address and port", color='danger')
        return

    method = str( pin.pin[PIN_METHOD_SELECT] )
    params = pin.pin['params']

    if params == '':
        params = None

    return format_RPC_call(
        username=username,
        password=password,
        ip_address=ip_address,
        port=port,
        method=method,
        params=params
        )


def add_command( run: bool=False ):
    """ Displays the command on a table row with buttons to the TOP of 'history' scope """

    command = generate_command()
    # this happens when the user clicks the "add" button without entering a username and password
    if command == None:
        return

    logging.debug(f"add_command({command})")

    # convert the current time to string
    timenow_str = datetime.datetime.now().strftime("%H%M%S%f")

    with output.use_scope('history'):
        output.put_table([
            [
                output.span(pin.pin[PIN_METHOD_SELECT], col=2)
            ],
            [
                output.span(pin.put_textarea(name=timenow_str, value=f"{command}", readonly=True, rows=5, code=True) ),
                # pin.put_textarea(name=timenow_str, value=f"{command}", readonly=True, rows=5, code=True),
                # output.put_button("run", color='info', onclick=lambda: run_command(globals.saved_commands[i])),
                # output.put_button("run", color='info', onclick=partial(run_command, cmd=globals.saved_commands[i])),
                output.put_button("run", color='info', onclick=partial(run_command, cmd=command)),
                # output.put_button("copy", onclick=lambda: copy_to_clipboard(globals.saved_commands[i]))
                output.put_button("copy", onclick=lambda: pyperclip.copy(command))
                # output.put_button("delete", color='danger', onclick=lambda: delete_command(cmd_index=i))
            ],
        ], position=output.OutputPosition.BOTTOM)

    output.scroll_to(scope='history', position=output.Position.BOTTOM)

    if run:
        # run_command(command)
        req_command()

# def copy_to_clipboard( cmd: str ):
#     """ Copies the command to the clipboard """
#     logging.debug(f"copy_to_clipboard({cmd})")

#     pyperclip.copy(cmd)
#     output.toast(f"Command copied to clipboard\n\n\n{cmd}", color='success')

@output.use_scope('output', clear=True)
def run_command( cmd: str ):
    """ Runs the command in the terminal and displays the output in the 'output' scope """

    with output.put_loading(color='success', scope='command_output', position=output.OutputPosition.TOP):
        res = subprocess.run(f"{cmd} | jq", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # res = requests.post(f"{cmd}")

        # TODO - DON'T BE A NOOB AND PLEASE WRITE BETTER PYTHON CODEZ...!! <3 <3
        # https://stackoverflow.com/questions/12943819/how-to-prettyprint-a-json-file
        # print(json.dumps(parsed, indent=4))

    output.put_markdown(f"# Output:")

    if res.returncode != 0:
        output.put_text(f"ERROR:\n{res.stderr}\nCheck the username and password")
        return

    # error = None
    try:
        res_json = json.loads(res.stdout)

        # error = res_json.get("error")
    except json.decoder.JSONDecodeError as e:
        # output.toast("Error: Invalid JSON - NO OUTPUT - likely a user auth error", color='danger')
        res_json = None

    logging.debug(f"result.returncode: {res.returncode}")
    logging.debug(f"result.stdout: {res.stdout}")
    logging.debug(f"result.stderr: {res.stderr}")

    # count the number of lines in res
    num_lines_res = len(res.stdout.splitlines())

    if res_json == None:
        output.put_text("ERROR:\nNo output.\nCheck the username and password.")
    else:
        # BUG - outputs that are too big (like getblock with verbosity=2) cause the page to crash
        # note: readonly must be false so that the user can copy the text
        # pin.put_textarea(name='res', value=res.stdout, readonly=False, rows=max(num_lines_res, 4), code=True)
        output.put_text(res.stdout)

    output.scroll_to(scope='output', position=output.Position.BOTTOM)






def req_command():
    username = str( pin.pin[PIN_USERNAME] )
    password = str( pin.pin[PIN_PASSWORD] )

    if "" in (username, password):
        # output.toast("Please enter a username and password", color='danger')
        return

    ip_address = str( pin.pin[PIN_HOST] )
    port = str( pin.pin[PIN_PORT] )

    if "" in (ip_address, port):
        # output.toast("Please enter an IP address and port", color='danger')
        return

    method = str( pin.pin[PIN_METHOD_SELECT] )
    params = pin.pin['params']

    if params == '':
        params = None


    rpc_url = f"http://{username}:{password}@{ip_address}:{port}"
    ap = AuthServiceProxy(rpc_url)

    # res = ap.method

    # if res.status_code != 200:
    #     output.toast(f"Error: {res.status_code} - {res.reason}", color='danger')
    #     # logging.error(f"Error: {res.raw}")
    #     return

    output.put_text(res)


# def req_command():
#     username = str( pin.pin[PIN_USERNAME] )
#     password = str( pin.pin[PIN_PASSWORD] )

#     if "" in (username, password):
#         # output.toast("Please enter a username and password", color='danger')
#         return

#     ip_address = str( pin.pin[PIN_HOST] )
#     port = str( pin.pin[PIN_PORT] )

#     if "" in (ip_address, port):
#         # output.toast("Please enter an IP address and port", color='danger')
#         return

#     method = str( pin.pin[PIN_METHOD_SELECT] )
#     params = pin.pin['params']

#     if params == '':
#         params = None

#     # r = requests.get(f"https://pool.braiins.com/accounts/workers/json/btc/")

#     # send a request to the RPC server
#     res = requests.post(f"http://{ip_address}:{port}", auth=(username, password), json={"method": method, "params": params})

#     if res.status_code != 200:
#         output.toast(f"Error: {res.status_code} - {res.reason}", color='danger')
#         # logging.error(f"Error: {res.raw}")
#         return
    
#     output.put_text(res.text)





def use_cookie_callback( opt: str ):
    """ Callback for the use cookie checkbox
        This function makes the username input box read only and sets the username to '__cookie__'
        or, if unchecked, enables the username input box and sets the username to '' (blank)
    """

    logging.debug(f"use_cookie_callback({opt})")

    if opt == ["Use cookie file"]:
        pin.pin[PIN_USERNAME] = '__cookie__'
        pin.pin_update(PIN_USERNAME, readonly=True)
        pin.pin_update(PIN_PASSWORD, label="secret cookie")
    else:
        pin.pin_update(PIN_USERNAME, readonly=False)
        pin.pin[PIN_USERNAME] = ''
        pin.pin_update(PIN_PASSWORD, label="password")

############################################################
def format_RPC_call(username: str, password: str, ip_address: str, port: str, method: str, params) -> str:
    logging.debug(f"_format_RPC_call({method=}, {params=})")

    user_string = username + ':' + password

    data_binary = {}
    data_binary['jsonrpc'] = '1.0'
    data_binary['id'] = 'plebtools' # TODO turn this into an advanced option?
    data_binary['method'] = f"{method}"
    if params != None:
        params = params.split(' ')
        # if the param is a number, type-cast it to int to prevent double quotes from surrounding it
        # else, it's a string (a block hash, for example) and curl needs double quotes around it
        data_binary['params'] = [ int(p) if p.isdigit() == True else f"{p}" for p in params ]
    else:
        data_binary['params'] = []

    everything = "curl -s --user " + user_string + " --data-binary " + f"'{json.dumps(data_binary)}'" + " -H 'content-type: text/plain;' " + f"http://{ip_address}:{port}/"
    logging.debug(f"_format_RPC_call() returning: \n{everything}")
    return everything

@output.use_scope('help', clear=True)
def clear_params( throwaway ):
    pin.pin['params'] = ''
    logging.debug(f"{pin.pin[PIN_METHOD_SELECT]=}")
    ht = BLOCKCHAIN_RPCS.get( str( pin.pin[PIN_METHOD_SELECT] ) )

    output.put_collapse("Description", [
        output.put_markdown(ht)
        ], open=False)
