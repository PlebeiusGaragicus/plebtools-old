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

DEFAULT_NODE_IP_ADDRESS = '127.0.0.1'
DEFAULT_NODE_PORT = '8332'

SETTING_NAME_NODE_IP_ADDRESS = "NODE_IP_ADDRESS"
SETTING_NAME_NODE_PORT = "NODE_PORT"
SETTING_NAME_NODE_USERNAME = "NODE_USERNAME"
SETTING_NAME_NODE_PASSWORD = "NODE_PASSWORD"
SETTING_NAME_NODE_DATA_DIRECTORY = "NODE_DATA_DIRECTORY"



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


# ######################################################################
# if __name__== "__main__":
#     logging.basicConfig( level=logging.DEBUG, format="[%(levelname)s] (%(filename)s @ %(lineno)d) %(message)s", handlers=[logging.StreamHandler()])

#     u = input("what is your bitcoin node's username: ")
#     p = input("what is your bitcoin node's password: ")

#     bn = BitcoinNodeHelper(username=u, password=p, ip_address='127.0.0.1', port='8332')

#     # EXAMPLES:
#     # bn.run('getblockcount')
#     # bn.run('getblockheader', params=["00000000c937983704a73af28acdec37b049d214adbda81d7e2a3dd146f6ed09"])
#     # bn.run('getblockstats', params=[660_202, ['time']])
#     # bn.run('getblockstats', params=[660_000, ["minfeerate","avgfeerate"]])

#     # https://developer.bitcoin.org/reference/rpc/getnetworkhashps.html
#     # bn.run('getnetworkhashps', params=[5, 660_000])
#     # bn.run('getnetworkhashps', params=[-1, 660_000]) # since last difficulty change
#     bn.run('getnetworkhashps', params=[])

#     # WARNING - this will cause an error
#     #   getblockstats take a "hash" or a height.  If given string it will expect a hash of len 64 - else if int it expects a height
#     # bn.run('getblockstats', params=["650000", ["minfeerate","avgfeerate"]])

# # TODO - now write tests!!! ;)
# # <3 <3
