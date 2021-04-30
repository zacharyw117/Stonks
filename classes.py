import json


class Stonk:
    def __init__(self, ticker, shares, buy_price):
        self.ticker = ticker
        self.shares = shares
        self.buy_price = buy_price

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Profile:
    def __init__(self, name, tax_rate):
        self.name = name
        self.tax_rate = tax_rate
        self.stonks = []

    def add_stonk(self, stonk):
        self.stonks.append(stonk)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
