import os
import json
import time
import logging

from src.api.authproxy import AuthServiceProxy

from src import tool_settings

def respond_to_client():
    # latest_hash = 
    while True:

        _data = json.dumps({"height":counter})
        yield f"id: 1\ndata: {_data}\nevent: online\n\n"
        time.sleep(1.0)
