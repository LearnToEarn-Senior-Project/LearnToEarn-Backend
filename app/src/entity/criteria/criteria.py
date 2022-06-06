from json import dumps

from bson import ObjectId

from app.src.database import DB


class Criteria(object):
    def __init__(self, criteria_name, criteria_detail, top_rank, submit_stack):
        self.criteria_name = criteria_name
        self.criteria_detail = criteria_detail
        self.top_rank = top_rank
        self.submit_stack = submit_stack

    def addReward(self):
        DB.insert(collection='Criteria', data={
            '_id': ObjectId().__str__(),
            'criteria_name': self.criteria_name,
            'criteria_detail': self.criteria_detail,
            'top_rank': self.top_rank,
            'submit_stack': self.submit_stack
        }

    def addCriteria(self):
        DB.insert(collection='criteria', data=self.addJson())

    @staticmethod
    def getAllCriterias():
        cursor = DB.DATABASE['criteria'].find()
        criteriaList = list(cursor)
        json_data = dumps(criteriaList, indent=2)
        return json_data
