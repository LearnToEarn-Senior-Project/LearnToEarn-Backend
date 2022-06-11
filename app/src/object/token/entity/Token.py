class Token(object):
    __slots__ = "amount"

    def __init__(self, amount):
        self.amount: float = amount
