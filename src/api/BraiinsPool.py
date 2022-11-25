import os
import json
import logging

import requests

"""
    TODO - document that dotenv.load_env() needs to be called if no credentials will be given during init()
"""

BRAIINS_TOKEN_ENV = 'BRAIINS_TOKEN'

class BraiinsPoolUser:
    # these are the names of the environment variables that BraiinsAPIHelper
    # will look for during initialization if they are not supplied
    api_token = None
    #pool_username = None # TODO can we just get this from the pool?  Yeah, let's try that...

    def __init__(self, api_token: str = None):
        if api_token == None:
            api_token = os.getenv(BRAIINS_TOKEN_ENV)
            if api_token == None:
                raise Exception(f"{BRAIINS_TOKEN_ENV} environment variable not privded and not found in '.env'")
        self.api_token = api_token


def query_worker_metric(braiins_user: BraiinsPoolUser, poolname_workername: str, metric: str):
    # run the curl command
    # ret = os.popen(f"curl -s 'https://pool.braiins.com/accounts/workers/json/btc/' -H \"SlushPool-Auth-Token: {braiins_user.api_token}\"").read()
    r = requests.get(f"https://pool.braiins.com/accounts/workers/json/btc/", headers={"SlushPool-Auth-Token": braiins_user.api_token})

    logging.debug(f"{r.status_code=}")
    if r.status_code != 200:
        raise Exception(f"query_worker_metric() failed with status code {r.status_code}")

    # make it a JSON object
    ret = json.loads(r.content)
    logging.debug(ret)

    try:
        # TODO - this will cause a bug if the user tries to get any metric besides the hashrate... shit
        ans = ret['btc']['workers'][poolname_workername][metric]
        #if ret['hash_rate_unit'] == 'Gh/s':
        #    ans /= 1000
        ans /= 1000
        logging.debug(f"query_workers: return {ans=}")
        return ans
    except KeyError:
        logging.exception("WORKER NAME ERROR?")
        return None



def list_workers_and_metric(metric: str, user: BraiinsPoolUser = None) -> list[dict]:
    if user == None:
        user = BraiinsPoolUser()
    
    # run the curl command
    ret = os.popen(f"curl -s 'https://pool.braiins.com/accounts/workers/json/btc/' -H \"SlushPool-Auth-Token: {user.api_token}\"").read()

    # make it a JSON object
    ret = json.loads(ret)
    logging.debug(ret)

    # for each_worker in ret['btc']['workers']:
    #     worker_name = each_worker[]

    #     try:
    #         metric_value = each_worker[metric]
    #     except:
    #         logging.exception("NO METRIC BY THAT NAME?")

    # HOLY SHIT DON'T ASK ME HOW I KNEW HOW TO DO THIS... HOW IS THE PYTHONIC WAY SUPPOSED TO BE EASIER?
    # THIS LOOKS LIKE RANDOM CHARACHTERSZ.AZZZZ............... UGH
    #w = [z for z in ret['btc']['workers'].keys()]
    w = list( ret['btc']['workers'].keys() )
    #print(f"{w=}")

    # we don't want to round... do we?  No, not for every/any given metric..
    #m = [ round(ret['btc']['workers'][i][metric], 1) for m, i in enumerate(w)]
    m = [ ret['btc']['workers'][i][metric] for m, i in enumerate(w)]
    #print(f"{m=}")

    ## TODO - there must be a better way.. this will cause a bug if not every unit is reported with the same unit
    # if ret['btc']['workers'][0]['hash_rate_unit'] == 'Gh/s':
    #     m = [m / 1000 for m in m]
    m = [m / 1000 for m in m]

    #ans = [r for r in (w,m)]
    ans = list( [(n, m[i]) for i, n in enumerate(w) ] )

    logging.debug(f"list_workers_and_metric() returning: {ans=}")
    return ans




if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    print( os.getenv( BraiinsPoolUser.BRAIINS_TOKEN_ENV ) )

    user = BraiinsPoolUser()
    print(user.api_token)

    user = BraiinsPoolUser(api_token="TOKENZZZZSCHWEE")
    print(user.api_token)
