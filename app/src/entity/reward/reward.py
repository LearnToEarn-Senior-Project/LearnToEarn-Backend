from json import dumps

from bson import ObjectId

from app.src.database import DB


class Reward(object):
    def __init__(self, reward_name, detail, amount, price, image):
        self.reward_name = reward_name
        self.detail = detail
        self.amount = amount
        self.price = price
        self.image = image

    def addJson(self):
        return {
            '_id': ObjectId().__str__(),
            'reward_name': self.reward_name,
            'detail': self.detail,
            'amount': self.amount,
            'price': self.price,
            'image': self.image
        }

    @staticmethod
    def getAllRewards():
        cursor = DB.DATABASE['reward'].find()
        rewardList = list(cursor)
        json_data = dumps(rewardList, indent=2)
        return json_data

    def addReward(self):
        DB.insert(collection='reward', data=self.addJson())
