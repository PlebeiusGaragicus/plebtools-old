import logging
import json
import requests

""" https://mempool.space/docs/api/rest#get-block-height
"""

def getblockhash(height: int):
    logging.debug(f"query_mempool_bitcoin_getblockhash({height=})")

    API_URL = f"https://mempool.space/api/block-height/{height}"
    #response = ur.urlopen(ur.Request( API_URL )).read()
    response = requests.get(API_URL)
    logging.debug(f"{response.status_code=}")

    if response.status_code != 200:
        logging.error("Did not receieve OK response from mempool.space API")
        return None

    # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
    block_hash = response.text

    # TODO check that returned value is valid?? Ensure it is a string of len 64?

    logging.debug(f"query_mempool_bitcoin_getblockhash() -> {block_hash}")
    return block_hash


def blockcount() -> int:
    logging.debug(f"query_mempool_blockcount()")
    API_URL = "https://mempool.space/api/blocks/tip/height"

    response = requests.get(API_URL)
    logging.debug(f"{response.status_code=}")

    if response.status_code != 200:
        logging.error("Did not receieve OK response from mempool.space API")
        return None

    tip_height = int(response.text)

    # TODO check that returned value is valid???

    logging.debug(f"query_mempool_blockcount() -> {tip_height}")
    return tip_height


def block_info(hash: str):
    logging.debug(f"query_mempool_block_info({hash=})")

    API_URL = f"https://mempool.space/api/block/{hash}"
    response = requests.get(API_URL)
    logging.debug(f"{response.status_code=}; {response.text}")

    if response.status_code != 200:
        logging.error("Did not receieve OK response from mempool.space API")
        return None

    block_info = response.text

    try:
        block_info = json.loads(response.text) # returns dict
    except json.decoder.JSONDecodeError:
        logging.error(f"__func__ exception", exc_info=True)
        return None

    # TODO check that returned value is valid?? Ensure it is a string of len 64?

    logging.debug(f"query_mempool_block_info() -> {block_info}")
    return block_info


def blocktime(height: int) -> int:
    logging.debug(f"query_mempool_blocktime({height=})")
    hash = getblockhash(height=height)
    ret = block_info(hash)
    block_time = int( ret['timestamp'] )
    return block_time



################################
if __name__ == "__main__":
    import datetime
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s",
    #     handlers=[logging.StreamHandler()])

    print("Using the mempool.space API https://mempool.space/docs/api/rest")

    tip = blockcount()
    print("Blockchain tip height:", tip)
    print("Hash of genesis block:", getblockhash(0))
    print("Hash of latest block :", getblockhash(tip))

    # d = datetime.datetime.fromtimestamp()

    gen = blocktime(0)
    now = blocktime(tip)
    print("Block time of genesis block:", gen, datetime.datetime.fromtimestamp(gen))
    print("Block time of latest block :", now, datetime.datetime.fromtimestamp(now))
    print(f"Bitcoin is {(now - gen) / 86_400:,.1f} days old!")
