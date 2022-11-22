import datetime

import pywebio
from pywebio import output

from . import config
from . import API_coinbase
from . import API_mempoolspace
from . import authproxy

@pywebio.config(title=config.APP_TITLE, theme='dark')
def main_page():
    output.put_markdown(f"# {config.APP_TITLE}")

    with output.use_scope("menu", clear=True):
        # when this is used the callback is given the text of the button pressed
        # output.put_buttons(["Refresh", "or"], onclick=refresh)
        output.put_button("Refresh", onclick=refresh)

    refresh()

def refresh():
    # clear any results and show a loading message
    with output.use_scope('main', clear=True):
        output.put_text("Refreshing...")

    # get the data
    spot = API_coinbase.spot_price()
    tip = API_mempoolspace.blockcount()
    gen = API_mempoolspace.blocktime(0)
    now = API_mempoolspace.blocktime(tip)


    # TODO TODO TODO
    # how to I get the user/password of the running bitcoind docker if it's running in a docker container?
    # rpc_user and rpc_password are set in the bitcoin.conf file
    # rpc_connection = authproxy.AuthServiceProxy("http://%s:%s@127.0.0.1:3005"%(rpc_user, rpc_password))
    # best_block_hash = rpc_connection.getbestblockhash()

    # print(rpc_connection.getblock(best_block_hash))


    # commands = [ [ "getblockhash", height] for height in range(100) ]
    # block_hashes = rpc_connection.batch_(commands)

    # blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
    # block_times = [ block["time"] for block in blocks ]

    # print(block_times)


    # display the data
    with output.use_scope('main', clear=True):
        output.put_text("Bitcoin price: ${}".format(spot))
        output.put_text("Bitcoin block height: {}".format(tip))
        output.put_text("Block time of genesis block:", gen, datetime.datetime.fromtimestamp(gen))
        output.put_text("Block time of latest block :", now, datetime.datetime.fromtimestamp(now))
        output.put_text(f"Bitcoin is {(now - gen) / 86_400:,.1f} days old!")
