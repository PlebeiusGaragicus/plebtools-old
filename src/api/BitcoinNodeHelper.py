# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.



import os
import logging
import json
# from functools import cache
# __OR__
# 'least recently used'
# from functools import lru_cache
# @lru_cache(maxsize=5)
# def example(num: int) -> int:
#     return int * int * int

SETTINGS_FILE_NAME = 'SETTINGS'


class BlockchainCurrentState:
    block_height: int = 0
    latest_block_hash: str = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
    block_time: int = 1231006505
    #nBits: int = 0x1d00ffff
    difficulty: float = 1.0


DEFAULT_NODE_IP_ADDRESS = '127.0.0.1'
DEFAULT_NODE_PORT = '8332'

SETTING_NAME_NODE_IP_ADDRESS = "NODE_IP_ADDRESS"
SETTING_NAME_NODE_PORT = "NODE_PORT"
SETTING_NAME_NODE_USERNAME = "NODE_USERNAME"
SETTING_NAME_NODE_PASSWORD = "NODE_PASSWORD"
SETTING_NAME_NODE_DATA_DIRECTORY = "NODE_DATA_DIRECTORY"


class BitcoinNodeHelper():
    ip_address = None
    port = None

    username = None
    password = None

    cookie = None

    blockchain_state: BlockchainCurrentState = BlockchainCurrentState()
    #is_pruned = None
    pruned_height = None # we combine both isPruned and Pruned_height here

    # we will use RPC calls thru curl to interact with the node - we no longer need to use os.popen with a path
    # although.... this could be implemented in addition in a future release
    #bin_path = None
    # bin_path = "/opt/homebrew/bin/bitcoin-cli"


    ############################################################
    # TODO - I need to be able to write tests for these... that would be NEXT LEVEL
    def __init__(self, username: str = None, password: str = None, data_dir: str = None, ip_address: str = None, port: str = None):
        logging.debug(f"BitcoinNodeHelper.__init__({username=} {password=} {data_dir=} {ip_address=} {port=})")

        # STEP 1 - source ./SETTINGS so we can re-load the environment variables
        os.popen(f"source ./{SETTINGS_FILE_NAME}")
        # TODO .. uh.. then we're sourcing that file twice for every startup--- for the possible occasion
        # TODO probably have a 'reload settings file' button that will source it and then call refresh()

        # STEP 2 - ENSURE ALL VARIABLES ARE SET
        # TODO is there a pythonic way to make this if else a SINGLE LINE?? Like in C++?  if (?) 1 : 2
        if ip_address == None:
            self.ip_address = os.getenv(SETTING_NAME_NODE_IP_ADDRESS)
            if self.ip_address == None:
                self.ip_address = DEFAULT_NODE_IP_ADDRESS
        else:
            self.ip_address = ip_address

        if port == None:
            self.port = os.getenv(SETTING_NAME_NODE_PORT)
            if self.port == None:
                self.port = DEFAULT_NODE_PORT
        else:
            self.port = port
        
        if username == None:
            self.username = os.getenv(SETTING_NAME_NODE_USERNAME)
        else:
            self.username = username
        
        if password == None:
            self.password = os.getenv(SETTING_NAME_NODE_PASSWORD)
        else:
            self.password = password

        # TODO - THIS ALL NEEEEEDS TO BE TESTED1!!!!!!!
        # didn't provide BOTH username and password either to this function (AKA on init of BitcoinNodeHelper object) or in the SETTINGS file??
        if None in (self.username, self.password):
            # then try to find a cookie... ;)
            if data_dir == None:
                data_dir = os.getenv(SETTING_NAME_NODE_DATA_DIRECTORY)
                # oh, you didn't supply the Bitcoin Core data directory of the node you're using?
                if data_dir == None:
                    # the, try to find the default location for your operating system
                    # TODO - here we can read `uname -a` to find the OS, then look in the 'default' location
                    # 'just works' mentality... I'm sure the majority of users will install a node the default way and not have too much to configure
                    logname = os.popen("logname").read().strip('\n') # this isn't working for damn reason
                    logname = os.popen("echo $LOGNAME").read().strip('\n')

                    logging.debug(f"{logname=}")
                    my_os = os.popen("uname").read()
                    logging.debug(f"uname -> {my_os}")

                    if 'Darwin' in my_os:
                        # macOS	$HOME/Library/Application Support/Bitcoin/	/Users/username/Library/Application Support/Bitcoin/bitcoin.conf
                        data_file = f"/Users/{logname}/Library/Application Support/Bitcoin/.cookie"
                        logging.warning(f"no data directory given in SETTINGS file - will try looking in the default location for this operating system, which is:\n{data_file}")
                    else:
                        # Windows	%APPDATA%\Bitcoin\	C:\Users\username\AppData\Roaming\Bitcoin\bitcoin.conf
                        # f"C:\\Users\\{logname}}\\AppData\\Roaming\\Bitcoin\\bitcoin.conf"
                        # Linux	$HOME/.bitcoin/	/home/username/.bitcoin/bitcoin.conf
                        # f"/home/{logname}/.bitcoin/bitcoin.conf"
                        raise NotImplementedError("NOT YET IMPLEMENTED for your operating system.. can't set up this bitcoin node helper... oops")
                    
                    cat_file = os.popen(f"cat \"{data_file}\"").read()
                else:
                    cat_file = os.popen(f"cat \"{data_dir}/.cookie\"").read()

                logging.debug(f".cookie file: '{cat_file}'")
                if cat_file == '':
                    raise NotImplementedError("NO USERNAME/PASSWORD GIVEN AND CANNOT FIND COOKIE FILE - your node may not be running.")
                
                self.username = "__cookie__"
                self.password = cat_file.split(':')[1]

                logging.debug(f"BitcoinNodeHelper using cookie file contents: {cat_file}\nignoring any possible username/password.. setting to None")


        # - state is now setup; so we log output to confirm
        logging.debug(f"Node setup: {self.username=} {self.password=} {self.ip_address=} {self.port=}")

        # STEP 4 - USE VARIABLES AND TRY TO CONNECT
        # NOW WE RUN A COMMAND TO TEST THE SETUP AND PULL THE REST OF THE NEEDED INFORMATION STRAIGHT FROM THE NODE
        #try:
        # Note: This time, we aren't calling run() inside a try block, because in this case, we want exceptions to kill this __init__() and prevent this object from being created... something went wrong in setting up this node and shit just got real... and needs to be addressed
        info = self.run('getblockchaininfo')
        logging.debug(f"getblockchaininfo: {info}")
        # except Exception as e:
        #     logging.error(f"ERROR: could not configure a bitcoin node helper - see debug.log\n{e}")
        #     raise Exception("SHIT BROKE... YOUR NODE ISN'T WORKING RIGHT...")

        if info == None:
            raise Exception(f"ERROR: could not configure a bitcoin node helper - see the debug log")
        # {
        #   "chain": "main",
        #   "blocks": 656393,
        #   "headers": 754962,
        #   "bestblockhash": "00000000000000000000d56e0b0939335d59f9b99a66427e70dbea84fc27b2a7",
        #   "difficulty": 16787779609932.66,
        #   "time": 1605071585,
        #   "mediantime": 1605065123,
        #   "verificationprogress": 0.7656264483412351,
        #   "initialblockdownload": true,
        #   "chainwork": "0000000000000000000000000000000000000000159fcf781510f816684ddada",
        #   "size_on_disk": 40357429141,
        #   "pruned": true,
        #   "pruneheight": 627779,
        #   "automatic_pruning": true,
        #   "prune_target_size": 41943040000,
        #   "warnings": ""
        # }

        if info['initialblockdownload'] == True:
            progress = float( info['verificationprogress'] )
            logging.error(f"ERROR: your node is currently downloading the blockchain, it is not fully synced yet ({float(progress * 100):.0f}% downloaded)")

            # TODO - make sure this ugly exception is caught in the application... we don't want to fuck with that shit in real life... tracebacks and shit
            #raise Exception("This node is in Initial Block Download - you have to wait for it to fully synchronize before you can use it")

        #self.best_block_height = info['blocks']
        self.blockchain_state.block_height = info['blocks']
        if info['pruned']:
            self.pruned_height = info['pruneheight']
        else:
            self.pruned_height = 0
        self.blockchain_state.latest_block_hash = info['bestblockhash']
        self.blockchain_state.difficulty = info['difficulty']

        logging.debug("This bitcoin node...")
        #logging.info(f"getblockchaininfo: {node_info}")
        #logging.info(f"Node in Initial Block Download? {ibd}")
        logging.debug(f"...is on {info['chain']}net")
        # TODO - improve wording
        logging.debug(f"...has {self.blockchain_state.block_height} blocks")
        logging.debug(f"...has blocks back to block: {self.pruned_height}")
        #logging.info(f"Node is pruned to block: {config.pruned_height}")
        #logging.debug(f"...is pruned? {self.is_pruned}")
        logging.debug(f"...latest difficulty: {self.blockchain_state.difficulty}")
    
        logging.info(f"This node appears up-to-date - we can use it!")




    ############################################################
    def _format_RPC_call(self, method: str, params: list=None) -> str:
        logging.debug(f"_format_RPC_call({method=}, {params=})")

        if self.username == None:
            # todo - is there seriously no way to use curl with bitcoin without a user name?  I tried it and apparently yes, but honestly!!??
            raise NotImplementedError("NO USERNAME PROVIDED... CAN'T FUNCTION")

        # note: I don't think that I can run this without --user... curl just acts dumb and doesn't return anything... WTF

        user_string = self.username + ':' + self.password

        data_binary = {}
        data_binary['jsonrpc'] = '1.0'
        data_binary['id'] = 'btccalcs'
        data_binary['method'] = f"{method}"
        if params != None:
            data_binary['params'] = params
        
        # if params == None:
        #     cmd = "curl -s --user {} -X POST http://{} --data-binary '{{\"jsonrpc\":\"1.0\",\"id\":\"miningcalcs<3\",\"method\":\"{}\"}}' -H 'Content-Type: application/json'".format(config.RPC_user_pass, config.RPC_ip_port, command, params)
        # else:
        #     if type(params) == str:
        #         cmd = "curl -s --user {} -X POST http://{} --data-binary '{{\"jsonrpc\":\"1.0\",\"id\":\"miningcalcs<3\",\"method\":\"{}\", \"params\": [ \"'{}'\" ]}}' -H 'Content-Type: application/json'".format(config.RPC_user_pass, config.RPC_ip_port, command, params)
        #     else:
        #         cmd = "curl -s --user {} -X POST http://{} --data-binary '{{\"jsonrpc\":\"1.0\",\"id\":\"miningcalcs<3\",\"method\":\"{}\", \"params\": [ '{}' ]}}' -H 'Content-Type: application/json'".format(config.RPC_user_pass, config.RPC_ip_port, command, params)

        everything = "curl -s --user " + user_string + " --data-binary " + f"'{json.dumps(data_binary)}'" + " -H 'content-type: text/plain;' " + f"http://{self.ip_address}:{self.port}/"
        logging.debug(f"_format_RPC_call() returning: \n{everything}")
        return everything



    ##############################################################
    def _format_SHELL_call(self, method: str, params=None) -> str:
        raise NotImplementedError("ONE DAY I WILL WRITE THIS AND IT WILL BE AWESOME")
        # TODO add "2> /dev/null"
        #node_info = json.loads( os.popen(cmd).read() )['result']
        # for reference:
        # bitcoin-cli getblockstats 1000 '["minfeerate","avgfeerate"]'
        # bitcoin-cli getblockstats '"00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"' '["minfeerate","avgfeerate"]'



    ###########################################################
    #@cache TODO - use this?
    # TODO - you need to run this in a try: except block... your node may not like what you give it...
    def run(self, method: str, params=None):
        """ NOTE: THIS FUNCTION RETURNS A JSON OBJECT

            when you run bitcoin-cli getblockchaininfo, for example, it will return a some 'clean' JSON, BUT...
                when you run a curl command it will return that same JSON but under a top level 'result' and...
                    also includes top level 'error', and 'id' fields
            
                    This function returns whatever is included in that 'result' field.  So, it may be a string, integer, dictionary, etc...
            
            This function should NOT raise an exception... but will return None on error - so make sure you sanitize the result

            TODO - I'm actually not sure if this is the same with a shell command... actuallly it can't be... it will run just like how clean bitcoina-cli does it.
        """
        logging.debug(f"BitcoinNodeHelper.run({method=}, {params=})")

        #if self.RPC_enabled == True:
        cmd = self._format_RPC_call(method=method, params=params)
        # else:
        #     cmd = self._format_SHELL_call(method=method, params=params)
            # TODO - THIS IS HOW THE ERROR LOOKS LIKE FROM THE COMMAND LINE
            # as in - it's not wrapped in JSON, so grep 'error message:\n'
            # bitcoin-cli getblockchaininfoj
            # error code: -32601
            # error message:
            # Method not found

        logging.info(f"Running this on command line:\n{cmd}")
        ret = os.popen(cmd).read()
        logging.info(f"echo'd back:\n{ret}")

        #try:
        jres = json.loads( ret )

        # TODO - below is only how you catch errors for a `curl`... not for `bitcoin-cli`... FIX THIS
        if jres['error'] != None:
            raise Exception(jres['error']['message'])

        jres = jres['result'] # this may trigger a "json.decoder.JSONDecodeError" Exception!

        logging.debug(f".run() returning: {jres} {type(jres)}")
        return jres


    def get_block_time(self, height: int = None):
        """ calling this with no height returns block time of latest block
            
            https://developer.bitcoin.org/reference/rpc/getblockstats.html
        """
        if height == None:
            return self.get_block_time
        
        ret = self.run(method='getblockstats', params=[height])

        try:
            return int(ret['time'])
        # except Exception as e:
        #     logging.exception(e, exc_info=True)
        except json.decoder.JSONDecodeError:
            # this will fail if the node is unable to return the block time (eg. pruned node)
            logging.debug("json decode error - are you running a pruned node?")
            return None
    
    def average_block_fee():
        raise NotImplementedError("Why can't I find this old function...???")


######################################################################
if __name__== "__main__":
    logging.basicConfig( level=logging.DEBUG, format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s", handlers=[logging.StreamHandler()])

    u = input("what is your bitcoin node's username: ")
    p = input("what is your bitcoin node's password: ")

    bn = BitcoinNodeHelper(username=u, password=p, ip_address='127.0.0.1', port='8332')

    # EXAMPLES:
    # bn.run('getblockcount')
    # bn.run('getblockheader', params=["00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"])
    # bn.run('getblockstats', params=[660_202, ['time']])
    # bn.run('getblockstats', params=[660_000, ["minfeerate","avgfeerate"]])

    # https://developer.bitcoin.org/reference/rpc/getnetworkhashps.html
    # bn.run('getnetworkhashps', params=[5, 660_000])
    # bn.run('getnetworkhashps', params=[-1, 660_000]) # since last difficulty change
    bn.run('getnetworkhashps', params=[])

    # WARNING - this will cause an error
    #   getblockstats take a "hash" or a height.  If given string it will expect a hash of len 64 - else if int it expects a height
    # bn.run('getblockstats', params=["650000", ["minfeerate","avgfeerate"]])

# TODO - now write tests!!! ;)
# <3 <3
