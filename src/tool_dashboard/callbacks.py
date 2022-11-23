# import datetime

# from pywebio import output, pin

# from src.api import mempoolspace
# from src.api import coinbase

# from .config import *



# @output.use_scope('app', clear=True)
# def refresh():
#     spot = coinbase.spot_price()
#     tip = mempoolspace.blockcount()
#     gen = mempoolspace.blocktime(0)
#     now = mempoolspace.blocktime(tip)

#     show_dashboard()
