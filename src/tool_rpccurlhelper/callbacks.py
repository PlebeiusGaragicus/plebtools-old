import logging
import json

from pywebio import output, pin

from .config import *

@output.use_scope('app')
def generate():

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

    output.put_text(f"{out}")

def add_command( cmd: str ):
    #pin.pin['feescroller'] = f"block: {bdx} --> fee: {block_fee:,}\n" + pin.pin["feescroller"]
    pass

def use_cookie_callback( opt: str ):
    logging.debug(f"use_cookie_callback({opt})")

    # if pin.pin[PIN_USE_COOKIE]:
    if opt == ["Use cookie file"]:
        pin.pin[PIN_USERNAME] = '__cookie__'
        pin.pin_update(PIN_USERNAME, readonly=True)
    else:
        pin.pin_update(PIN_USERNAME, readonly=False)
        pin.pin[PIN_USERNAME] = ''

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
