from bson import ObjectId
from orjson import orjson
from starlette.responses import Response

from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices
from app.src.server.database import DB
from app.src.object.reward.entity.Reward import RewardDAO


class RewardServices:
    @staticmethod
    def getAllPagination(page, perPage):
        try:
            if page > 0:
                totalRewards = len(list(DB.DATABASE['reward'].find()))
                rewardList = list(DB.DATABASE['reward'].find().skip(perPage * (page - 1)).limit(perPage))
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
                return Response(content=orjson.dumps(reward_object))
        except:
            reward_object = {
                "total_classrooms": 0,
                "classroom_list": []
            }
            return reward_object

    @staticmethod
    def getByID(reward_id):
        return Response(content=orjson.dumps(list(DB.DATABASE['reward'].find({"_id": reward_id}).limit(1))))

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

    @staticmethod
    def redeem(reward_id, user_id):
        try:
            try:
                list(
                    DB.DATABASE["reward"].find({"_id": reward_id}, {"amount": True, "price": True, "_id": False}).limit(
                        1))[0]
            except:
                return "Reward not found"
            try:
                list(DB.DATABASE['user'].find({"_id": user_id}, {"current_token": True, "_id": False}))[0][
                    "current_token"]
            except:
                return "Student not found"
            reward = list(
                DB.DATABASE["reward"].find({"_id": reward_id}, {"amount": True, "price": True, "_id": False}).limit(1))[
                0]
            rewardAmount = reward["amount"]
            rewardPrice = reward["price"]
            tokenAmount = list(DB.DATABASE['token'].find({"_id": "1"}, {"amount": True, "_id": False}))[0]["amount"]
            userTokenAmount = \
                list(DB.DATABASE['user'].find({"_id": user_id}, {"current_token": True, "_id": False}))[0][
                    "current_token"]
            if userTokenAmount - rewardPrice < 0:
                return "Cannot redeem this reward"
            DB.upsert(collection="reward", id=reward_id, data={"amount": rewardAmount - 1})
            DB.upsert(collection="token", id="1", data={"amount": tokenAmount + rewardPrice})
            DB.upsert(collection="user", id=user_id, data={"current_token": userTokenAmount - rewardPrice})
            return TokenHistoryServices.add((-1 * rewardPrice), user_id, reward_id)
        except:
            return "Cannot redeem this reward"
