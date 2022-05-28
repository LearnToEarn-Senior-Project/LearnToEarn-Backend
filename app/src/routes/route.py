from flask import request, Blueprint
from app.src.entity.classroom.classroom import Classroom
from app.src.entity.reward.reward import Reward
from app.src.entity.user.googleUser import GoogleUser
from app.src.entity.user.user import User

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
        reward = Reward(request.json['reward_name'],
                        request.json['detail'],
                        request.json['amount'],
                        request.json['price'],
                        request.json['image'])
        reward.addReward()
        return "Success"

    @staticmethod
    @route.route('/google_login', methods=["POST"])
    def getGoogleToken():
        GoogleUser.bindGoogleAccount(request.json['id'], request.json['auth_code'])
        return "success"

    # @route.route('/deleteReward/<reward_id>', methods=["DELETE"])
    # def adminDeleteReward(reward_id):
    #     Reward.deleteReward(reward_id)
    #     return 'Success'

    @staticmethod
    @route.route('/google_logout', methods=["POST"])
    def googleLogout():
        GoogleUser.unbindGoogleAccount(request.json['id'])
        return "success"

    @staticmethod
    @route.route('/googleGetData/<string:id>', methods=["GET"])
    def googleGetData(id):
        return GoogleUser.getUserGoogleData(id)

    @staticmethod
    @route.route('/getGoogleClassrooms/<string:id>', methods=["GET", "POST"])
    def getAllGoogleClassrooms(id):
        return Classroom.getAllGoogleClassrooms(id)

    @staticmethod
    @route.route('/login', methods=["POST"])
    def CMUOAuthLogin():
        return User.getAccessToken(request.json['code'])

    @staticmethod
    @route.route('/credentials/<string:token>', methods=["GET"])
    def CMUOAuthGetUserData(token):
        return User.getCredentials(token)

    @staticmethod
    @route.route('/getUser/<string:id>', methods=["GET"])
    def CMUOAuthGetUserByID(id):
        return User.getUser(id)

    @staticmethod
    @route.route('/addUser', methods=["POST"])
    def CMUOAuthSaveUser():
        cmuUser = User(request.json['id'],
                       request.json['firstname'],
                       request.json['lastname'],
                       request.json['email'],
                       None,
                       request.json['role'])
        cmuUser.addUser()
        return "success"
