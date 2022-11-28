import logging
import datetime

from pywebio import output, pin

from OSINTofBlockchain.BitcoinData import (
    coinbase_API,
    MEGAHASH,
    ONE_HUNDRED_MILLION,
    EXPECTED_BLOCKS_PER_DAY,
    fiat,
    btc,
    block_subsity,
    get_hashrate_from_difficulty
)

from . import config
from .constants import *

from OSINTofBlockchain.Apps import get_input



def update_price() -> None:
    """ This is called when the user enters an 'old' block height and we run a historical projection

        This function essentially takes the entered height, queries coinbase for the price, and updates the PIN_PRICE field
    """
    # this feature is only available when running a node
    if config.my_node != None:
        return

    h = get_input(PIN_HEIGHT, int)
    if h == None:
        return

    if h < 365000:
        output.toast("price data does not exist for block before 365000")
        pin.pin_update(PIN_BTC_PRICE_NOW, value=0)
        return

    # a height in the future
    if h > config.my_node.blockchain_state.block_height:
        return

    # TODO - shouldn't even a pruned node have all the headers..?  and isn't the unix time in that header?  We should be able to use a pruned node here... right??!?!??
    # on second thought... just say no to pruned nodes, kids.
    #if config.pruned and h < config.pruned_height:
    # if h < config.my_node.pruned_height:
    #     logging.debug("This node is pruned and that block is not in memory...")
    #     return

    logging.debug(f"update_price {h=}")

    unix = config.my_node.get_block_time(h)
    if unix == None: #pruned node.. or, we just don't have the data for that height
        return

    p = coinbase_API.coinbase_fetch_price_history(unix, unix+86400)
    try:
        price = (p['open'][0] + p['close'][0]) / 2
        logging.debug(f"{price=}")
        price = round(price, 2)
    except IndexError:
        output.toast(f"unable to load the price for block height {h}")
        pin.pin_update(PIN_BTC_PRICE_NOW, value='')
        return
    
    logging.debug(f"we got a price of {price}")

    pin.pin_update(PIN_BTC_PRICE_NOW, value=price) #nah, just leave it...

################################
def update_timestamp() -> None:
    # this feature only works if you have a node
    #if config.node_path == None and config.RPC_enabled == False:
    if config.my_node == None:
        return

    h = get_input(PIN_HEIGHT, int)

    # if height is blank, return
    # or, if height is in the future, return
    if (h == None) or (h > config.my_node.blockchain_state.block_height):
        pin.pin_update(PIN_HEIGHT, help_text='')
        return

    try:
        t = config.my_node.get_block_time(h)
        #t = node.get_block_unix_time(h)
        t = datetime.datetime.fromtimestamp(t).isoformat(sep=' ', timespec='seconds')

    except Exception:
        logging.debug('', exc_info=True)
        output.toast("unable to get block time - are you running a pruned node?")
        pin.pin_update(PIN_HEIGHT, help_text='')
        return

    pin.pin_update(PIN_HEIGHT, help_text=t)

#################################
def update_difficulty() -> None:
    # this feature only works if you have a node
    if config.my_node == None:
        logging.debug("no node enabled; update_difficulty() returning")
        return

    h = get_input(PIN_HEIGHT, int)

    if (h == None) or (h > config.my_node.blockchain_state.block_height):
        return

    try:
        bh = config.my_node.run(method='getblockhash', params=[h])
        diff = config.my_node.run(method='getblockheader', params=[bh, ['difficulty']])

        if diff == None:
            return

        pin.pin_update(PIN_NETWORKDIFFICULTY, value=diff)

    except Exception:
        #logging.error('', exc_info=True)
        output.toast("unable to get block difficulty - are you running a pruned node?")


