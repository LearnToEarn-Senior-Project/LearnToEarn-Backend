from bson import ObjectId
from flask import request, Blueprint

from app.src.database import DB
from app.src.entity.reward.reward import Reward
from app.src.entity.assignment.assignment import Assignment
from app.src.entity.user.googleUser import GoogleUser

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
    @route.route('/reward/<reward_id>', methods=["GET"])
    def getRewardByID(reward_id):
        return Reward.getRewardByID(reward_id)

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

    @staticmethod
    @route.route('/deleteReward/<reward_id>', methods=["DELETE"])
    def adminDeleteReward(reward_id):
        Reward.deleteReward(reward_id)
        return 'Success'

    @staticmethod
    @route.route('/google_login', methods=["POST"])
    def googleLogin():
        googleUser = GoogleUser(access_token=request.json['access_token'], firstname=request.json['firstname'],
                                lastname=request.json['lastname'],
                                email=request.json['email'],
                                image_url=request.json['image_url'])
        googleUser.addGoogleUser()
        return 'Success'

    @staticmethod
    @route.route('/google_get_by_id', methods=["GET"])
    def googleGetById():
        return GoogleUser.getGoogleUserById("123")

    @staticmethod
    @route.route('/assignments', methods=["GET"])
    def getAllAssignments():
        return Assignment.getAllAssignments()
