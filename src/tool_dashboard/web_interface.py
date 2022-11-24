import datetime
from pywebio import output, pin, config

from src.chainstate import ChainState, GenesisBlock
from src.api import mempoolspace
from src.api import coinbase

from .config import *
# from .callbacks import *

@config(title=APP_TITLE, theme='dark')
def main():#menu_callback: callable):

    # output.clear('app')
    with output.use_scope('main', clear=True):
        # output.put_button("<<- Main Menu", color='danger', onclick=menu_callback)
        output.put_markdown(f"# {APP_TITLE}")

    with output.use_scope('refresh', clear=True):
        output.put_button("Refresh", onclick=refresh)

    show_dashboard( GenesisBlock() )
    refresh()



@output.use_scope('app', clear=True)
def show_dashboard(cs: ChainState ):
    if cs is None:
        cs = GenesisBlock()

    output.put_markdown("### Bitcoin network state")
    output.put_table([[
        pin.put_input(name=PIN_BTC_PRICE_NOW, type='text', label="Bitcoin price $", value=f"{cs.spot_price}", readonly=True),
        pin.put_input(name=PIN_HEIGHT, type='text', label="blockchain height", value=f"{cs.block_height}", readonly=True),
        pin.put_input(name=PIN_AVERAGEFEE, type='text', label="average tx fee", value='', readonly=True),
        pin.put_input(name=PIN_SUBSIDY, type='text', label="total reward", value='', readonly=True)
    ],[
        pin.put_input(name=PIN_NETWORKDIFFICULTY, type='text', label="network difficulty", value='', readonly=True),
        pin.put_input(name=PIN_NETWORKHASHRATE, type='text', label="network TH/s", value='', readonly=True),
        pin.put_input(name=PIN_HASHVALUE, type='text', label="hash value", value='', readonly=True, help_text='satoshi earned per Terahash per day'),
        pin.put_input(name=PIN_HASHPRICE, type='text', label="hash price", value='', readonly=True, help_text='hash value denominated in fiat at today\'s price')
    ]])


    output.put_text("Block time of genesis block:", GenesisBlock().block_time, datetime.datetime.fromtimestamp(GenesisBlock().block_time))
    output.put_text("Block time of latest block :", cs.block_time, datetime.datetime.fromtimestamp(cs.block_time))
    output.put_text(f"Bitcoin is {(cs.block_time - GenesisBlock().block_time) / 86_400:,.1f} days old!")
    # output.put_text(f"Bitcoin has been running for {(cs.block_time - ChainState().block_time) / 86_400 / 365:,.1f} years!")


def refresh():

    cs = ChainState()

    # hide refresh button while we're loading
    output.clear_scope('refresh')

    with output.put_loading(color='success', scope='refresh', position=output.OutputPosition.TOP):
        cs.spot_price = coinbase.spot_price()
        cs.block_height = mempoolspace.blockcount()
        cs.block_time = mempoolspace.blocktime(cs.block_height)

    # show refresh button once loading is done
    output.put_button("Refresh", onclick=refresh, scope='refresh')

    show_dashboard( cs )




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