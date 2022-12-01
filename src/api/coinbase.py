import logging
import json
import requests

# import pandas as pd

def spot_price() -> float:
    """ queries the current bitcoin price from the coindesk.com API
        returns (-1) on error
        shell one-liner:
            - alias btcprice = "curl -s 'https://api.coinbase.com/v2/prices/spot?currency=USD' | jq -r '.data.amount'"
    """

    API_URL = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
    #response = ur.urlopen(ur.Request( API_URL )).read()
    response = requests.get(API_URL)

    if response.status_code != 200:
        logging.error("Did not receieve OK response from Coinbase API")
        return None

    try:
        data = json.loads(response.text) # returns dict
        price = float( data['data']['amount'] )
    except json.decoder.JSONDecodeError:
        logging.error(f"__func__ exception", exc_info=True)
        return None

    logging.debug(f"query_bitcoin_spot_price() -> {price}")
    return price



# # FOR HELP WITH UNIX TIME
# # https://www.unixtimestamp.com/index.php
# def bitcoin_price_history(start_timestamp: int, end_timestamp: int) -> pd.DataFrame:
#     """
#         refer to: https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles
#         code example taken from: https://www.cryptodatadownload.com/blog/posts/Use-Python-to-Download-Coinbase-Price-Data/
#     """

#     logging.debug(f"query_coinbase_bitcoin_price_history({start_timestamp=} {end_timestamp=})")
#     SYMBOL = 'BTC-USD'

#     COINBASE_URL = f'https://api.pro.coinbase.com/products/{SYMBOL}/candles?granularity=86400&start={start_timestamp}&end={end_timestamp}'
#     response = requests.get(COINBASE_URL)
#     logging.debug(f"{response.status_code=}")

#     if response.status_code != 200:
#         logging.error("Did not receieve OK response from Coinbase API")
#         return None

#     data = pd.DataFrame(json.loads(response.text), columns=['unix', 'low', 'high', 'open', 'close', 'volume'])
#     #data = pd.DataFrame(json.loads(response.text), columns=['unix', 'close'])
#     #data = pd.DataFrame(json.loads(response.text))
#     data['date'] = pd.to_datetime(data['unix'], unit='s')  # convert to a readable date
#     #data['unix'] = pd.to_datetime(data['unix'], unit='s')  # convert to a readable date

#     # if data is None:
#     #     logging.error("Did not return any data from Coinbase for this symbol")
#     #     return None
#     # else:
#     #     data.to_csv(f'Coinbase_price_data.csv', index=False)

#     logging.debug(f"query_coinbase_bitcoin_price_history() -> {data=}")

#     return data