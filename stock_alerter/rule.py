class PriceRule:
    """PriceRule is a rul that triggers when a stock pices
    satisfies a condition (isually greater, equal or lesser
    than a given value)
    """

    def __init__(self, symbol, condition):
        self.symbol = symbol
        self.condition = condition

    def matches(self, exchange):
        try:
            stock = exchange[self.symbol]
        except KeyError:
            return False
        return self.condition(stock) if stock.price else False

    def depends_on(self):
        return {self.symbol}


class AndRule:
    
    def __init__(self, *args):
        self.rules = args

    def matches(self, exchange):
        return all([rule.matches(exchange) for rule in self.rules])
