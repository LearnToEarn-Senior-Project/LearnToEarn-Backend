from app.src.database import DB


class Token(object):
    def __init__(self, amount):
        self.amount = amount

    def addToken(self):
        token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))
        if not token:
            DB.insert(collection='token', data={
                '_id': "1",
                'amount': float(self.amount)
            })
        else:
            current_token = token[0]["amount"]
            DB.update(collection='token', id="1", data={
                'amount': current_token + float(self.amount)
            })
        return token

    @staticmethod
    def getStudentToken(id):
        studentToken = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["current_token"]
        return studentToken
