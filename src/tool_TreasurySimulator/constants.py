MAIN_TEXT = """# Open-Source Bitcoin Mining Profitability Calculator

__The goal of this project is to inspire__ people to learn about bitcoin's built-in incentive structure - mining.

__The purpose of this tool is to__ help bitcoin miners make sound business decisions - namely, how much to pay for equipment and what operating environment is needed to be profitable.

"""

REFERENCE_TEXT = """
Also see:
[Braiins Insights](https://insights.braiins.com/en/profitability-calculator/) <-- the gold-standard
[red dirt mining](https://reddirtmining.io/calculator) <-- brand-new, and open-source
[Crypto compate](https://www.cryptocompare.com/mining/calculator/btc) <-- this one sucks

"""

### DEFAULT NUMBERS FOR THE USER INPUT FIELDS
DEFAULT_POOL_FEE = 0 # per-cent (2 == 2%; 0.1 == 0.1%)
DEFAUL_KPKWH = 0.075 # fiats per kWh
#DEFAULT_OPEX = 15 # fiats
DEFAULT_MONTHSTOPROJECT = 36
DEFAULT_RESELL = 75
DEFAULT_PRICEGROW = 2
DEFAULT_PRICEGROW2 = 18
DEFAULT_LAG = 3
DEFAULT_DIFFADJUST = 1.2

# THESE ARE THE NAMES OF THE 'PIN' INPUT FIELDS

# MACHINE UPFRONT
PIN_MACHINE_COST_UPFRONT = 'machine_upfront'
PIN_MACHINE_BOUGHTATPRICE = 'machine_btc_price'
PIN_MACHINE_OPCOST = 'machine_op_cost'

# INFRA UPFRONT
PIN_INFRA_COST_UPFRONT = 'infra_upfront'
PIN_INFRA_BOUGHTATPRICE = 'infra_btc_price'
PIN_INFRA_OPCOST = 'infra_op_cost'

# MACHINE LOAN
PIN_MACHINE_LOAN_PRINCIP = 'machine_loan_principal'
PIN_MACHINE_LOAN_INTEREST = 'machine_loan_interest'
PIN_MACHINE_LOAN_REPAYMENT = 'machine_loan_repayment'
PIN_MACHINE_LOAN_MONTHLY = 'machine_loan_monthly'

# INFRA LOAN
PIN_INFRA_LOAN_PRINCIP = 'infra_loan_principal'
PIN_INFRA_LOAN_INTEREST = 'infra_loan_interest'
PIN_INFRA_LOAN_REPAYMENT = 'infra_loan_repayment'
PIN_INFRA_LOAN_MONTHLY = 'infra_loan_monthly'








PIN_WATTAGE = 'wattage'
PIN_HASHRATE = 'hashrate'
PIN_BOUGHTATPRICE = 'boughtatprice'
PIN_WATTDOLLAR = 'wattdollar'

PIN_BTC_PRICE_NOW = 'price'
PIN_PRICEGROW = 'pricegrow'
PIN_PRICEGROW_SLIDER = 'pricegrow_slider'
PIN_PRICEGROW2_SLIDER = 'pricegrow2_slider'
PIN_LAG = 'lag'
PIN_PRICEGROW2 = 'pricegrow2'
# miner analysis
#PIN_CAPEX = 'satsPerTH'
PIN_COST_SLIDER = 'cost_slider'
PIN_EFF = 'eff'
PIN_EFF_SLIDER = 'eff_slider'
PIN_SAT_PER_TH = 'satsperth'
PIN_FIAT_PER_TH = 'fiatperth'
# bitcoina network state
PIN_HEIGHT = 'height'
PIN_SUBSIDY = 'subsidy'
PIN_AVERAGEFEE = 'avgfee'
PIN_NETWORKDIFFICULTY = 'diff'
PIN_NETWORKHASHRATE = 'nh'
PIN_HASHVALUE = 'hashvalue'
PIN_HASHPRICE = 'hashprice'
PIN_DIFFADJUST = 'diff_adjust'
PIN_CASH = 'cash'

# PROJECTION PARAMETERS
PIN_KWH_RATE = 'costkwh'
PIN_POOLFEE = 'poolfee'
PIN_OPEX = 'opex'
PIN_REV_SHARE = 'rev_share'
PIN_WATTAGE_OTHER = 'watt_other'

# TAXES
PIN_MAXDEDUCT="allowed_deduct"
PIN_MARGINALTAX="marginal_tax"
PIN_MACHINE_DEPRECIATE="machine_depreciation"
PIN_INFRA_DEPRECIATE="infra_depreciation"


