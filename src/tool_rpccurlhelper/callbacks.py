import datetime
import subprocess
import logging
import json
from functools import partial

# just to get thru debugging
try:
    import pyperclip
except ImportError:
    pass

from pywebio import output, pin

from .const import *

def generate_command():
    """ Reads the pin values and generates the curl command """

    username = pin.pin[PIN_USERNAME]
    password = pin.pin[PIN_PASSWORD]

    if "" in (username, password):
        output.toast("Please enter a username and password", color='danger')
        return

    method = pin.pin[PIN_METHOD_SELECT]
    params = pin.pin['params']

    if params == '':
        params = None

    return format_RPC_call(
        username=username,
        password=password,
        ip_address=DEFAULT_NODE_IP_ADDRESS,
        port=DEFAULT_NODE_PORT,
        method=method,
        params=params
        )


# # @output.use_scope('commands', clear=True)
# def generate_and_add_command():

#     # whole = {
#     #     "command": cmd,
#     #     "formatted": out
#     # }

#     add_command( command )

# def generate_and_run_command():
#     generate_command()

#     run_command( cmd )

# def add_command( cmd: str ):
#     """ Saves the command to the saved_commands list"""
#     logging.debug(f"save_command({cmd})")

#     # inspired by:
#     # pin.pin['feescroller'] = f"block: {bdx} --> fee: {block_fee:,}\n" + pin.pin["feescroller"]

#     # if globals.saved_commands == []:
#     #     globals.saved_commands = [cmd]
#     # else:
#     #     globals.saved_commands = [cmd].append(globals.saved_commands)

#     globals.saved_commands.append(cmd)

#     logging.debug(f"globals.saved_commands:")
#     for i in range(0, len(globals.saved_commands)):
#         logging.debug(f"globals.saved_commands[{i}]: {globals.saved_commands[i]}")


@output.use_scope('history')
# def add_command( command: str, run: bool=False ):
def add_command( run: bool=False ):
    """ Displays the command on a table row with buttons to the TOP of 'history' scope """

    command = generate_command()
    # this happens when the user clicks the "add" button without entering a username and password
    if command == None:
        return

    logging.debug(f"add_command({command})")

    # convert the current time to string
    timenow_str = datetime.datetime.now().strftime("%H%M%S%f")

    output.put_table([
        [
            output.span(pin.pin[PIN_METHOD_SELECT], col=2)
            # output.span(method, col=2),
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
    ], position=output.OutputPosition.TOP)

    if run:
        run_command(command)

# def copy_to_clipboard( cmd: str ):
#     """ Copies the command to the clipboard """
#     logging.debug(f"copy_to_clipboard({cmd})")

#     pyperclip.copy(cmd)
#     output.toast(f"Command copied to clipboard\n\n\n{cmd}", color='success')

@output.use_scope('output', clear=True)
def run_command( cmd: str ):
    """ Runs the command in the terminal and displays the output in the 'output' scope """
    # logging.debug(f"run_command():\n{cmd}\n")

    with output.put_loading(color='success', scope='command_output', position=output.OutputPosition.TOP):
        res = subprocess.run(f"{cmd} | jq", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output.put_markdown(f"# Output:")

    if res.returncode != 0:
        output.put_text(f"ERROR:\n{res.stderr}\nCheck the username and password")
        return

    # parse the json output
    error = None
    try:
        res_json = json.loads(res.stdout)

        error = res_json.get("error")
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
    data_binary['id'] = 'plebtools' # TODO turn this into an advanced option
    data_binary['method'] = f"{method}"
    if params != None:
        params = params.split(' ')
        data_binary['params'] = [ int(p) if p.isdigit() == True else p for p in params ]
    else:
        data_binary['params'] = []

    # true if string is a number
    # is_number = lambda s: s.replace('.', '', 1).isdigit()

    everything = "curl -s --user " + user_string + " --data-binary " + f"'{json.dumps(data_binary)}'" + " -H 'content-type: text/plain;' " + f"http://{ip_address}:{port}/"
    logging.debug(f"_format_RPC_call() returning: \n{everything}")
    return everything

# @output.use_scope('params', clear=True)
# def method_select_callback( selected_method ):
#     output.put_text("additional params")

#     if selected_method == "getblockhash":
#         pin.put_input(name='param1', label="Argument #1 - height", help_text="\nType: numeric, required. The height index", value="0")


@output.use_scope('help', clear=True)
def clear_params( throwaway ):
    pin.pin['params'] = ''
    logging.debug(f"{pin.pin[PIN_METHOD_SELECT]=}")
    ht = BLOCKCHAIN_RPCS.get( pin.pin[PIN_METHOD_SELECT] )

    output.put_collapse("Description", [
        output.put_markdown(ht)
        ], open=False)

