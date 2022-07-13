from app.src.object.criteria.entity.CriteriaDAO import Criteria
from app.src.server.database import DB


class CriteriaServices:
    @staticmethod
    def add(course_id, first, second, third):
        criteria = Criteria(course_id, first, second, third)
        DB.upsert(collection='criteria', id=course_id, data={'_id': criteria.course_id,
                                                             'first': criteria.first,
                                                             'second': criteria.second,
                                                             'third': criteria.third,
                                                             })
        return DB.DATABASE['criteria'].find({"id": criteria.course_id})

    @staticmethod
    def get(course_id):
        try:
            return list(DB.DATABASE['criteria'].find({"_id": course_id}).limit(1))[0]
        except:
            DB.upsert(collection='criteria', id=course_id, data={'_id': course_id,
                                                                 'first': False,
                                                                 'second': {
                                                                     'value': False,
                                                                     'count': None
                                                                 },
                                                                 'third': False,
                                                                 })
            return list(DB.DATABASE['criteria'].find({"_id": course_id}).limit(1))[0]

    @staticmethod
    def getAll():
        return list(DB.DATABASE['criteria'].find())
