from app.src.server.database import DB


class AssignmentServices:

    @staticmethod
    def getAll():
        return list(DB.DATABASE['assignment'].find())
