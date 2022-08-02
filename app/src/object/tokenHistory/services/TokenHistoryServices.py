from bson import ObjectId
from orjson import orjson
from datetime import datetime
from starlette.responses import Response
from app.src.object.tokenHistory.entity.TokenHistoryDAO import TokenHistoryDAO
from app.src.server.database import DB


class TokenHistoryServices:

    @staticmethod
    def getAllPagination(user_id, page):
        try:
            perPage = 10
            tokenHistoriesList = list(DB.DATABASE['tokenHistory'].find({"student_id": user_id}).skip(
                perPage * (page - 1)).limit(perPage))
            tokenHistories = {
                "total_histories": len(
                    list(DB.DATABASE['tokenHistory'].find({"student_id": user_id}))),
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
        tokenHistory = TokenHistoryDAO(datetime.now(), amount, student_id, reward_id if reward_id else None)
        dt_string = tokenHistory.date.strftime("%d/%m/%Y %H:%M:%S")
        id = ObjectId().__str__()
        DB.upsert(collection='tokenHistory', id=id, data={
            '_id': id,
            'date': dt_string,
            'amount': float(tokenHistory.amount),
            'student_id': tokenHistory.student_id,
            'reward_id': tokenHistory.reward_id if reward_id else None,
        })
        return list(DB.DATABASE['tokenHistory'].find({"_id": id}).limit(1))[0]
