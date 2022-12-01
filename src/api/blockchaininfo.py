import logging
import urllib.request as ur

""" This gets the needed bitcoin network data from blockchain.info :)
    https://www.blockchain.com/api/q

"""

def bitcoin_height() -> int:
    try:
        return int(ur.urlopen(ur.Request('https://blockchain.info/q/getblockcount')).read())
    except Exception as e:
        logging.info(f"ERROR while querying blockchain.info: {e}", exc_info=True)
        return None


def bitcoin_difficulty() -> int:
    try:
        # why int(float()) ??? I don't remember...
        return int(float(ur.urlopen(ur.Request('https://blockchain.info/q/getdifficulty')).read()))
    except Exception as e:
        logging.info(f"ERROR while querying blockchain.info: {e}", exc_info=True)
        return None



def bitcoin_networkhashrate() -> int:
    try:
        return int(ur.urlopen(ur.Request('https://blockchain.info/q/hashrate')).read()) / 1000
    except Exception as e:
        logging.info(f"ERROR while querying blockchain.info: {e}", exc_info=True)
        return None
