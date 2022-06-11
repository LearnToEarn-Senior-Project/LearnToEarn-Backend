class Reward(object):
    __slots__ = "name", "detail", "amount", "price", "image_url"

    def __init__(self, name, detail, amount, price, image_url):
        self.name = name
        self.detail = detail
        self.amount = amount
        self.price = price
        self.image_url = image_url
