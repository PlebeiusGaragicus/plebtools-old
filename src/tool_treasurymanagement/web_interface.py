# TODO - remember!!!! run(method={...}) should be in a try: block so that output.info_popup can be run for the user!!!

import os
import json
import logging
import datetime
import dotenv

from pywebio import output, pin, config

from src.api.authproxy import AuthServiceProxy, JSONRPCException, CustomJsonEncoder

from .config import *
from .constants import *
from . import callbacks
from .projection import show_projection

from src.api.coinbase import spot_price
from src.api.blockchaininfo import bitcoin_height, bitcoin_difficulty

def setup_node():
    user = os.getenv('RPC_USER')
    pswd = os.getenv('RPC_PASS')
    host = os.getenv('RPC_HOST')
    port = os.getenv('RPC_PORT')

    rpc_url = f"http://{user}:{pswd}@{host}:{port}"
    node = AuthServiceProxy(rpc_url)
    # rpc_connection = AuthServiceProxy(rpc_url)
    logging.debug(f"{rpc_url=}")

    global tip
    try:
        tip = node.getblockcount()
    except JSONRPCException as e:
        output.toast(f"ERROR: {e}", color='error', duration=10)
        output.toast(f"Check your RPC connection settings", color='warn', duration=10)
        return

    height = pin.pin[PIN_HEIGHT]

    if height == None or height == '':
        output.toast("Enter a block height to read OP_RETURN data")
        return

    if height > tip:
        output.toast(f"Block height {height} is higher than the current tip {tip}", position='top', duration=3)
        return

    hash = node.getblockhash( height )
    try:
        block = node.getblock( hash, 2 ) # call with verbosity 2 in order to get tx details
    except JSONRPCException as e:
        output.toast(f"ERROR: {e}", color='error', duration=10)
        return
    block = json.loads( json.dumps( block , cls=CustomJsonEncoder) )







    return
    # SETUP A BITCOIN NODE, IF POSSIBLE
    logging.debug(f"{config.my_node=}")
    try:
        # done - one line... all the logic is inside this class and everything can be set inside the ./SETTINGS file, if desired... but you don't need to... it should work this way 'out of the box' after an install with "brew install bitcoin" ... I think this is the optimal way.
        config.my_node = BitcoinNodeHelper()
    except Exception as e:
        config.my_node = None
        logging.error(f"ERROR: could not create instance of BitcoinNodeHelper - can't pull data from a node!\n{e}", exc_info=True)
    logging.debug(f"{config.my_node=}")



def load_network_state() -> None:

    setup_node()

    output.toast("refreshing network data...", color='info')
    #setup.download_bitcoin_network_data()
    # TODO - need to fail gracefully if I can't get the price.. just alert the user!!!
    pin.pin[PIN_BTC_PRICE_NOW] = pin.pin[PIN_BOUGHTATPRICE] = spot_price()

    # TODO - DEBUG VALUES
    # TODO RENAME COST TO TOTAL_MINER_CAPITAL_COST
    # TODO RENAME HASHRATE TO TOTAL HASHRATE
    # TODO RENAME WATTAGE TO TOTAL_MACHINE_WATTAGE
    pin.pin[PIN_MACHINE_COST_UPFRONT] = 5000
    pin.pin[PIN_WATTAGE] = 3000
    pin.pin[PIN_HASHRATE] = 90

    if config.my_node == None:
        pin.pin[PIN_HEIGHT] = bitcoin_height()
        pin.pin[PIN_NETWORKDIFFICULTY] = bitcoin_difficulty()
    else:
        pin.pin[PIN_HEIGHT] = config.my_node.blockchain_state.block_height
        pin.pin[PIN_NETWORKDIFFICULTY] = config.my_node.blockchain_state.difficulty

    callbacks.update_timestamp()
    callbacks.update_numbers() # this is the callback function used to ensure all UI read_only fields are updated

    with output.use_scope("TOP"):
        if config.my_node == None:
            output.put_button("NO NODE SETUP - CLICK HERE TO RESOLVE", onclick=resolve_node_issue, color='danger')
        else:
            if config.my_node.pruned_height != 0: # IS PRUNED
                output.put_button("PRUNED NODE RUNNING - CLICK TO VIEW STATUS", onclick=view_node_stats, color='info')
                ph = config.my_node.pruned_height
                output.put_text(f"Node is pruned to height: {ph} : ({datetime.datetime.fromtimestamp(config.my_node.get_block_time(ph))})")
            else:
                output.put_button("NODE RUNNING - CLICK TO VIEW STATUS", onclick=view_node_stats, color='success')

    output.toast("refresh done", color='success')


