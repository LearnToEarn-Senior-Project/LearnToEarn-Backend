from bson import ObjectId
from orjson import orjson
from starlette.responses import Response

from app.src.object.tokenHistory.entity.TokenHistoryDAO import TokenHistoryDAO
from app.src.server.database import DB


class TokenHistoryServices:

    @staticmethod
    def getByID(tokenHistory_id):
        return Response(content=orjson.dumps(list(DB.DATABASE['tokenHistory'].find({"_id": tokenHistory_id}).limit(1))))

    @staticmethod
    def add(date,amount,student_id,reward_id):
        try:
            if (date and amount and student_id and reward_id is not None) and type(amount) is float and (amount >= 0):
                tokenHistory = TokenHistoryDAO(date,amount,student_id,reward_id)
                id = ObjectId().__str__()
                DB.insert(collection='tokenHistory', data={
                    '_id': id,
                    'date': tokenHistory.date,
                    'amount': tokenHistory.amount,
                    'student_id': tokenHistory.student_id,
                    'reward_id': tokenHistory.reward_id,
                })
                return TokenHistoryServices.getByID(id)
            else:
                return "The input is required or the type of data is not correct"
        except:
            return

    @staticmethod
    def getAllTokenHistory(student_id, page):
        try:
            print("test")
            perPage = 10
            if page > 0:
                tokenHistory_list = list(DB.DATABASE['tokenHistory'].find({"student_id": student_id}).skip(perPage * (page - 1)).limit(perPage))
                tokenHistory = {
                    "tokenHistory_list": tokenHistory_list
                }
                return tokenHistory
            else:
                tokenHistory = {
                    "tokenHistory_list": []
                }
                return Response(content=orjson.dumps(tokenHistory))
        except:
            tokenHistory = {
                "tokenHistory_list": []
            }
            return tokenHistory