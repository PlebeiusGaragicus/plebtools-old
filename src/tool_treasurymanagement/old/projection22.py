import logging

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .constants import *

class ProjectionMapping:
    current_height: int # AKA current time
    months_to_project: int # how long to make the results
    block_height: list[int] = []

    # NETWORK HASH RATE
    starting_difficulty: float
    ngf: float # Network Growth Factor
    block_difficulty: list[float] = []

    # PRICE
    # starting_price: float,
    # pgf: float # price growth factor
    # block_price : list[float]


#def make_projection(vars: ProjectionMapping) -> dict:
def make_projection(
                    current_height: int, # AKA current time
                    months_to_project: int, # how long to make the results

                    # NETWORK HASH RATE
                    difficulty: float,
                    ngf: float,

                    # PRICE
                    exchange_rate: float = None,
                    exchange_gf: float = None
    ) -> ProjectionMapping:
    """ This function does the "make believe" into the future and returns a guess ( a projection )
    """

    logging.debug(f"{vars=}")
    pass































def calculate_projection(
                        months, height, avgfee, hashrate, wattage,
                        price, pricegrow, pricegrow2, pricelag,
                        network_difficulty, hashgrow,
                        kWh_rate, opex,capex_in_sats, resale, poolfee
                    ) -> dict:
    """ This function taken in all variables of interest and projects bitcoin earnings and fiat cost of running bitcoin miners
        This function returns a dict with the projection results.
    """

    # var = {}
    # var['months'] = get_entered_months()
    # var['height'] = get_entered_height()
    # var['avgfee'] = get_entered_fees()
    # var['hashrate'] = get_entered_hashrate()
    # var['wattage'] = get_entered_wattage()
    # var['price'] = get_entered_price()
    # var['price_when_bought'] = get_entered_bought_price()

    # var['pricegrow'] = float(pin.pin[PIN_PRICEGROW] / 100)
    # var['pricegrow2'] = float(pin.pin[PIN_PRICEGROW2] / 100)
    # var['pricelag'] = int(pin.pin[PIN_LAG])
    
    # var['diff'] = get_entered_difficulty()
    # var['hashgrow'] = float(pin.pin[PIN_HASHGROW] / 100)

    # var['kWh_rate'] = get_entered_rate()
    # var['opex'] = get_entered_opex()
    # var['capex'] = get_entered_machine_cost()
    # var['resell'] = get_entered_resell_percent()
    # var['poolfee'] = get_entered_poolfee()

        #if None in (months, height, avgfee, hashrate, wattage, price,
    #            pricegrow, pricegrow2, pricelag, diff,
    #            hashgrow, kWh_rate, opex, capex, resell, poolfee):
    raise NotImplementedError('fuck')
    # if None in var.items():
    #     output.toast("Error - an input field was left blank (or is invalid)")
    #     logging.error("None variable passed to calculate_projection()")
    #     return



    if None in (months,height, avgfee, hashrate, wattage, price,
                pricegrow, pricegrow2, pricelag, network_difficulty,
                hashgrow, kWh_rate, opex, capex_in_sats, resale, poolfee):
        logging.error("None variable passed to calculate_projection()")
        return

    networh_hashrate = get_hashrate_from_difficulty(network_difficulty)

    capexsats_per_months = capex_in_sats / months
    logging.debug(f"capex: {capex_in_sats} sats -> {capexsats_per_months} sats/month")

    capex_in_sats *= 1 - (resale / 100)
    logging.debug(f"resell: {resale}% -> {capex_in_sats} sats/month")

    capexsats_per_months = capex_in_sats / months
    logging.debug(f"capex: {capex_in_sats} sats -> {capexsats_per_months} sats/month")

    # have we crossed a halvening?  We use this to determine which growth factor to use with price/nh
    # TODO - what if we project out really far and cross TWO halvenings?
    crossed = False
    # this used in conjunction with pricelag
    month_we_crossed = 0

    for m in range(months):
        sats_earned = 0
        #poolfee = 0
        _kwh = 0

        # DO ONE DAY OF CALCULATIONS
        for _day in range(30):

            if blocks_until_halvening( height ) < EXPECTED_BLOCKS_PER_DAY:
                crossed = True
                month_we_crossed = m

                # GO BLOCK BY BLOCK
                for _blk in range( EXPECTED_BLOCKS_PER_DAY ):

                    sats_earned += hashrate * (block_subsity( height ) + avgfee) * (1 - poolfee) / networh_hashrate
                    _kwh += wattage / 6000
                    height += 1

                    #logging.debug(f"block - block {height}, subsidy {block_subsity( height )}, nh {networh_hashrate/MEGAHASH:,.2f}, kWh {_kwh}")

            # DO A WHOLE DAY AT A TIME
            else:
                sats_earned += hashrate * (block_subsity( height ) + avgfee) * (1 - poolfee) * EXPECTED_BLOCKS_PER_DAY / networh_hashrate
                _kwh += 24 * wattage / 1000
                height += EXPECTED_BLOCKS_PER_DAY

                #logging.debug(f"day - block {height}, subsidy {block_subsity( height )}, nh {networh_hashrate/MEGAHASH:,.2f}, kWh {_kwh}")

            # END OF DAY STUFF
            networh_hashrate *= 1 + hashgrow / 30

        # END OF MONTH STUFF - now we have to settle

        # if we have crossed the halvening AND it's been 'LAG MONTHS' since... use pricegrow2
        if crossed and m - month_we_crossed >= pricelag:
            price *= 1 + pricegrow2
            #logging.debug(f"price increased to {price} - using growth factor2: {pricegrow2}")
        else:
            # if we haven't crossed a halvening... OR it hasn't been 'LAG MONTHS' yet
            price *= 1 + pricegrow # 1 + pricegrow / 30 # daily
            #logging.debug(f"price increased to {price} - using growth factor2: {pricegrow2}")

        sold_e = btc(_kwh * kWh_rate, bitcoin_price=price)
        sold_o = btc(opex, bitcoin_price=price) # we divide opex by my hashrate because everything else on this graph is reduced in this manner

        # basically, just the decision/assumption-making/verifying helper variables
        breakeven_price = ((ONE_HUNDRED_MILLION * opex) + (ONE_HUNDRED_MILLION * _kwh * kWh_rate)) / (sats_earned - btc(capex_in_sats, bitcoin_price=price))

        res[KEY_ESTIMATED_HEIGHT].append( height )
        res[KEY_ESTIMATED_NETWORK_HASHRATE].append( networh_hashrate )
        res[KEY_ESTIMATED_PRICE].append( price )
        #res[KEY_ESTIMATED_AVGFEE].append( 0 )

        res[KEY_HASHVALUE].append( sats_earned )
        res[KEY_KWH].append( _kwh )

        res[KEY_SOLD_ELECTRICITY].append( sold_e )
        res[KEY_SOLD_OPEX].append( sold_o )
        res[KEY_SOLD_CAPEX].append( capexsats_per_months )

        res[KEY_BREAKEVEN_PRICE].append( breakeven_price )
        # KEY_BREAKEVEN_PRICE_P20P : [],
        # KEY_BREAKEVEN_NH : [],
    return res
