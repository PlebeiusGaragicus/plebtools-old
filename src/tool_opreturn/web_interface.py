import logging
import json

from pywebio import output, pin, config

from src.api.authproxy import AuthServiceProxy, JSONRPCException, CustomJsonEncoder
from src.settings import AppSettings

####################################
# GLOBALS

APP_TITLE = "OP_RETURN Reader"

appsettings: AppSettings = None

# Note: we don't use a global connection anymore because it will time out or otherwise have a bunch of errors happen when the user pauses for as little as 30 seconds
# rpc_connection: AuthServiceProxy = None

tip = 0


########################################
# CALLBACKS

def prev():
    if pin.pin['height'] == 0:
        return
    try:
        pin.pin['height'] -= 1
    except TypeError:
        output.toast("no block number entered", color='error')
        return
    show_opreturns()

def next():
    try:
        pin.pin['height'] += 1
    except TypeError:
        output.toast("no block number entered", color='error')
        return
    show_opreturns()

def use_latest():
    global tip
    pin.pin['height'] = tip
    show_opreturns()

def show_opreturns():
    output.clear('opreturns')
    with output.put_loading(color='primary'):#, scope='main', position=output.OutputPosition.BOTTOM):
        do_work()
########################################




def return_AuthProxy() -> AuthServiceProxy:
    global appsettings
    user = appsettings['RPC_USER']
    pswd = appsettings['RPC_PASS']
    host = appsettings['RPC_HOST']
    port = appsettings['RPC_PORT']

    rpc_url = f"http://{user}:{pswd}@{host}:{port}"
    logging.debug(f"{rpc_url=}")

    return AuthServiceProxy(rpc_url)


@output.use_scope('opreturns')
def do_work():
    """
        - connects to node and gets the block
    """


    rpc_connection = return_AuthProxy()

    # Note: shouln't need this because we verify node settings and connection when the app starts
    # if rpc_connection == None:
    #     return


    # NOTE: I shouldn't need this anymore becuase app will verify node connection at startup
    # try:
    #     tip = rpc_connection.getblockcount()
    # except JSONRPCException as e:
    #     output.toast(f"ERROR: {e}", color='error', duration=10)
    #     output.toast(f"Check your RPC connection settings", color='warn', duration=10)
    #     return

    global tip
    tip = rpc_connection.getblockcount()

    height = pin.pin['height']

    if height == None or height == '':
        output.toast("Enter a block height to read OP_RETURN data")
        return

    if height > tip:
        output.toast(f"Block height {height} is higher than the current tip {tip}", color='error', duration=3)
        return

    try:
        hash = rpc_connection.getblockhash( height )
    except JSONRPCException as e:
        output.toast(f"ERROR: {e}", color='error', duration=5)
        return

    try:
        block = rpc_connection.getblock( hash, 2 ) # call with verbosity 2 in order to get tx details
    except JSONRPCException as e:
        output.toast(f"ERROR: {e}", color='error', duration=10)
        return
    block = json.loads( json.dumps( block , cls=CustomJsonEncoder) )

    if "tx" not in block:
        output.put_text(f"Block {height} has no transactions")
        return

    for txidx, tx in enumerate(block['tx']):
        for voutidx, vout in enumerate(tx['vout']): # THESE ARE THE UTXOs
            if 'scriptPubKey' in vout:
                scriptPubKey = vout['scriptPubKey']
                if "asm" in scriptPubKey:
                    asm = scriptPubKey["asm"]
                    if "OP_RETURN" in asm:
                        ophex = asm.replace("OP_RETURN ", "")
                        # require even number of characters (two hex digits per byte)
                        if len(ophex) % 2 == 1:
                            continue
                        # encodinglist = ["utf-8","gb18030","euc-kr","cp1253","utf-32","utf-16","euc-kr","cp1253","cp1252","iso8859-16","ascii","latin-1","iso8859-1"]
                        encodinglist = ["utf-8","ascii"]
                        hasError = True
                        try:
                            opbytes = bytes.fromhex(ophex)
                        except Exception as e:
                            logging.error(f"error handling ophex '{ophex}' : error: {e}")
                        for encoding in encodinglist:
                            if hasError == False:
                                break
                            try:
                                optext = opbytes.decode(encoding)
                                hasError = False
                                logging.debug(optext)
                                output.put_markdown(f"# OP_RETURN:")
                                output.put_markdown(f"### {optext}")
                                output.put_collapse(title="details", content=[
                                    output.put_markdown(f"## Encoding used: {encoding}"),
                                    output.put_markdown(f"```Transaction index [{txidx}]``` \n ```vout index [{voutidx}]```"),
                                    output.put_markdown(f"## txid: \n {tx['txid']}"),
                                    output.put_markdown(f"## Raw transaction JSON: \n {tx}")
                                ])
                            except Exception as e:
                                pass
    output.put_markdown(f"---")
    output.put_text("end of list...")



@config(title=APP_TITLE, theme='dark')
def main():

    global appsettings
    appsettings = AppSettings()

    rpc_connection = return_AuthProxy()

    try:
        info = rpc_connection.getblockchaininfo()

        global tip
        tip = rpc_connection.getblockcount()

        output.toast(f"Node connected - working on {info['chain']} chain")
    except JSONRPCException as e:
        logging.error(f"Error connecting to node: {e}")
        output.toast("ERROR: Cannot connect to node!", color='error', duration=4)
        output.put_markdown("# Uh oh - cannot connect to node!")
        output.put_text("I can't connect to a bitcoin node.  Make sure the node is running.  Also double check your that bitcoind RPC credentials are correct in settings...")
        output.put_link(name='Open settings', url="./settings")
        return


    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_table([
            [
                output.span(
                    pin.put_input(name='height',label='Block height:',type='number',value='', placeholder='Enter Block Height'),
                    col=3
                )
            ],[
                output.span(
                    output.put_button('Get OP_RETURN data', onclick=show_opreturns),
                    col=3)
            ],[
                    output.put_button('Prev', disabled=pin.pin['height'] == 0, onclick=prev),
                    output.put_button("Use latest", onclick=use_latest),
                    output.put_button('Next', onclick=next)
            ],[
                output.span(
                    output.put_collapse(title='Encoding options', content=[
                        pin.put_checkbox('encoding', options=["utf-8","ascii"], value=["utf-8","ascii"], inline=True)
                    ], open=False),
                    col=3)
            ]
            # TODO: I can't get this fucking style thing to work!!! WTF!?!?!?
        ]).style("align-items: center; justify-content: center;")


    pin.pin_update('height', value=tip)
