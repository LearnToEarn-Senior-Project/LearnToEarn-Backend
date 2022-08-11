from bson import ObjectId
from orjson import orjson
from datetime import datetime
from starlette.responses import Response
from app.src.object.tokenHistory.entity.TokenHistoryDAO import TokenHistoryDAO
from app.src.server.database import DB


class TokenHistoryServices:

    @staticmethod
    def getAllPagination(user_id, page, checked):
        try:
            perPage = 10
            if checked is True:
                json = {"student_id": user_id}
                tokenHistoriesList = list(DB.DATABASE['tokenHistory'].find(json, sort=[("_id", -1)]).skip(
                    perPage * (page - 1)).limit(perPage))
            else:
                json = {"student_id": user_id, "checked": False}
                tokenHistoriesList = list(DB.DATABASE['tokenHistory'].find(json, sort=[("_id", -1)]))
            tokenHistories = {
                "total_histories": len(
                    list(DB.DATABASE['tokenHistory'].find(json))),
                "token_history_list": tokenHistoriesList
            }
        except:
            tokenHistories = {
                "total_histories": 0,
                "token_history_list": []
            }
        return Response(content=orjson.dumps(tokenHistories))

    @staticmethod
    def add(amount, student_id, reward_id):
        try:
            list(
                DB.DATABASE["reward"].find({"_id": reward_id}, {"amount": True, "price": True, "_id": False}).limit(
                    1))[0]
        except:
            return "Reward not found"
        try:
            list(DB.DATABASE['user'].find({"_id": student_id}, {"current_token": True, "_id": False}))[0][
                "current_token"]
        except:
            return "Student not found"
        tokenHistory = TokenHistoryDAO(datetime.now(), amount, student_id, reward_id if reward_id else None)
        dt_string = tokenHistory.date.strftime("%d/%m/%Y %H:%M:%S")
        if amount is str(amount):
            return "Amount must be number only"
        id = ObjectId().__str__()
        DB.upsert(collection='tokenHistory', id=id, data={
            '_id': id,
            'date': dt_string,
            'amount': float(amount),
            'student_id': tokenHistory.student_id,
            'reward_id': tokenHistory.reward_id if reward_id else None,
            'checked': False
        })
        return list(DB.DATABASE['tokenHistory'].find({"_id": id}).limit(1))[0]

    @staticmethod
    def approve(transaction_id):
        try:
            DB.update(collection='tokenHistory', id=transaction_id, data={
                'checked': True
            })
            return list(DB.DATABASE['tokenHistory'].find({"_id": transaction_id}).limit(1))[0]
        except:
            return "Cannot approve this transaction (Transaction ID not found)"

    @staticmethod
    def getAllForApproval(page):
        try:
            perPage = 10
            tokenHistoriesList = list(DB.DATABASE['tokenHistory'].find({"checked": False}, sort=[("_id", -1)]).skip(
                perPage * (page - 1)).limit(perPage))
            tokenHistories = {
                "total_histories": len(
                    list(DB.DATABASE['tokenHistory'].find())),
                "token_history_list": tokenHistoriesList
            }
        except:
            tokenHistories = {
                "total_histories": 0,
                "token_history_list": []
            }
        return Response(content=orjson.dumps(tokenHistories))
