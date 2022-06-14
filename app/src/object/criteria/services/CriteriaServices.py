from bson import ObjectId
from app.src.server.database import DB


class CriteriaServices:
    @staticmethod
    def add(name, detail, top_rank, submit_stack):
        id = ObjectId().__str__()
        DB.insert(collection='criteria', data={'_id': id,
                                               'criteria_name': name,
                                               'top_rank': top_rank,
                                               'submit_stack': submit_stack})
        return DB.DATABASE['criteria'].find({"id": id})

    @staticmethod
    def getAll():
        return list(DB.DATABASE['criteria'].find())
