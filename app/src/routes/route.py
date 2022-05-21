from flask import request, Blueprint, jsonify
from app.src.entity.reward.reward import Reward

route = Blueprint('route', __name__)


class Routes:
    @staticmethod
    def getBlueprint():
        return route

    @staticmethod
    @route.route('/rewards', methods=["GET"])
    def getAllReward():
        return Reward.getAllRewards()

    @staticmethod
    @route.route('/addReward', methods=["POST"])
    def adminAddReward():
        reward = Reward(reward_name=request.json['reward_name'],
                        detail=request.json['detail'],
                        amount=request.json['amount'],
                        price=request.json['price'],
                        image=request.json['image'])
        reward.addReward()
        return 'Success'
