from app.src.object.token.entity.TokenDAO import TokenDAO
from app.src.server.database import DB


class TokenServices:
    @staticmethod
    def add(amount):
        try:
            if amount > 0:
                tokenAmount = TokenDAO(amount)
                token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))
                if not token:
                    DB.insert(collection='token', data={
                        '_id': "1",
                        'amount': tokenAmount.amount
                    })
                    token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))
                else:
                    current_token = token[0]["amount"]
                    DB.update(collection='token', id="1", data={
                        'amount': current_token + tokenAmount.amount
                    })
                    token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))
                return token
            else:
                return "Token amount must more than 0!!"
        except:
            return "The token amount cannot be null"

    @staticmethod
    def getStudentToken(user_id):
        try:
            studentToken = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["current_token"]
        except:
            studentToken = []
        return studentToken

    @staticmethod
    def getAmount():
        try:
            return DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"]
        except:
            return 0
