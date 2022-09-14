from app.src.object.criteria.entity.Criteria import Criteria
from app.src.server.database import DB


class CriteriaServices:
    @staticmethod
    def add(course_id, first, second, third):
        try:
            try:
                list(DB.DATABASE["classroom"].find({"_id": course_id}).limit(1))[0]
            except:
                return "classroom not found"
            criteria = Criteria(course_id, first, second, third)
            if criteria.first["value"] is None or second["value"] is None or criteria.third["value"] is None:
                return "The criteria cannot be null"
            if second["value"] is True and (
                    second["count"] <= 0 or isinstance(second["count"], float) or isinstance(second["count"], str)):
                return "The counting must more than 0 and must be integer type"
            if second["value"] is False and second["count"] is not None:
                return "The counting must be null"
            DB.upsert(collection='criteria', id=course_id, data={'_id': criteria.course_id,
                                                                 'first': criteria.first,
                                                                 'second': criteria.second,
                                                                 'third': criteria.third,
                                                                 })
            return list(DB.DATABASE['criteria'].find({"_id": criteria.course_id}))[0]
        except:
            return "The data is not complete"

    @staticmethod
    def get(course_id):
        try:
            return list(DB.DATABASE['criteria'].find({"_id": course_id}).limit(1))[0]
        except:
            try:
                list(DB.DATABASE["classroom"].find({"_id": course_id}).limit(1))[0]
            except:
                return "classroom not found"
            DB.upsert(collection='criteria', id=course_id, data={'_id': course_id,
                                                                 'first': {
                                                                     'value': False,
                                                                     'statCount': 0
                                                                 },
                                                                 'second': {
                                                                     'value': False,
                                                                     'count': None,
                                                                     'statCount': 0
                                                                 },
                                                                 'third': {
                                                                     'value': False,
                                                                     'statCount': 0
                                                                 }
                                                                 })
            return list(DB.DATABASE['criteria'].find({"_id": course_id}).limit(1))[0]
