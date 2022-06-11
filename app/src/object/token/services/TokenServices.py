from app.src.object.token.entity.Token import Token
from app.src.server.database import DB


class TokenServices:
    @staticmethod
    def addToken(amount):
        tokenAmount = Token(amount)
        token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))
        if not token:
            DB.insert(collection='token', data={
                '_id': "1",
                'amount': tokenAmount.amount
            })
        else:
            current_token = token[0]["amount"]
            DB.update(collection='token', id="1", data={
                'amount': current_token + tokenAmount.amount
            })
        return token

    @staticmethod
    def getStudentToken(id):
        try:
            studentToken = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["current_token"]
        except:
            studentToken = []
        return studentToken

    @staticmethod
    def getTokenAmount():
        return DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"]
