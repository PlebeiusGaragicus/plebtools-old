import imp
import logging

from pywebio import output, pin

from OSINTofBlockchain.BitcoinData.helpers import btc

from Apps import config
from .constants import *


























# TODO - remember!!!! run(method={...}) should be in a try: block so that output.info_popup can be run for the user!!!

# ###############################
# def make_projection() -> None:
#     """ THIS FUNCTION TAKES THE VALUES FROM THE INPUT FIELDS AND RUNS THE PROJECTION...
#     """
#     output.toast("calculating...", color='warn', duration=1)
#     logging.info("running show_projection()")

#     var = {}
#     var['months'] = get_entered_months()
#     var['height'] = get_entered_height()
#     var['avgfee'] = get_entered_fees()
#     var['hashrate'] = get_entered_hashrate()
#     var['wattage'] = get_entered_wattage()
#     var['price'] = get_entered_price()
#     var['price_when_bought'] = get_entered_bought_price()

#     var['pricegrow'] = float(pin.pin[PIN_PRICEGROW] / 100)
#     var['pricegrow2'] = float(pin.pin[PIN_PRICEGROW2] / 100)
#     var['pricelag'] = int(pin.pin[PIN_LAG])
    
#     var['diff'] = get_entered_difficulty()
#     var['hashgrow'] = float(pin.pin[PIN_HASHGROW] / 100)

#     var['kWh_rate'] = get_entered_rate()
#     var['opex'] = get_entered_opex()
#     var['capex'] = get_entered_machine_cost()
#     var['resell'] = get_entered_resell_percent()
#     var['poolfee'] = get_entered_poolfee()

#     save_all_vars( var )

#     #if None in (months, height, avgfee, hashrate, wattage, price,
#     #            pricegrow, pricegrow2, pricelag, diff,
#     #            hashgrow, kWh_rate, opex, capex, resell, poolfee):
#     if None in var.items():
#         output.toast("Error - an input field was left blank (or is invalid)")
#         logging.error("None variable passed to calculate_projection()")
#         return

#     with output.use_scope('projection', clear=True):
#         output.put_markdown( "# PROJECTION SUMMARIES:" )

#     res = calculate_projection(
#         months = months,
#         height = height,
#         avgfee = avgfee,
#         hashrate = hashrate,
#         wattage = wattage,
#         price = price,
#         pricegrow = pricegrow,
#         pricegrow2 = pricegrow2,
#         pricelag = pricelag,
#         network_difficulty = diff,
#         hashgrow = hashgrow,
#         kWh_rate = kWh_rate,
#         opex = opex,
#         capex_in_sats = btc(capex, bitcoin_price=price_when_bought),
#         resale = resell,
#         poolfee = poolfee,
#     )

#     config.analysis_number += 1

#     table = make_table_string(res)
#     with output.use_scope("result"):
#         output.put_collapse(title=f"analysis #{config.analysis_number}", content=[
#             output.put_html( pretty_graph(res) ),
#             output.put_collapse("Monthly Breakdown Table", content=[
#             output.put_markdown( table ),
#             output.put_table(tdata=[[
#                     output.put_file('projection.csv', content=b'123,456,789'),
#                     output.put_text("<<-- Download results as CSV file")
#                 ]])
#         ])
#         ], position=output.OutputPosition.TOP, open=True)

#     output.toast("done.", color='success', duration=1)




# def save_all_vars(vars: dict) -> None:
#     logging.debug(f"save_all_vars({vars=})")
    



# def show_projection() -> None:
#     """
#         This takes all the entered variables, runs an earnings projection and displays the results
#     """
#     output.toast("calculating...", color='warn', duration=1)
#     logging.info("running show_projection()")

#     months = get_entered_months()
#     height = get_entered_height()
#     avgfee = get_entered_fees()
#     hashrate = get_entered_hashrate()
#     wattage = get_entered_wattage()
#     price = get_entered_price()
#      # TODO figure out my strategy for this thang!!
#     price_when_bought = get_entered_bought_price()

#     pricegrow = float(pin.pin[PIN_PRICEGROW] / 100)
#     pricegrow2 = float(pin.pin[PIN_PRICEGROW2] / 100)
#     pricelag = int(pin.pin[PIN_LAG])
    
#     diff = get_entered_difficulty()
#     hashgrow = float(pin.pin[PIN_HASHGROW] / 100)

#     kWh_rate = get_entered_rate()
#     opex = get_entered_opex()
#     capex = get_entered_machine_cost()
#     resell = get_entered_resell_percent()
#     poolfee = get_entered_poolfee()

#     if None in (months, height, avgfee, hashrate, wattage, price,
#                 pricegrow, pricegrow2, pricelag, diff,
#                 hashgrow, kWh_rate, opex, capex, resell, poolfee):
#         output.toast("Error - an input field was left blank (or is invalid)")
#         logging.error("None variable passed to calculate_projection()")
#         return

#     with output.use_scope('projection', clear=True):
#         output.put_markdown( "# PROJECTION SUMMARIES:" )


#     res = calculate_projection(
#         months = months,
#         height = height,
#         avgfee = avgfee,
#         hashrate = hashrate,
#         wattage = wattage,
#         price = price,
#         pricegrow = pricegrow,
#         pricegrow2 = pricegrow2,
#         pricelag = pricelag,
#         network_difficulty = diff,
#         hashgrow = hashgrow,
#         kWh_rate = kWh_rate,
#         opex = opex,
#         capex_in_sats = btc(capex, bitcoin_price=price_when_bought),
#         resale = resell,
#         poolfee = poolfee,
#     )

#     config.analysis_number += 1

#     table = make_table_string(res)
#     with output.use_scope("result"):
#         output.put_collapse(title=f"analysis #{config.analysis_number}", content=[
#             output.put_html( pretty_graph(res) ),
#             output.put_collapse("Monthly Breakdown Table", content=[
#             output.put_markdown( table ),
#             output.put_table(tdata=[[
#                     output.put_file('projection.csv', content=b'123,456,789'),
#                     output.put_text("<<-- Download results as CSV file")
#                 ]])
#         ])
#         ], position=output.OutputPosition.TOP, open=True)

#     output.toast("done.", color='success', duration=1)


