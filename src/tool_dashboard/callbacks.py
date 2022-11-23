import datetime

from pywebio import output

from src.api import mempoolspace
from src.api import coinbase

from . import config

def show_dashboard():
    # clear any results and show a loading message
    with output.use_scope('dashboard', clear=True):
        # output.put_text("Refreshing...")
        output.put_text("Bitcoin price: ${}".format(config.spot))
        output.put_text("Bitcoin block height: {}".format(config.tip))
        output.put_text("Block time of genesis block:", config.gen, datetime.datetime.fromtimestamp(config.gen))
        output.put_text("Block time of latest block :", config.now, datetime.datetime.fromtimestamp(config.now))
        output.put_text(f"Bitcoin is {(config.now - config.gen) / 86_400:,.1f} days old!")
        # TODO - THE OTHER WAY TO DO THIS IS TO HAVE INPUT BOXES THAT ARE UPDATED.. BUT THAT IS NOT PRETTY...
        # OR MAYBE I CAN UPDATE STRINGS... WITH NAMES... CAN I DO THAT?
    
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



def refresh():
    with output.use_scope('dashboard', clear=True):
        output.put_text("...")

    # get the data
    config.spot = coinbase.spot_price()
    config.tip = mempoolspace.blockcount()
    config.gen = mempoolspace.blocktime(0)
    config.now = mempoolspace.blocktime(config.tip)

    show_dashboard()
