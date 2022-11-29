import logging
import json

import pywebio
from pywebio import output, pin

from src import settings

APP_TITLE = "PlebTool Settings"

def update_inputs():
    pin.pin_update(name='RPC_USER', value=settings.settings_json['RPC_USER'])
    pin.pin_update(name='RPC_PASS', value=settings.settings_json['RPC_PASS'])
    pin.pin_update(name='RPC_HOST', value=settings.settings_json['RPC_HOST'])
    pin.pin_update(name='RPC_PORT', value=settings.settings_json['RPC_PORT'])
    pin.pin_update(name='BRAIINS_TOKEN', value=settings.settings_json['BRAIINS_TOKEN'])
    pin.pin_update(name='TWILIO_SID', value=settings.settings_json['TWILIO_SID'])
    pin.pin_update(name='TWILIO_TOKEN', value=settings.settings_json['TWILIO_TOKEN'])
    pin.pin_update(name='TWILIO_PHONE_NUMBER', value=settings.settings_json['TWILIO_PHONE_NUMBER'])
    pin.pin_update(name='NOTIFY_PHONE_NUMBER', value=settings.settings_json['NOTIFY_PHONE_NUMBER'])
    pin.pin_update(name='ADAFRUIT_USERNAME', value=settings.settings_json['ADAFRUIT_USERNAME'])
    pin.pin_update(name='ADAFRUIT_APITOKEN', value=settings.settings_json['ADAFRUIT_APITOKEN'])


def save_inputs():
    settings.settings_json['RPC_USER'] = pin.pin['RPC_USER']
    settings.settings_json['RPC_PASS'] = pin.pin['RPC_PASS']
    settings.settings_json['RPC_HOST'] = pin.pin['RPC_HOST']
    settings.settings_json['RPC_PORT'] = pin.pin['RPC_PORT']

    settings.settings_json['BRAIINS_TOKEN'] = pin.pin['BRAIINS_TOKEN']

    settings.settings_json['TWILIO_SID'] = pin.pin['TWILIO_SID']
    settings.settings_json['TWILIO_TOKEN'] = pin.pin['TWILIO_TOKEN']
    settings.settings_json['TWILIO_PHONE_NUMBER'] = pin.pin['TWILIO_PHONE_NUMBER']
    settings.settings_json['NOTIFY_PHONE_NUMBER'] = pin.pin['NOTIFY_PHONE_NUMBER']

    settings.settings_json['ADAFRUIT_USERNAME'] = pin.pin['ADAFRUIT_USERNAME']
    settings.settings_json['ADAFRUIT_APITOKEN'] = pin.pin['ADAFRUIT_APITOKEN']

    settings.save_settings()


@pywebio.config(title=APP_TITLE, theme='dark')
def main():
    with output.use_scope('main', clear=True):
        output.put_markdown(f"# {APP_TITLE}")

        output.put_table(tdata=[[
            output.span([
                output.put_markdown("## Bitcoin Core RPC Settings"),
                output.put_text("This allows PlebTools to access a node and pull blockchain data.  This is more text and I want to see how it wraps etc, etc, etc....  Fill this out completely so that it can span and span and span...!!! <3 <3")
            ], col=4)
        ],[
            output.span(pin.put_input('RPC_USER', type='text', label="username"), col=2),
            output.span(pin.put_input('RPC_PASS', type='text', label="password"), col=2),
        ],[
            output.span(pin.put_input('RPC_HOST', type='text', label="ip address"), col=2),
            output.span(pin.put_input('RPC_PORT', type='text', label="port"), col=2),
        ],[
            output.span([
                output.put_markdown("## Braiins Pool Token"),
                output.put_text("Get this from the Braiins pool web interface.")
            ], col=4)
        ],[
            output.span(
                pin.put_input('BRAIINS_TOKEN', type='text', label="Braiins Pool Token")
            , col=4)
        ],[
            output.span([
                output.put_markdown("## Twilio Settings"),
                output.put_text("This allows PlebTools to send SMS messages to your phone.")
            ], col=4)
        ],[
            output.span(pin.put_input('TWILIO_SID', type='text', label="Twilio SID"), col=2),
            output.span(pin.put_input('TWILIO_TOKEN', type='text', label="Twilio Token"), col=2)
        ],[
            output.span(pin.put_input('TWILIO_PHONE_NUMBER', type='text', label="Twilio Phone Number"), col=2),
            output.span(pin.put_input('NOTIFY_PHONE_NUMBER', type='text', label="Notification Phone Number", help_text="This is the number that will be notified."), col=2)
        ],[
            output.span([
                output.put_markdown("## Adafruit IO Settings"),
                output.put_text("This allows PlebTools to send data to your Adafruit IO account.")
            ], col=4)
        ],[
            output.span(pin.put_input('ADAFRUIT_USERNAME', type='text', label="Adafruit IO Username"), col=2),
            output.span(pin.put_input('ADAFRUIT_APITOKEN', type='text', label="Adafruit IO Key"), col=4)
        ]])

        output.put_button('Save', onclick=save_inputs, color="success")

    settings.load_settings()
    update_inputs()
