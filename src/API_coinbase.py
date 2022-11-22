import logging
import json
import requests

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
