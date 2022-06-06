from flask import request, Blueprint

from app.src.entity.classroom.classroom import Classroom
from app.src.entity.reward.reward import Reward
from app.src.entity.criteria.criteria import Criteria

from app.src.entity.user.googleUser import GoogleUser
from app.src.entity.user.user import User

route = Blueprint('route', __name__)


class Routes:
    @staticmethod
    def getBlueprint():
        return route

# ========================= Reward session ============================
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
        reward = Reward(request.json['name'],
                        request.json['detail'],
                        request.json['amount'],
                        request.json['price'],
                        request.json['image'])
        return reward.addReward()

    @staticmethod
    @route.route('/deleteReward/<reward_id>', methods=["DELETE"])
    def adminDeleteReward(reward_id):
        Reward.deleteReward(reward_id)
        return 'Success'

    @staticmethod
    @route.route('/updateReward/<reward_id>', methods=["PATCH"])
    def adminUpdateReward(reward_id):
        Form_RewardName = request.form["reward_name"]
        Form_Detail = request.form["detail"]
        Form_Amount = request.form["amount"]
        Form_Price = request.form["price"]
        Form_Image = request.form["image"]
        Reward.updateReward(reward_id,Form_RewardName,Form_Detail,Form_Amount,Form_Price,Form_Image)
        return 'Success'

# ========================= Reward session ============================
# ========================= Google session ============================

    @staticmethod
    @route.route('/google_login', methods=["POST"])
    def getGoogleToken():
        return GoogleUser.bindGoogleAccount(request.json['id'], request.json['auth_code'])

    @staticmethod
    @route.route('/google_logout', methods=["POST"])
    def googleLogout():
        return GoogleUser.unbindGoogleAccount(request.json['id'])

    @staticmethod
    @route.route('/googleGetData/<string:id>', methods=["GET"])
    def googleGetData(id):
        return GoogleUser.getUserGoogleData(id)

# ========================= Google session ============================
# =========================== CMU session =============================
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
        return cmuUser.addUser()
# =========================== CMU session =============================
# =========================== Criteria session =============================

    @staticmethod
    @route.route('/criteria', methods=["GET"])
    def getAllCriteria():
        return Criteria.getAllCriterias()

# =========================== Criteria session =============================
