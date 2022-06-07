from bson import ObjectId
from app.src.database import DB


class Reward(object):
    def __init__(self, name, detail, amount, price, image):
        self.name = name
        self.detail = detail
        self.amount = amount
        self.price = price
        self.image = image

    @staticmethod
    def getAllRewards():
        cursor = DB.DATABASE['reward'].find()
        rewardList = list(cursor)
        return rewardList

    @staticmethod
    def getRewardsPagination(page, perPage):
        cursor = DB.DATABASE['reward'].find().skip(perPage * (page - 1)).limit(perPage)
        rewardList = list(cursor)
        return rewardList

    @staticmethod
    def getRewardByID(id):
        cursor = DB.DATABASE['reward'].find({"_id": id})
        reward = list(cursor)
        return reward

    def addReward(self):
        id = ObjectId().__str__()
        DB.insert(collection='reward', data={
            '_id': id,
            'name': self.name,
            'detail': self.detail,
            'amount': self.amount,
            'price': self.price,
            'image': self.image
        })
        return self.getRewardByID(id)

    @staticmethod
    def deleteReward(id):
        DB.delete(collection='reward', data=id)

    @staticmethod
    def updateReward(id, Form_RewardName, Form_Detail, Form_Amount, Form_Price, Form_Image):
        DB.update(collection='reward', id=id, data={"_id": id,
                                                    'name': Form_RewardName,
                                                    'detail': Form_Detail,
                                                    'amount': Form_Amount,
                                                    'price': Form_Price,
                                                    'image': Form_Image})
        return Reward.getRewardByID(id)