##############################
def update_subsity() -> None:
    fees = get_input(PIN_AVERAGEFEE, float)
    height = get_input(PIN_HEIGHT, int)

    if None in (height, fees):
        pin.pin[PIN_SUBSIDY] = ''
        pin.pin_update(PIN_SUBSIDY, help_text='')
        return

    total = block_subsity( height ) + fees
    pin.pin[PIN_SUBSIDY] = f"{total:,}"

    price = get_input(PIN_BTC_PRICE_NOW, float)

    if price == None:
        pin.pin_update(PIN_SUBSIDY, help_text='')
        return

    fiat_reward = fiat(total, price)
    pin.pin_update(PIN_SUBSIDY, help_text=f"$ {fiat_reward:,.2f}")

###############################
def update_hashrate() -> None:
    diff = get_input(PIN_NETWORKDIFFICULTY, float)

    if diff == None: # this is lame... I am lame for writing this... but this make the code consistant... and it works... so buzz off
        pin.pin[PIN_NETWORKHASHRATE] = ''
        pin.pin_update(PIN_NETWORKHASHRATE, help_text=f'')
        return

    nh = round(get_hashrate_from_difficulty(diff), 2)
    pin.pin[PIN_NETWORKHASHRATE] = f"{nh:,} TH/s"
    pin.pin_update(PIN_NETWORKHASHRATE, help_text=f"{nh/MEGAHASH:.2f} EH/s")

################################
def update_hashvalue() -> None:
    height = get_input(PIN_HEIGHT, int)
    fees = get_input(PIN_AVERAGEFEE, float)
    diff = get_input(PIN_NETWORKDIFFICULTY, float)

    if None in (height, fees, diff):
        pin.pin[PIN_HASHVALUE] = ''
        return

    try:
        nh = round(get_hashrate_from_difficulty(diff), 2)
        reward = block_subsity( height ) + fees
        r = reward / nh * EXPECTED_BLOCKS_PER_DAY
    except ZeroDivisionError:
        pin.pin[PIN_HASHVALUE] = ''
        return

    pin.pin[PIN_HASHVALUE] = f"{r:,.1f} sats"

################################
def update_hashprice() -> None:
    price = get_input(PIN_BTC_PRICE_NOW, float)

    try:
        # let's be lazy and just grab the hashvalue entry to use it
        s = str(pin.pin[PIN_HASHVALUE]).replace(',', '').replace(' sats', '')
        hv = float(s)
    except ValueError:
        pin.pin[PIN_HASHPRICE] = ''
        logging.debug('ummm...', exc_info=True)
        return

    if price == None:
        pin.pin[PIN_HASHPRICE] = ''
        return

    r = fiat(hv, price)
    pin.pin[PIN_HASHPRICE] = f"$ {r:,.4f}"

###########################
def update_cost() -> None:
    """
    """

    cost = get_input(PIN_MACHINE_COST_UPFRONT, float)
    bought_price = get_input(PIN_BOUGHTATPRICE, float)

    if None in (cost, bought_price):
        pin.pin_update(name=PIN_MACHINE_COST_UPFRONT, help_text='')
        return

    try:
        pin.pin_update(name=PIN_MACHINE_COST_UPFRONT, help_text=f"{ONE_HUNDRED_MILLION * (cost/bought_price):,.1f} sats")
    except ZeroDivisionError:
        pin.pin_update(name=PIN_MACHINE_COST_UPFRONT, help_text=f"")

################################
def update_satsperth() -> None:
    """
    """

    hashrate = get_input(PIN_HASHRATE, float)
    bought_price = get_input(PIN_BOUGHTATPRICE, float)
    cost = get_input(PIN_MACHINE_COST_UPFRONT, float)

    if None in (hashrate, bought_price, cost):
        pin.pin[PIN_FIAT_PER_TH] = ''
        return

    ret = btc(cost, bought_price) / hashrate

    pin.pin[PIN_SAT_PER_TH] = f"{ret:,.2f}"

################################
def update_fiatperth() -> None:
    """
    """

    hashrate = get_input(PIN_HASHRATE, float)
    cost = get_input(PIN_MACHINE_COST_UPFRONT, float)

    if None in (hashrate, cost):
        pin.pin_update(PIN_FIAT_PER_TH, value='')
        return

    fiats_per_th = cost / hashrate
    pin.pin[PIN_FIAT_PER_TH] = f"{fiats_per_th:,.2f}"

