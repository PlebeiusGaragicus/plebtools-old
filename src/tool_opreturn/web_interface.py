import os
import decimal
import logging
import json
import dotenv
from pywebio import output, pin, config

from src.api.authproxy import AuthServiceProxy, JSONRPCException

from .config import *
from .callbacks import *

tip = 0

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

@config(title=APP_TITLE, theme='dark')
def main():

    dotenv.load_dotenv()

    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_row(
            [
                pin.put_input(name='height',label='',type='number',value='', placeholder='Enter Block Height'),
                output.put_button('Get OP_RETURN data', onclick=show_opreturns)
            ])
        output.put_table([
            [
                    output.put_button('Prev', disabled=pin.pin['height'] == 0, onclick=prev),
                    output.put_button("Use latest", onclick=use_latest),
                    output.put_button('Next', onclick=next)
            ]
        ])
        output.put_collapse(title='Encoding options', content=[
            pin.put_checkbox('encoding', options=["utf-8","ascii"], value=["utf-8","ascii"], inline=True)
        ], open=False)

        show_opreturns()


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

def show_opreturns():
    output.clear('opreturns')
    with output.put_loading(color='primary'):#, scope='main', position=output.OutputPosition.BOTTOM):
        do_work()

@output.use_scope('opreturns')
def do_work():
    # user = os.getenv('RPC_USER')
    user = '__cookie__'
    # pswd = os.getenv('RPC_PASS')
    pswd = os.getenv('COOKIE')
    host = os.getenv('RPC_HOST')
    port = os.getenv('RPC_PORT')

    rpc_url = f"http://{user}:{pswd}@{host}:{port}"
    rpc_connection = AuthServiceProxy(rpc_url)
    logging.debug(f"{rpc_url=}")

    global tip
    try:
        tip = rpc_connection.getblockcount()
    except JSONRPCException as e:
        output.toast(f"ERROR: {e}", color='error', duration=10)
        output.toast(f"Check your RPC connection settings", color='warn', duration=10)
        return

    height = pin.pin['height']

    if height == None or height is '':
        output.toast("Enter a block height to read OP_RETURN data")
        return

    if height > tip:
        output.toast(f"Block height {height} is higher than the current tip {tip}", position='top', duration=3)
        return

    hash = rpc_connection.getblockhash( height )
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
