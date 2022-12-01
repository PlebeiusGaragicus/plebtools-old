import logging
import json

from pywebio import output

from src.api.authproxy import AuthServiceProxy, JSONRPCException
from src.settings import AppSettings

def return_AuthProxy() -> AuthServiceProxy:
    appsettings = AppSettings()
    user = appsettings['RPC_USER']
    pswd = appsettings['RPC_PASS']
    host = appsettings['RPC_HOST']
    port = appsettings['RPC_PORT']

    rpc_url = f"http://{user}:{pswd}@{host}:{port}"
    logging.debug(f"{rpc_url=}")

    ap = AuthServiceProxy(rpc_url)

    try:
        # i = json.loads( ap.getblockchaininfo() )
        i = ap.getblockchaininfo()

        output.toast(f"Node connected - working on {i['chain']} chain")
    except JSONRPCException as e:
        #assume this is a JSON decode error... TODO WHERE IS COPILOT when i need it??!
        logging.error(f"Error connecting to node: {e}")
        # output.toast(f"{e=}", color='error')
        output.toast("ERROR: Cannot connect to node!", color='error', duration=4)
        return None

    return ap
