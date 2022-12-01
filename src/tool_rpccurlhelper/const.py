APP_TITLE = "bitcoin-cli RPC curl Formatter"

APP_DESCRIPTION = """
This tool will format a curl command for you to use with bitcoin-cli.  It will also run the command for you if you want.  It will load your authentication settings for you so you don't have to enter them every time.

Note: This is for Bitcoin Core version x.x.x - FYI... Changes to bitcoin core may not be reflected here

"""

DEFAULT_NODE_IP_ADDRESS = '127.0.0.1'
DEFAULT_NODE_PORT = '8332'

PIN_USERNAME = 'username'
PIN_PASSWORD = 'password'
PIN_USE_COOKIE = 'use_cookie'
PIN_HOST = 'ip_address'
PIN_PORT = 'port'
PIN_METHOD_SELECT = "method_select"
PIN_GENERATED_CMD = "generated_cmd"

BLOCKCHAIN_RPCS = {
    "getbestblockhash": """
        ```getbestblockhash```
    
        Returns the hash of the best (tip) block in the most-work fully-validated chain.""",

    "getblock": """
        ```getblock "blockhash" ( verbosity )```

        If verbosity is 0, returns a string that is serialized, hex-encoded data for block ‘hash’.

        If verbosity is 1, returns an Object with information about block ‘hash’.

        If verbosity is 2, returns an Object with information about block ‘hash’ and information about each transaction.

        ### Argument #1 - blockhash

        Type: string, required

        The block hash

        ### Argument #2 - verbosity

        Type: numeric, optional, default=1

        0 for hex-encoded data, 1 for a json object, and 2 for json object with transaction data""",

    "getblockchaininfo": """
        ```getblockchaininfo```

        Returns an object containing various state info regarding blockchain processing.""",

    "getblockcount": """
        ```getblockcount```

        Returns the height of the most-work fully-validated chain.

        The genesis block has height 0.""",

    "getblockfilter": """
        ```getblockfilter "blockhash" ( "filtertype" )```

        Retrieve a BIP 157 content filter for a particular block.

        ### Argument #1 - blockhash

        Type: string, required

        The hash of the block

        ### Argument #2 - filtertype

        Type: string, optional, default=basic

        The type name of the filter""",
    "getblockhash": """""",
    "getblockheader": """""",
    "getblockstats": """""",
    "getchaintips": """""",
    "getchaintxstats": """""",
    "getdifficulty": """""",
    "getmempoolancestors": """""",
    "getmempooldescendants": """""",
    "getmempoolentry": """""",
    "getmempoolinfo": """""",
    "getrawmempool": """""",
    "gettxout": """""",
    "gettxoutproof": """""",
    "gettxoutsetinfo": """""",
    "preciousblock": """""",
    "pruneblockchain": """""",
    "savemempool": """""",
    "scantxoutset": """""",
    "verifychain": """""",
    "verifytxoutproof": """"""
}

# a list of dicts
# list = [
#     {"name": "John", "age": 30,