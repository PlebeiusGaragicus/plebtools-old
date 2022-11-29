APP_TITLE = "PlebTool Settings"

SETTINGS_FILE = "settings.json"
settings = None
default_settings = {
    # bitcoind authentication
    # bitcoin core rpc settings
    'RPC_USER': '',
    'RPC_PASS': '',
    'RPC_HOST': '127.0.0.1',
    'RPC_PORT': '8332',

    # braiins pool api
    'BRAIINS_TOKEN': '',

    # # ADAFRUIT
    'ADAFRUIT_USERNAME': "",
    'ADAFRUIT_APITOKEN': "",

    # TWILIO
    'TWILIO_SID': "",
    'TWILIO_TOKEN' :"",
    'TWILIO_PHONE_NUMBER': "",
    'NOTIFY_PHONE_NUMBER': "",
}

    # # E164 format: [+] [country code] [subscriber number including area code]
    # 'NOTIFY_NUMBER': ""