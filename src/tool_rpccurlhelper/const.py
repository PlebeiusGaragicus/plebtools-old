APP_TITLE = "Bitcoin RPC Curl Helper"

# TODO is this the 'official'??
TOP_TEXT = """
Note: This is for Bitcoin Core version x.x.x - FYI...
"""

DEFAULT_NODE_IP_ADDRESS = '127.0.0.1'
DEFAULT_NODE_PORT = '8332'

PIN_USERNAME = 'username'
PIN_PASSWORD = 'password'
PIN_USE_COOKIE = 'use_cookie'
PIN_IPADDRESS = 'ip_address'
PIN_PORT = 'port'
PIN_METHOD_SELECT = "method_select"
PIN_GENERATED_CMD = "generated_cmd"

# TODO - include a short description and make a callback that will update the description and show the user what parameters are needed
BLOCKCHAIN_RPCS = [
    "getbestblockhash",
    "getblock",
    "getblockchaininfo",
    "getblockcount",
    "getblockfilter",
    "getblockhash",
    "getblockheader",
    "getblockstats",
    "getchaintips",
    "getchaintxstats",
    "getdifficulty",
    "getmempoolancestors",
    "getmempooldescendants",
    "getmempoolentry",
    "getmempoolinfo",
    "getrawmempool",
    "gettxout",
    "gettxoutproof",
    "gettxoutsetinfo",
    "preciousblock",
    "pruneblockchain",
    "savemempool",
    "scantxoutset",
    "verifychain",
    "verifytxoutproof",
]
