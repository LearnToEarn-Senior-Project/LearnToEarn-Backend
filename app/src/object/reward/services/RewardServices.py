from bson import ObjectId
from app.src.server.database import DB
from app.src.object.reward.entity.RewardDAO import RewardDAO


class RewardServices:
    @staticmethod
    def getAllPagination(page):
        try:
            if page > 0:
                totalRewards = len(list(DB.DATABASE['reward'].find()))
                rewardList = list(DB.DATABASE['reward'].find().skip(10 * (page - 1)).limit(10))
                reward_object = {
                    "total_rewards": totalRewards,
                    "reward_list": rewardList
                }
                return reward_object
            else:
                reward_object = {
                    "total_classrooms": 0,
                    "classroom_list": []
                }
                return reward_object
        except:
            reward_object = {
                "total_classrooms": 0,
                "classroom_list": []
            }
            return reward_object

    @staticmethod
    def getByID(reward_id):
        return list(DB.DATABASE['reward'].find({"_id": reward_id}).limit(1))

    @staticmethod
    def add(name, detail, amount, price, image_url):
        if (name and detail and amount and price is not None) and type(amount) is int and (amount >= 0 and price >= 0):
            reward = RewardDAO(name, detail, amount, price, image_url)
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
        else:
            return "The input is required or the type of data is not correct"

    @staticmethod
    def delete(reward_id):
        DB.delete(collection='reward', data=reward_id)
        if DB.delete(collection='reward', data=reward_id) is not None:
            return "Delete reward successfully!!"
        else:
            return "The reward ID is not available"

    @staticmethod
    def update(reward_id, name, detail, amount, price, image_url):
        if reward_id and name and detail and amount and price is not None and type(
                amount) is int and (amount >= 0 and price >= 0):
            reward = RewardDAO(name, detail, amount, price, image_url)
            DB.update(collection='reward', id=reward_id, data={
                'name': reward.name,
                'detail': reward.detail,
                'amount': reward.amount,
                'price': reward.price,
                'image': reward.image_url})
            return RewardServices.getByID(reward_id)
        else:
            return "The input is required or the type of data is not correct"
