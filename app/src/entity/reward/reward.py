from json import dumps
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
        json_data = dumps(rewardList, indent=2)
        return json_data

    @staticmethod
    def getRewardByID(id):
        cursor = DB.DATABASE['reward'].find({"_id": id})
        rewardList = list(cursor)
        json_data = dumps(rewardList, indent=2)
        return json_data

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
        return Reward.getRewardByID(id)

    @staticmethod
    def updateReward(id, Form_RewardName, Form_Detail, Form_Amount, Form_Price, Form_Image):
        value = {"reward_name": str(Form_RewardName)}
        DB.update(collection='reward', id=id, data=value)
        value = {"detail": str(Form_Detail)}
        DB.update(collection='reward', id=id, data=value)
        value = {"amount": str(Form_Amount)}
        DB.update(collection='reward', id=id, data=value)
        value = {"price": str(Form_Price)}
        DB.update(collection='reward', id=id, data=value)
        value = {"image": str(Form_Image)}
        DB.update(collection='reward', id=id, data=value)
