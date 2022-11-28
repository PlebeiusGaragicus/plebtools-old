# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

"""
This module contains the callbacks to the pywebio fields and
a lot of the code that runs the pywebio user interface
"""

# TODO - remember!!!! run(method={...}) should be in a try: block so that output.info_popup can be run for the user!!!

# TODO
#     """ There is a global instance of a 'bitcoin node helper' in config.py - this function
#     initializes that instance and verifies that it can pull data from it (by calling getblockchaininfo)

#     If you supplied a username/password in the SETTINGS file, it will be used to setup the node.
#     If you didn't, then DATA_DIRECTORY will be used to pull Bitcoin Core's .cookie file.
#     If that doesn't work the program will show the user an error saying that a node could not be found/setup,
#         and the functionality will default back to only being able to use current Bitcoin metrics for projections/calculations - which is fine.

#     Note to self:  This function is as easy to 'get right' as my implementation of BitcoinNodeHelper allows.. also the specifics of my implementation inside the app - how could this be done better?

# TODO - watt dollar!?!?!?!?
# pin.put_input(name='wattdollar', label="WattDollar", readonly=True, value='', help_text="The product of an ASIC’s watts/Th multiplied by $/Th")


import logging
import datetime

from pywebio import pin
from pywebio import output

from OSINTofBlockchain.BitcoinData import (
    BitcoinNodeHelper,
    coinbase_API,
    blockchaininfo_API
)

from .constants import *
from . import config

from . import callbacks

from .popup import (
    popup_breakeven_analysis,
    popup_currencyconverter,
    popup_difficulty_history,
    popup_fee_analysis,
    popup_price_history
)




def setup_node():
    # SETUP A BITCOIN NODE, IF POSSIBLE
    logging.debug(f"{config.my_node=}")
    try:
        # done - one line... all the logic is inside this class and everything can be set inside the ./SETTINGS file, if desired... but you don't need to... it should work this way 'out of the box' after an install with "brew install bitcoin" ... I think this is the optimal way.
        config.my_node = BitcoinNodeHelper()
    except Exception as e:
        config.my_node = None
        logging.error(f"ERROR: could not create instance of BitcoinNodeHelper - can't pull data from a node!\n{e}", exc_info=True)
    logging.debug(f"{config.my_node=}")


def view_node_stats():
    """ TODO
    """
    pass


def resolve_node_issue():
    """ TODO
    """
    setup_node()
    pass


def refresh() -> None:
    """ This function is called (1) at startup and (2) when the "refresh data" button is pushed

        Use this function to setup a node if one hasn't been already TODO - maybe we can 'reinitialize it?' - why not?  That way if there is an error setup, the user can edit the SETTINGS file, for instance, and just click refresh and stay in the app the whole time.

    """

    setup_node()

    output.toast("refreshing network data...", color='info')
    #setup.download_bitcoin_network_data()
    pin.pin[PIN_BTC_PRICE_NOW] = pin.pin[PIN_BOUGHTATPRICE] = coinbase_API.query_coinbase_bitcoin_spot_price()

    # TODO - DEBUG VALUES
    # TODO RENAME COST TO TOTAL_MINER_CAPITAL_COST
    # TODO RENAME HASHRATE TO TOTAL HASHRATE
    # TODO RENAME WATTAGE TO TOTAL_MACHINE_WATTAGE
    pin.pin[PIN_MACHINE_COST_UPFRONT] = 5000
    pin.pin[PIN_WATTAGE] = 3000
    pin.pin[PIN_HASHRATE] = 90

    if config.my_node == None:
        pin.pin[PIN_HEIGHT] = blockchaininfo_API.query_blockchaininfo_bitcoin_height()
        pin.pin[PIN_NETWORKDIFFICULTY] = blockchaininfo_API.query_blockchaininfo_bitcoin_difficulty()
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



###############################
def show_projection():
    """ THIS FUNCTION TAKES THE VALUES FROM THE INPUT FIELDS AND RUNS THE PROJECTION...
    """
    output.toast("calculating...", color='warn', duration=1)
    logging.info("running show_projection()")

    # make_projection(
    #     current_height=get_entered_height(),
    #     months_to_project=get_entered_months(),
    #     difficulty=get_entered_difficulty(),
    #     ngf=get_entered
    #     )
    # make_projection(
    #     months, height, avgfee, hashrate, wattage,
    #                     price, pricegrow, pricegrow2, pricelag,
    #                     network_difficulty, hashgrow,
    #                     kWh_rate, opex,capex_in_sats, resale, poolfee
    #                     )


    return

    with output.use_scope('projection', clear=True):
        output.put_markdown( "# PROJECTION SUMMARIES:" )

    res = calculate_projection(
        months = months,
        height = height,
        avgfee = avgfee,
        hashrate = hashrate,
        wattage = wattage,
        price = price,
        pricegrow = pricegrow,
        pricegrow2 = pricegrow2,
        pricelag = pricelag,
        network_difficulty = diff,
        hashgrow = hashgrow,
        kWh_rate = kWh_rate,
        opex = opex,
        capex_in_sats = btc(capex, bitcoin_price=price_when_bought),
        resale = resell,
        poolfee = poolfee,
    )

    config.analysis_number += 1

    table = make_table_string(res)
    with output.use_scope("result"):
        output.put_collapse(title=f"analysis #{config.analysis_number}", content=[
            output.put_html( pretty_graph(res) ),
            output.put_collapse("Monthly Breakdown Table", content=[
            output.put_markdown( table ),
            output.put_table(tdata=[[
                    output.put_file('projection.csv', content=b'123,456,789'),
                    output.put_text("<<-- Download results as CSV file")
                ]])
        ])
        ], position=output.OutputPosition.TOP, open=True)

    output.toast("done.", color='success', duration=1)




def save_all_vars(vars: dict) -> None:
    logging.debug(f"save_all_vars({vars=})")


####################################
def show_interface():
    """ This is basically the web page in one function.

        This function displays the items on the screen that the user interacts with.

        The items (text fields and buttons) have callbacks which make them interactive. A
        thread was started earlier that is keeping PyWebIO alive so these callbacks can be
        triggered.
    """

    with output.use_scope("TOP"):
        output.put_markdown( MAIN_TEXT )
        output.put_collapse(title="See also:", content=[
            output.put_markdown( REFERENCE_TEXT )
        ]),
        output.put_collapse(title="ANALYSIS TOOLS:", content=[
            output.put_button("fiat <-> bitcoin converter", onclick=popup_currencyconverter, color='info'),
            output.put_button("refresh data", onclick=refresh),
            output.put_button("break-even analysis", onclick=popup_breakeven_analysis, color='info'),
            output.put_button("block fee analysis", onclick=popup_fee_analysis),
            output.put_button("price history analysis", onclick=popup_price_history),
            output.put_button("hashrate history analysis", onclick=popup_difficulty_history)
        ])



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

    refresh()
