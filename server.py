from bottle import Bottle, request #, static_file
from login import SetupClient

entrade_client, dnse_client = SetupClient() # Can use SetUpClient(False) to only login Entrade
app = Bottle()

@app.get("/trade") # http://localhost:8000/trade?side=NB&symbol=41I1F8000&price=1621.3&account=1000064040&platform=Entrade&demo=f
def DatLenh():
    symbol = request.query.symbol # Query return '' if not found: "https://bottlepy.org/docs/0.13/tutorial.html"
    account = request.query.account

    if not (symbol and account):
        return "Missing query: symbol or account!"

    side = request.query.side or "NB"
    loan = request.query.loan
    volume = request.query.volume or 1
    order_type = request.query.type or "LO"
    platform = request.query.platform or "Entrade" # or "DNSE"

    price = ""
    if order_type == "LO":
        price = request.query.price
        if not price:
            return "Missing query: price!"

    if platform == "DNSE":
        return dnse_client.DatLenh(symbol, account, side, price, loan, volume, order_type)
    else:
        demo = True if request.query.demo else False
        return entrade_client.DatLenh(symbol, account, side, price, loan, volume, order_type, demo)

@app.get("/conditional_order")
def DatLenhDieuKien():
    symbol = request.query.symbol
    account = request.query.account
    sub_acc = request.query.sub_acc
    price = request.query.price
    stop = request.query.stop

    if not (symbol and account and price and stop and sub_acc):
        return "Missing query: symbol, account, price, sub_acc or stop!"

    side = request.query.side or "NB"
    loan = request.query.loan
    volume = request.query.volume or 1
    condition = request.query.condition or "<="
    platform = request.query.platform or "Entrade"

    if platform == "DNSE":
        order_type = request.query.type or "LO"
        return dnse_client.DatLenhDieuKien(symbol, account, side, price, loan, volume, order_type, f"price {condition} {stop}")
    else:
        demo = True if request.query.demo else False
        return entrade_client.DatLenhDieuKien(symbol, int(account), int(sub_acc), side, float(price), loan, volume, f"price {condition} {stop}", demo)

@app.get("/cancel_conditional_order") # http://localhost:7979/cancel_conditional_order?id=12121 (remove 'id' to cancel all orders)
def HuyLenhDieuKien():
    account = request.query.account
    sub_acc = request.query.sub_acc

    if not (account and sub_acc):
        return "Missing query: account or sub_acc!"

    id = request.query.id
    demo = True if request.query.demo else False
    return entrade_client.HuyLenhDieuKien(account, sub_acc, id, id == '', demo)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, reloader=True)