import os
import logging
import json

import pyperclip

from pywebio import output, pin

from .config import *

@output.use_scope('app')
def generate():
    """ Reads the pin values and generates the curl command """

    username = pin.pin[PIN_USERNAME]
    password = pin.pin[PIN_PASSWORD]

    if "" in (username, password):
        output.toast("Please enter a username and password", color='danger')
        return

    cmd = pin.pin[PIN_CMD_SELECT]

    out = format_RPC_call(
        username=username,
        password=password,
        ip_address=DEFAULT_NODE_IP_ADDRESS,
        port=DEFAULT_NODE_PORT,
        method=cmd,
        params=None
        )

    show_command(out)
    show_saved_commands()


@output.use_scope('saved_commands', clear=True)
def show_saved_commands():
    """ Shows the saved commands in the saved_commands list """
    logging.debug("show_saved_commands()")

    if len(saved_commands) == 0:
        # output.put_markdown("---\nNo saved commands")
        return

    output.put_markdown("Saved commands:")
    for cmd in saved_commands:
        output.put_row([
            output.put_text(cmd),
            output.put_button("Delete", color='danger', onclick=lambda: delete_command(cmd))
        ])

def copy_to_clipboard( cmd: str ):
    """ Copies the command to the clipboard """
    logging.debug(f"copy_to_clipboard({cmd})")

    pyperclip.copy(cmd)
    output.toast("Command copied to clipboard", color='success')

@output.use_scope('output', clear=True)
def show_command( cmd: str ):
    """ Shows the command in the 'output' scope with a button to save the commmand to table """
    #pin.pin['feescroller'] = f"block: {bdx} --> fee: {block_fee:,}\n" + pin.pin["feescroller"]
    output.put_table([
        [output.span(output.put_text(f"{cmd}"), col=3)],
        [
            output.put_button("copy", onclick=lambda: copy_to_clipboard(cmd)),
            output.put_button("save", color='success', onclick=lambda: save_command(cmd)),
            output.put_button("run", color='info', onclick=lambda: run_command(cmd))
        ],
    ])

@output.use_scope('command_output', clear=True)
def run_command( cmd: str ):
    """ Runs the command in the terminal and displays the output in the 'command_output' scope """
    logging.debug(f"run_command({cmd})")

    # res = os.popen(cmd).read()
    res = os.popen(f"{cmd} | jq").read()

    # count the number of lines in res
    num_lines = len(res.splitlines())

    logging.debug(f"result: {res}")

    # output.put_markdown(
    #     f"""
    #     ## Command output
    #     ```sh
    #     {res}
    #     ```
    #     """)
    output.put_markdown(f"## Command output")
    # output.put_code(res, language='sh')
    pin.put_textarea(name='res', value=res, readonly=True, rows=num_lines, code=True)


def save_command( cmd: str ):
    """ Saves the command to the saved_commands list"""

    logging.debug(f"save_command({cmd})")
    saved_commands.append(cmd)

    show_saved_commands()

    # for c in saved_commands:
    #     output.put_table([
    #         [output.put_text(f"{c}")],
    #         [output.put_button("Delete this command", onclick=lambda: delete_command(c))]
    #     ])

    # output.put_text(f"Saved commands: {len(saved_commands)}")
    # for c in saved_commands:
    #     output.put_text(c)

def delete_command( cmd: str ):
    """ Deletes the command from the saved_commands list"""
    logging.debug(f"delete_command({cmd})")
    saved_commands.remove(cmd)

    show_saved_commands()


def use_cookie_callback( opt: str ):
    """ Callback for the use cookie checkbox
        This function makes the username input box read only and sets the username to '__cookie__'
        or, if unchecked, enables the username input box and sets the username to '' (blank)
    """

    logging.debug(f"use_cookie_callback({opt})")

    # if pin.pin[PIN_USE_COOKIE]:
    if opt == ["Use cookie file"]:
        pin.pin[PIN_USERNAME] = '__cookie__'
        pin.pin_update(PIN_USERNAME, readonly=True)
        pin.pin_update(PIN_PASSWORD, label="cookie file contents")
    else:
        pin.pin_update(PIN_USERNAME, readonly=False)
        pin.pin[PIN_USERNAME] = ''
        pin.pin_update(PIN_PASSWORD, label="password")

############################################################
def format_RPC_call(username: str, password: str, ip_address: str, port: str, method: str, params: list=None) -> str:
    logging.debug(f"_format_RPC_call({method=}, {params=})")

    user_string = username + ':' + password

    data_binary = {}
    data_binary['jsonrpc'] = '1.0'
    data_binary['id'] = 'plebtools' # TODO turn this into an advanced option
    data_binary['method'] = f"{method}"
    if params != None:
        data_binary['params'] = params

    everything = "curl -s --user " + user_string + " --data-binary " + f"'{json.dumps(data_binary)}'" + " -H 'content-type: text/plain;' " + f"http://{ip_address}:{port}/"
    logging.debug(f"_format_RPC_call() returning: \n{everything}")
    return everything
