import time
from datetime import datetime
import logging

from pywebio import pin, output

from PlebTools.BlockchainData import NodeHelper
from PlebTools.BlockchainData import API_mempoolspace

block_now: int
block_last: int

def update_time():
    output.put_markdown(f"""
## The current time is:
__{block_now}__
{datetime.now()}
---
""")




def keep_alive():
    
    global block_now, block_last
    block_last = block_now

    update_time()

    while True:
        time.sleep(15)

        block_now = API_mempoolspace.query_blockcount()

        if block_last != block_now:
            block_last = block_now

            update_time()
        





def show_interface():
    global block_now
    block_now = API_mempoolspace.query_blockcount()

    output.put_markdown("# BLOCK CLOCK")
    # output.put_markdown(f"## The current time is: {block_now} | {time.time()} | {datetime.now()}")


    keep_alive()




# output.put_button(label='label', onclick=trythis, color='info')