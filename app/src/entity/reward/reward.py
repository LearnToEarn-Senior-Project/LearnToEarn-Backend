import io

from bson import ObjectId
from app.src.database import DB
from firebase_admin import credentials, initialize_app, storage, get_app


class Reward(object):
    def __init__(self, name, detail, amount, price, image):
        self.name = name
        self.detail = detail
        self.amount = amount
        self.price = price
        self.image = image

    @staticmethod
    def getAllRewards():
        rewardList = list(DB.DATABASE['reward'].find())
        return rewardList

    @staticmethod
    def getRewardsPagination(page, perPage):
        totalRewards = len(list(DB.DATABASE['reward'].find()))
        rewardList = list(DB.DATABASE['reward'].find().skip(perPage * (page - 1)).limit(perPage))
        reward_object = {
            "total_rewards": totalRewards,
            "reward_list": rewardList
        }
        return reward_object

    @staticmethod
    def getRewardByID(id):
        reward = list(DB.DATABASE['reward'].find({"_id": id}).limit(1))
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
        return "self.getRewardByID(id)"

    @staticmethod
    def deleteReward(id):
        DB.delete(collection='reward', data=id)

    @staticmethod
    def updateReward(id, Form_RewardName, Form_Detail, Form_Amount, Form_Price, Form_Image):
        DB.update(collection='reward', id=id, data={
            'name': Form_RewardName,
            'detail': Form_Detail,
            'amount': Form_Amount,
            'price': Form_Price,
            'image': Form_Image})
        return Reward.getRewardByID(id)

    @staticmethod
    def getImgPath(image, content):
        byte = io.BytesIO(content)
        cred = credentials.Certificate("../app/src/credentials/learntoearn-cred.json")
        try:
            initialize_app(cred, {'storageBucket': 'learntoearn-350914.appspot.com'})
        except:
            get_app()
        bucket = storage.bucket()
        blob = bucket.blob(image)
        blob.upload_from_string(byte.read(), content_type='image/png')
        blob.make_public()
        return blob.public_url