##########################
def update_eff() -> None:
    """
    """

    wattage = get_input(PIN_WATTAGE, float)
    hashrate = get_input(PIN_HASHRATE, float)

    if None in (wattage, hashrate):
        pin.pin[PIN_EFF] = ''
        return

    try:
        eff = float(wattage / hashrate)
    except ZeroDivisionError:
        eff = None

    pin.pin[PIN_EFF] = f"{eff:,.2f}"

##################################
def update_hashexpense() -> None:
    eff = pin.pin[PIN_EFF] # we're just going to read from this input field so we don't have to duplicate too much shit
    # rate = get_entered_rate()
    # poolfee = get_entered_poolfee()
    # price = get_entered_price()
    rate = get_input(PIN_KWH_RATE, float)
    poolfee = get_input(PIN_POOLFEE, float)
    price = get_input(PIN_MACHINE_COST_UPFRONT, float)

    try:
        hv = float(str(pin.pin[PIN_HASHVALUE]).replace(' sats', '').replace(',', ''))
    except ValueError:
        logging.debug('', exc_info=True) # this way it only shows up in debug mode
        pin.pin[PIN_HASHEXPENSE] = ''
        return

    if None in (eff, rate, poolfee, price, hv):
        pin.pin[PIN_HASHEXPENSE] = f''
        return

    fiat_pool_fee = poolfee * fiat(hv, price)
    ret = rate * (eff / 6000) * EXPECTED_BLOCKS_PER_DAY - fiat_pool_fee

    pin.pin[PIN_HASHEXPENSE] = f"$ {ret:,.5f}"


def update_height( height ) -> None:
    h = get_input(PIN_HEIGHT, int)

    if h == None:
        return

    # only try to update the price if we're going at least one day back
    #if h < (config.height - 144):
    if h < config.my_node.blockchain_state.block_height:
        output.toast("Using historical data")
        update_price()

    update_difficulty()
    update_timestamp()

    update_numbers()


def update_financing( throwaway ) -> None:
    """ This is the callback for any of the non-read-only financing input fields
    """

    p = get_input(PIN_MACHINE_LOAN_PRINCIP, float)
    i = get_input(PIN_MACHINE_LOAN_INTEREST, float)
    r = get_input(PIN_MACHINE_LOAN_REPAYMENT, float)

    try:
        pin.pin[PIN_MACHINE_LOAN_MONTHLY] = round((p + i) / r, 3)
        # if divide by zero (because the repayment term is zero months), monthly cost will be principal plus interest
    except ZeroDivisionError:
        pin.pin[PIN_MACHINE_LOAN_MONTHLY] = (p + i)

    p = get_input(PIN_INFRA_LOAN_PRINCIP, float)
    i = get_input(PIN_INFRA_LOAN_INTEREST, float)
    r = get_input(PIN_INFRA_LOAN_REPAYMENT, float)

    try:
        pin.pin[PIN_INFRA_LOAN_MONTHLY] = round((p + i) / r, 3)
    except ZeroDivisionError:
        # if divide by zero (because the repayment term is zero months), monthly cost will be principal plus interest
        pin.pin[PIN_INFRA_LOAN_MONTHLY] = (p + i)




def update_numbers( throw_away=None ) -> None:
    """ This is the callback for (just about) every 'pin' input field.  Why?
          Because this all-in-one function ensures that every field is updated whenever the user presses a key on the keyboard.
            All input fields are always up-to-date with proper numbers
    """

    #update_timestamp()
    #update_difficulty()
    update_subsity()
    update_hashrate()
    update_hashvalue()
    update_hashprice()
    update_cost() # really, just the help_text bit of it
    update_satsperth()
    update_fiatperth()
    update_eff()
    # update_resell()
    update_hashexpense()
