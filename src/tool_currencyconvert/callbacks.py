from pywebio import pin, output, session

from src.api.coinbase import spot_price
from src.constants import ONE_HUNDRED_MILLION

def currency_converter():
    def updateprice():
        try:
            pin.pin['price'] = spot_price()
        except Exception as e:
            output.toast("Unable to get coinbase spot price data - internet down?", color='error')

    def convert_to_sat():
        amnt = float(pin.pin["amount"])
        price = float(pin.pin["price"])

        r = float(ONE_HUNDRED_MILLION * (amnt / price))

        output.put_text(f"[{amnt:,.2f} fiat @ price:{price:,.2f}] = {r:,.2f} satoshi")

    def convert_to_fiat():
        amnt = float(pin.pin["amount"])
        price = float(pin.pin["price"])
        r = amnt * (price / ONE_HUNDRED_MILLION)
        output.put_text(f"[{amnt:,.2f} satoshi @ price:{price:,.2f}] = {r:,.2f} fiat")

    output.put_row(content=[
        output.put_column(content=[
            pin.put_input("price", type="float", label="Bitcoin price:", value=0),
            output.put_button("refresh price", onclick=updateprice)
            ]),
        output.put_column(content=[
            pin.put_input("amount", type="float", label="Amount to convert"),
            output.put_column(content=[
                output.put_button("sats -> fiat", onclick=convert_to_fiat),
                output.put_button("fiat -> sats", onclick=convert_to_sat)
                ])
            ])
    ])

    session.hold()