PIN_HASHEXPENSE = 'hashexpense'
PIN_MONTHSTOPROJECT = 'months'
PIN_NEVERSELL = 'neversellmachine'
PIN_RESELL ='resell'
PIN_RESELL_READONLY = 'resale_dollars'

# This is the option 'list' for the PIN_NEVERSELL checkbox
# Change this to change the text displayed
OPTION_NEVERSELL = "Never sell machine"

# THESE ARE DICTIONARY ITEM NAMES FOR THE RESULTS DICT WE CALCULATE
    ## CONSTANTS
KEY_MONTHS_TO_PROJECT = 'months'
KEY_START_HEIGHT = 'start height'
KEY_AVGFEE = 'avgfee'
KEY_MY_HASHRATE = 'my hashrate'
KEY_WATTAGE = 'wattage'
KEY_START_PRICE = 'start price'
KEY_PRICE_GROWTH = 'price growth'
KEY_PRICE_GROWTH2 = 'price grow2'
KEY_PRICE_LAG = 'price lag'
KEY_START_NH = 'starting nh'
KEY_HASH_GROWTH = 'hash growth'
#KEY_HASH_GROWTH2 : hashgrow2,
KEY_MONTHLY_OPEX = 'opex'
KEY_CAPEX_SATS = 'capex'
KEY_RESALE = 'resale'
#KEY_RESALE_LOWER = 'resale lower'
KEY_POOLFEE = 'poolfee'
KEY_RATE_KWH = 'rate kwh'
KEY_ESTIMATED_HEIGHT = 'height'
KEY_ESTIMATED_NETWORK_HASHRATE = 'network_hashrate'
KEY_ESTIMATED_PRICE = 'price btc'
KEY_HASHVALUE = 'hv'
KEY_KWH = 'kwh'
# THE SATS SOLD EVERY MONTH TO COVER THE GIVEN EXPENSE
KEY_SOLD_ELECTRICITY = 'sold_electricity'
KEY_SOLD_OPEX = 'sold_OPEX'
KEY_SOLD_CAPEX = 'sold_CAPEX'
KEY_BREAKEVEN_PRICE = 'BE price'
KEY_BREAKEVEN_PRICE_P20P = 'BE price 20%'
KEY_BREAKEVEN_NH = 'BE hashrate'


    # res = {
    #     # THESE ARE THE INPUTS TO THE CALCULATION
    #     KEY_MONTHS_TO_PROJECT : months,
    #     KEY_START_HEIGHT : height,
    #     KEY_AVGFEE : avgfee,
    #     KEY_MY_HASHRATE : hashrate,
    #     KEY_WATTAGE : wattage,
    #     KEY_START_PRICE : price,
    #     KEY_PRICE_GROWTH : pricegrow,
    #     KEY_PRICE_GROWTH2 : pricegrow2,
    #     KEY_PRICE_LAG : pricelag,
    #     KEY_HASH_GROWTH : hashgrow,
    #     KEY_MONTHLY_OPEX : opex,
    #     KEY_CAPEX_SATS : capex_in_sats, # sats
    #     KEY_RESALE : resale,
    #     KEY_POOLFEE : poolfee, # whole number percent / need to divide by 100
    #     KEY_RATE_KWH : kWh_rate,
    #     # THE REST OF THESE BELOW ARE CALCULATED OFF OF THE ABOVE GIVEN VARIABLES
    #     #HEIGHT AT THE END OF THE MONTH!
    #     KEY_ESTIMATED_HEIGHT : [],
    #     KEY_ESTIMATED_NETWORK_HASHRATE : [],
    #     KEY_ESTIMATED_PRICE : [],
    #     #KEY_ESTIMATED_AVGFEE : [],
    #     # EARNED
    #     KEY_HASHVALUE : [],
    #     # BURNED
    #     KEY_KWH : [],
    #     # THE SATS SOLD EVERY MONTH TO COVER THE GIVEN EXPENSE
    #     KEY_SOLD_ELECTRICITY : [],
    #     KEY_SOLD_OPEX : [],
    #     KEY_SOLD_CAPEX : [],
    #     # DECISION / FOREWARD-LOOKING // PROFIC ASSUMPTION MAKING-DECISION POINTS
    #     KEY_BREAKEVEN_PRICE : [], # at current nh
    #     KEY_BREAKEVEN_PRICE_P20P : [], # plus 20% 'worth my time fee', at current nh
    #     KEY_BREAKEVEN_NH : [], # at estimated price
    # }