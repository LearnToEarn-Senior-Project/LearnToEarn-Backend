class TokenDAO(object):
    __slots__ = "amountOfCoin"

    def __init__(self, amountOfCoin):
        self.amountOfCoin: float = amountOfCoin
