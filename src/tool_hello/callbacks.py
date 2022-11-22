import datetime

from pywebio import output

from src.api import mempoolspace
from src.api import coinbase


def refresh():
    # clear any results and show a loading message
    with output.use_scope('main', clear=True):
        output.put_text("Refreshing...")

    # get the data
    spot = coinbase.spot_price()
    tip = mempoolspace.blockcount()
    gen = mempoolspace.blocktime(0)
    now = mempoolspace.blocktime(tip)


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

    # display the data
    with output.use_scope('main', clear=True):
        output.put_text("Bitcoin price: ${}".format(spot))
        output.put_text("Bitcoin block height: {}".format(tip))
        output.put_text("Block time of genesis block:", gen, datetime.datetime.fromtimestamp(gen))
        output.put_text("Block time of latest block :", now, datetime.datetime.fromtimestamp(now))
        output.put_text(f"Bitcoin is {(now - gen) / 86_400:,.1f} days old!")
