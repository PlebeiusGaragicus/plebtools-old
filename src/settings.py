import logging
import json

from pywebio import output, pin

SETTINGS_FILE = "settings.json"

settings_json = None

def save_settings():
    """Save settings to file"""
    global settings_json

    if settings_json == None:
        logging.error("Settings not loaded, not saving")
        output.toast("Settings not loaded, not saving", duration=5, color='error')
        return

    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings_json, f, indent=4)

    output.toast("Settings saved")


def default_settings():
    global settings_json

    settings_json = {
        # bitcoin core RPC authentication
        'RPC_USER': '',
        'RPC_PASS': '',
        'RPC_HOST': '127.0.0.1',
        'RPC_PORT': '8332',

        # Braiins Pool API
        'BRAIINS_TOKEN': '',

        # Adafruit IO
        'ADAFRUIT_USERNAME': "",
        'ADAFRUIT_APITOKEN': "",

        # Twilio
        'TWILIO_SID': "",
        'TWILIO_TOKEN' :"",
        'TWILIO_PHONE_NUMBER': "",
        # E164 format: [+] [country code] [subscriber number including area code]
        'NOTIFY_PHONE_NUMBER': "",
    }

def load_settings():
    """Load settings from file into global settings variable"""
    global settings_json

    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings_json = json.load(f)
            logging.debug(f"Settings loaded: {settings_json=}")
    except FileNotFoundError:
        logging.warning("No settings file found, creating a new blank one")
        default_settings()
        save_settings()
