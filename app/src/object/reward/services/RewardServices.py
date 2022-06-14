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
    def getByID(reward_id):
        return list(DB.DATABASE['reward'].find({"_id": reward_id}).limit(1))

    @staticmethod
    def add(name, detail, amount, price, image_url):
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
    def delete(reward_id):
        DB.delete(collection='reward', data=reward_id)
        return "Delete reward successfully!!"

    @staticmethod
    def update(reward_id, name, detail, amount, price, image_url):
        reward = Reward(name, detail, amount, price, image_url)
        DB.update(collection='reward', id=reward_id, data={
            'name': reward.name,
            'detail': reward.detail,
            'amount': reward.amount,
            'price': reward.price,
            'image': reward.image_url})
        return RewardServices.getByID(reward_id)
