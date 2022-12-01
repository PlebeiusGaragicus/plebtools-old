import os
import time
import logging

from .authproxy import AuthServiceProxy


class NewBlockDetails:
    height: int
    difficulty: float
    block_time: float
    time_now: str



def get_latest_block_details( rpc_con ):
    best_hash = rpc_con.getbestblockhash()
    this_block = rpc_con.getblockheader( best_hash )


    new_block = {
        "height": f"{this_block['height']}",
        #"difficulty": this_block["difficulty"],
        "difficulty": "1.123",
        "block_time": f"{this_block['time']}",
        "time_now": f"{time.ctime(time.time())}"
    }

    return new_block


def wait_for_block():
    '''this could be any function that blocks until data is ready'''

    s = time.ctime(time.time())

    if os.getenv("NOT_IN_CONTAINER") == "1":
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(config.u, config.p))
    else:
        rpc_connection = AuthServiceProxy("http://%s:%s@host.docker.internal:8332"%(config.u, config.p))
    # TODO - if error occurs, show to user and assist in trouble-shooting
    config.tip_height = 0 # rpc_connection.getblockcount()

    while True:
        time.sleep(2.5)
        # logging.debug("looking for data again...!")
        # return get_latest_block_details( rpc_connection )

        # TODO I need to change this to track and compare best hashes.. instead of height.  In case of re-org
        # height_now = rpc_connection.getblockcount()
        hash_now = rpc_connection.getbestblockhash()
        logging.debug(f"\n{        hash_now=}\n{config.best_hash=}")
        # if height_now != config.tip_height:
        if hash_now != config.best_hash:
            config.best_hash = hash_now

            return get_latest_block_details( rpc_connection )
