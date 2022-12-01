import logging

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pywebio import pin, output

from src.api.coinbase import spot_price



def popup_price_history():
    """
        This is the popup that shows the price history of bitcoin
    """

    raise NotImplementedError("we aren't using Luxor at this time...")
    
    #price_df = get_luxor_price_as_df()
    price_df = None

    if price_df == None:
        output.toast("Error getting price data from Luxor", color='error')

    logging.debug(price_df)

    fig = go.Figure(data=go.Ohlc(x=price_df['timestamp'],
                        open=price_df['open'],
                        high=price_df['high'],
                        low=price_df['low'],
                        close=price_df['close']))

    pr = fig.to_html(include_plotlyjs="require", full_html=False)

    output.popup('bitcoin price history', size=output.PopupSize.LARGE, content=[
        output.put_html(pr)
        ], closable=True)




##############################
def popup_currencyconverter():
    """
        This popup allows you to convert from fiat to bitcoin and back
    """
    def updateprice():
        price_now = spot_price() # query_bitcoinprice()
        pin.pin['convertprice'] = price_now
        return price_now

    def convert_to_sat():
        try:
            amnt = float(pin.pin["amount"])
            price = float(pin.pin["convertprice"])
            if amnt < 0 or price < 0:
                return
        except Exception:
            logging.debug("", exc_info=True)
            return
        r = float(ONE_HUNDRED_MILLION * (amnt / price))
        pin.pin["result"] = f"${amnt:,.2f} @ ${price:,.2f} = {r:,.2f} sats / {r / ONE_HUNDRED_MILLION:.2f} bitcoin\n" + pin.pin['result']

    def convert_to_fiat():
        try:
            amnt = float(pin.pin["amount"])
            price = float(pin.pin["convertprice"])
            if amnt < 0 or price < 0:
                return
        except Exception as e:
            logging.debug("", exc_info=True)
            return
        r = amnt * (price / ONE_HUNDRED_MILLION)
        pin.pin["result"] = f"{amnt:,.2f} sats @ ${price:,.2f} = ${r:,.2f}\n" + pin.pin['result']

    output.popup('USD - BTC converter', content=[
        output.put_row(content=[
            output.put_column(content=[
                pin.put_input("convertprice", type="float", label="Price of bitcoin:", value=updateprice),
                output.put_button("refresh price", onclick=updateprice)
                ]),
            output.put_column(content=[
                pin.put_input("amount", type="float", label="Amount to convert"),
                output.put_column(content=[
                    output.put_button("sats -> fiat", onclick=convert_to_fiat),
                    output.put_button("fiat -> sats", onclick=convert_to_sat)
                    ])
                ])
        ]),
        pin.put_textarea("result", label="Result:", value="", readonly=True)
    ], closable=True)


#################################
def popup_difficulty_history():
    """
        Return a list of network difficulty at first block of each epoch (0, 2016, ...)
        Return None on error
    """
    raise NotImplementedError("TODO")
    # if config.apikey == None:
    #     output.toast("Luxor API key is not supplied", color='error')
    #     return

    # lux = luxor.LuxorAPI(host=luxor.LUXOR_ENDPOINT, method='POST', key=config.apikey)

    # dhx = lux.get_network_difficulty("_1_YEAR")['data']['getChartBySlug']['data']
    # nh = lux.get_network_hashrate("_1_YEAR")['data']['getNetworkHashrate']['nodes']
    # # Note - See issue: https://github.com/LuxorLabs/hashrateindex-api-python-client/issues/4

    # #fig = go.Figure()
    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    # #fig = make_subplots()

    # fig.add_trace(
    #     go.Scatter(
    #         x=[*range(len(dhx) // 2)],
    #         y=[i['difficulty'] for x, i in enumerate(dhx) if x % 2 == 0],
    #         name="difficulty",
    #         line_color="#A50CAC" # PURPLE
    #     ), secondary_y=False)
    # fig.add_trace(
    #     go.Scatter(
    #         x=[*range(len(nh))],
    #         y=[i['networkHashrate'] for i in nh],
    #         name="hashrate",
    #         line_color="#5A5AAA"
    #     ), secondary_y=True)

    # pr = fig.to_html(include_plotlyjs="require", full_html=False)

    # output.popup('network difficulty history', size=output.PopupSize.LARGE, content=[
    #         output.put_html(pr)
    #     ], closable=True)