def trythis(throwaway):
    if throwaway == None:
        pin.pin['test'] = 0


def save_all_vars(vars: dict) -> None:
    logging.debug(f"save_all_vars({vars=})")


####################################
@output.use_scope('main', clear=True)
def show_interface():

    output.put_markdown(f"# {APP_TITLE}")

    output.put_markdown("### BITCOIN NETWORK STATE")
    output.put_table([[
        pin.put_input(name=PIN_BTC_PRICE_NOW, type='float', label="Bitcoin price $", value=0),
        pin.put_input(name=PIN_HEIGHT, type='float', label="blockchain height", value=0),
        pin.put_input(name=PIN_AVERAGEFEE, type='float', label="average block fee", value=0),
        pin.put_input(name=PIN_SUBSIDY, type='text', label="total block reward", value=0, readonly=True)
    ],[
        pin.put_input(name=PIN_NETWORKDIFFICULTY, type='float', label="network difficulty", value=0),
        pin.put_input(name=PIN_NETWORKHASHRATE, type='text', label="network TH/s", value=0, readonly=True),
        pin.put_input(name=PIN_HASHVALUE, type='text', label="hash value", value=0, readonly=True, help_text='satoshi earned per Terahash per day'),
        pin.put_input(name=PIN_HASHPRICE, type='text', label="hash price", value=0, readonly=True, help_text='hash value denominated in fiat at today\'s price')
        ]])
    pin.pin_on_change(name=PIN_BTC_PRICE_NOW, onchange=callbacks.update_numbers)
    pin.pin_on_change(name=PIN_HEIGHT, onchange=callbacks.update_height)
    pin.pin_on_change(name=PIN_AVERAGEFEE, onchange=callbacks.update_numbers)
    pin.pin_on_change(name=PIN_NETWORKDIFFICULTY, onchange=callbacks.update_numbers)



    output.put_markdown("### CAPTIAL EXPENDITURE - UPFRONT COST")
    output.put_collapse("Mining Hardware upfront cost", content=[
        output.put_table(tdata=[[
            pin.put_input(name=PIN_MACHINE_COST_UPFRONT, type='float', label="Upfront fiat cost of mining hardware", value=0),
            pin.put_input(name=PIN_MACHINE_BOUGHTATPRICE, type='float', label="Bitcoin price at time of purchase", value=0),
            pin.put_input(name=PIN_MACHINE_OPCOST, type='float', label="Opportunity cost", value=0)
        ]])
    ], open=True)
    pin.pin_on_change(name=PIN_BOUGHTATPRICE, onchange=callbacks.update_numbers)
    pin.pin_on_change(name=PIN_MACHINE_COST_UPFRONT, onchange=callbacks.update_numbers)
    output.put_collapse("Infrastructure upfront cost", content=[
        output.put_table(tdata=[[
            pin.put_input(name=PIN_INFRA_COST_UPFRONT, type='float', label="Upfront fiat cost of infrastructure", value=0),
            pin.put_input(name=PIN_INFRA_BOUGHTATPRICE, type='float', label="Bitcoin price at time of purchase", value=0),
            pin.put_input(name=PIN_INFRA_OPCOST, type='float', label="Opportunity cost", value=0)
        ]])
    ], open=True)



    output.put_markdown("### CAPITAL EXPENDITURE - FINANCING")
    output.put_collapse("Mining hardware loan details ", content=[
        output.put_table(tdata=[[
            pin.put_input(name=PIN_MACHINE_LOAN_PRINCIP, type='float', label="Loan principal", value=0),
            pin.put_input(name=PIN_MACHINE_LOAN_INTEREST, type='float', label="Toal interest", value=0),
            pin.put_input(name=PIN_MACHINE_LOAN_REPAYMENT, type='float', label="Repayment period (months)", value=0),
            pin.put_input(name=PIN_MACHINE_LOAN_MONTHLY, type='float', label="Monthly bill", readonly=True, value=0)
        ]])
    ])
    pin.pin_on_change(PIN_MACHINE_LOAN_PRINCIP, onchange=callbacks.update_financing)
    pin.pin_on_change(PIN_MACHINE_LOAN_INTEREST, onchange=callbacks.update_financing)
    pin.pin_on_change(PIN_MACHINE_LOAN_REPAYMENT, onchange=callbacks.update_financing)
    pin.pin_on_change(PIN_MACHINE_LOAN_PRINCIP, onchange=callbacks.update_financing)
    output.put_collapse("Infrastructure loan details", content=[
        output.put_table(tdata=[[
            pin.put_input(name=PIN_INFRA_LOAN_PRINCIP, type='float', label="Loan principal", value=0),
            pin.put_input(name=PIN_INFRA_LOAN_INTEREST, type='float', label="Toal interest", value=0),
            pin.put_input(name=PIN_INFRA_LOAN_REPAYMENT, type='float', label="Repayment period (months)", value=0),
            pin.put_input(name=PIN_INFRA_LOAN_MONTHLY, type='float', label="Monthly bill", readonly=True, value=0)
        ]])
    ])
    pin.pin_on_change(PIN_INFRA_LOAN_PRINCIP, onchange=callbacks.update_financing)
    pin.pin_on_change(PIN_INFRA_LOAN_INTEREST, onchange=callbacks.update_financing)
    pin.pin_on_change(PIN_INFRA_LOAN_REPAYMENT, onchange=callbacks.update_financing)



    #pin.put_input(PIN_HASHEXPENSE, type='text', label='hash expense', value=0, readonly = True, help_text='your cost-of-production per Terahash per day'),
    output.put_markdown("### OPERATIONAL EXPENDITURE - OPEX")
    output.put_table([[
        pin.put_input(PIN_KWH_RATE, type='float', label='cost per kilowatt-hour: $', value=DEFAUL_KPKWH),
        pin.put_input(PIN_POOLFEE, type='float', label='mining pool fee: %', value= DEFAULT_POOL_FEE),
        pin.put_input(PIN_OPEX, type='float', label='All other monthly costs: $', value=0)
    ],[
        pin.put_input(PIN_WATTAGE_OTHER, type='float', label='Wattage - non-mining sources: #', value=0),
        pin.put_input(PIN_REV_SHARE, type='float', label='Revenue sharing: %', value=0)
        ]
    ])
    pin.pin_on_change(PIN_KWH_RATE, onchange=callbacks.update_numbers)
    pin.pin_on_change(PIN_POOLFEE, onchange=callbacks.update_numbers)
    pin.pin_on_change(PIN_OPEX, onchange=callbacks.update_numbers)



    output.put_markdown("### TAXES")
    output.put_collapse("Decuctions, tax rate, depreciation", content=[
        output.put_table([[
            pin.put_input(name=PIN_MAXDEDUCT, type='number', label="Amount allowed to deduct", value=0),
            pin.put_input(name=PIN_MARGINALTAX, type='number', label="Marginal Tax rate", value=0),
            pin.put_input(name=PIN_MACHINE_DEPRECIATE, type='number', label="Machine depreciation / year: $", value=0),
            pin.put_input(name=PIN_INFRA_DEPRECIATE, type='number', label="Infrastructure depreciation / year: $", value=0)
        ]])
    ])
    # output.put_markdown("### hardware resale / depreciation recapture")
    # output.put_table([[
    #         pin.put_checkbox(name=PIN_NEVERSELL, options=[OPTION_NEVERSELL], value=False),
    #         pin.put_input(name=PIN_RESELL, type='number', label="Resale %", help_text="% percent of purchase price", value=DEFAULT_RESELL),
    #         pin.put_input(name=PIN_RESELL_READONLY, type='text', label="Resale price", readonly=True)
    # ]])
    # pin.pin_on_change(name=PIN_NEVERSELL, onchange=callbacks.toggle_resell) # this toggles (disable/enables) other input fields
    # pin.pin_on_change(PIN_RESELL, onchange=callbacks.update_numbers)



    output.put_markdown("### MINING MACHINE SPECIFICATIONS")
    output.put_table([[
        pin.put_input(name=PIN_WATTAGE, type='float', label="Total wattage of miners"),
        pin.put_input(name=PIN_HASHRATE, type='float', label='Total hashrate (in terahash)'),
        pin.put_input(name=PIN_EFF, type='float', label="Hashing efficiency (W/TH)", readonly=True)
    ]])
    pin.pin_on_change(name=PIN_WATTAGE, onchange=callbacks.update_numbers)
    pin.pin_on_change(name=PIN_HASHRATE, onchange=callbacks.update_numbers)



    output.put_markdown("### PROJECTION PARAMETERS")
    output.put_table([[
        pin.put_input(name=PIN_MONTHSTOPROJECT, type='float', value=DEFAULT_MONTHSTOPROJECT, label='Months to simulate: #'),
        pin.put_input(name=PIN_DIFFADJUST, type='float', value=DEFAULT_DIFFADJUST, label='Difficult adjustment: %'),
        pin.put_input(name=PIN_CASH, type='float', value=0, label='Cash on hand: $')
    ]])


    output.put_button( 'Simulate!', onclick=show_projection, color='success' )

    load_network_state()

@config(title=APP_TITLE, theme='dark')
def main():

    dotenv.load_dotenv()

    setup_node()

    show_interface()
