from bson import ObjectId
from app.src.server.database import DB
from app.src.object.reward.entity.Reward import Reward


class RewardServices:
    @staticmethod
    def getAllPagination(page, perPage):
        if page is None or page < 1:
            page = 1
        totalRewards = len(list(DB.DATABASE['reward'].find()))
        rewardList = list(DB.DATABASE['reward'].find().skip(perPage * (page - 1)).limit(perPage))
        reward_object = {
            "total_rewards": totalRewards,
            "reward_list": rewardList
        }
        return reward_object

    @staticmethod
    def getByID(id):
        reward = list(DB.DATABASE['reward'].find({"_id": id}).limit(1))
        return reward

    @staticmethod
    def add(name, detail, amount, price, image_url):
        try:
            image_url = image_url
        except:
            image_url = None
        reward = Reward(name, detail, amount, price, image_url)
        id = ObjectId().__str__()
        DB.insert(collection='reward', data={
            '_id': id,
            'name': reward.name,
            'detail': reward.detail,
            'amount': reward.amount,
            'price': reward.price,
            'image': reward.image_url
        })
        return RewardServices.getByID(id)

    @staticmethod
    def delete(id):
        DB.delete(collection='reward', data=id)
        return "Delete reward successfully!!"

    @staticmethod
    def update(id, name, detail, amount, price, image_url):
        try:
            image_url = image_url
        except:
            image_url = list(DB.DATABASE['reward'].find({"_id": id}).limit(1))[0]["image"]
        reward = Reward(name, detail, amount, price, image_url)
        DB.update(collection='reward', id=id, data={
            'name': reward.name,
            'detail': reward.detail,
            'amount': reward.amount,
            'price': reward.price,
            'image': reward.image_url})
        return RewardServices.getByID(id)