def avgerage_block_fee(node: NodeHelper, nBlocks = EXPECTED_BLOCKS_PER_DAY) -> int:

    blockheight = node.blockheight()

    with output.popup(f"Averaging transactions fees for last {nBlocks} blocks...", closable=False) as p:

        pin.put_input("remaining", value=nBlocks, label="Blocks remaining:")
        pin.put_textarea("feescroller", value='')
        pin.put_input('sofar', value='', label="Average so far:")
        output.put_button("Stop early", color='danger', onclick=lambda: output.close_popup())

        total_fee = 0
        for bdx in range(blockheight-nBlocks, blockheight):
            # TODO
            # block_fee = int( os.popen(f"""{config.node_path} getblockstats {bdx} '["totalfee"]'""").read().split(': ')[1].split('\n')[0] )        
            raise NotImplementedError("oops...")


            total_fee += block_fee
            pin.pin['remaining'] = blockheight - bdx
            pin.pin['sofar'] = f"{ (total_fee / (1 + bdx - blockheight + nBlocks)) :,.2f}"

            try:
                pin.pin['feescroller'] = f"block: {bdx} --> fee: {block_fee:,}\n" + pin.pin["feescroller"]
            except Exception as e:
                logging.debug("", exc_info=True)
                # this error happens if the popup was closed
                return round(total_fee / (1 + bdx - blockheight + nBlocks), 2)
            logging.info(f"block: {bdx} -->  fee: {format(block_fee, ',').rjust(11)} satoshi")

    output.close_popup()

    total_fee /= nBlocks

    logging.info(f"average block fee over last {nBlocks} blocks is {total_fee:,.2f} satoshi")
    return round(total_fee, 2)








########################################
# https://www.blockchain.com/api/blockchain_api
# https://blockchain.info/rawblock/<block_hash> _OR_ https://blockchain.info/rawblock/<block_hash>?format=hex
# TODO I think we are off by one during countdown
def get_average_block_fee_from_internet(nBlocks = EXPECTED_BLOCKS_PER_DAY) -> float:
    try:
        latest_hash = str(ur.urlopen(ur.Request('https://blockchain.info/q/latesthash')).read(),'utf-8')
        blockheight = int(str(ur.urlopen(ur.Request(f'https://blockchain.info/rawblock/{latest_hash}')).read()).split('"height":')[1].split(',')[0])
    except ur.HTTPError as e:
        logging.exception('')
        return -1

    with output.popup(f"Averaging transactions fees for last {nBlocks} blocks...", closable=False) as p:
        pin.put_input("remaining", value=nBlocks, label="Blocks remaining:")
        pin.put_textarea("feescroller", value='')
        pin.put_input('sofar', value='', label="Average so far:")
        output.put_button("Stop early", color='danger', onclick=lambda: output.close_popup())

        total_fee = 0
        for bdx in range(blockheight-nBlocks, blockheight):
            try:
                block_data = str(ur.urlopen(ur.Request(f'https://blockchain.info/rawblock/{latest_hash}')).read())
            except ur.HTTPError as e:
                logging.exception('HTTPError')
                return -1

            block_fee = int(block_data.split('"fee":')[1].split(',')[0])
            total_fee += block_fee

            pin.pin['remaining'] = blockheight - bdx
            pin.pin['sofar'] = f"{ (total_fee / (1 + bdx - blockheight + nBlocks)) :,.2f}"

            block_height = int(block_data.split('"block_index":')[1].split(',')[0])
            latest_hash = block_data.split('"prev_block":')[1].split(',')[0].strip('"')

            try:
                pin.pin['feescroller'] = f"block: {bdx} --> fee: {block_fee:,}\n" + pin.pin["feescroller"]
            except TypeError as e:
                # this error happens if the popup was closed
                logging.debug("This error is expected if you push the 'stop early' button", exc_info=True)
                return round(total_fee / (1 + bdx - block_height + nBlocks), 2)
            logging.debug(f"block: {bdx} -->  fee: {format(block_fee, ',').rjust(11)} satoshi")

    output.close_popup()

    total_fee /= nBlocks
    logging.debug(f"Average fee per block in last {nBlocks} blocks: {total_fee:,.0f}")
    return round(total_fee, 2)
