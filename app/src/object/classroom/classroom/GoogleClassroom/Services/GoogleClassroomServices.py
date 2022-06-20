import numpy as np
from srsly.ujson import ujson
from starlette.responses import Response

from app.src.object.assignment.services.AssignmentServices import AssignmentServices
from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class GoogleClassroomServices:

    @staticmethod
    def getAllPagination(user_id, page):
        try:
            perPage = 4
            google = Google.GoogleCredential(user_id)
            googleUserId = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["google_object"]["_id"]
            response = google.courses().list().execute()
            DATA = np.array([])
            for data in response.get("courses"):
                teacher = google.courses().teachers().get(courseId=data.get("id"), userId=data.get("ownerId")).execute()
                np.append(DATA, [UpdateOne({"_id": data.get("id")}, {"$set": {
                    "_id": data.get("id"),
                    "name": data.get("name"),
                    "user_id": [googleUserId],
                    "teacher": teacher.get("profile").get("name").get("fullName"),
                    "environment": "google_classroom",
                }}, upsert=True)], axis=0)
                if len(DATA) == 4:
                    DB.DATABASE['classroom'].bulk_write(DATA, ordered=False)
                    DATA = np.array([])
            if len(DATA) > 0:
                DB.DATABASE['classroom'].bulk_write(DATA, ordered=False)

            DB.DATABASE['classroom'].drop_indexes()
            DB.DATABASE['classroom'].create_index([("user_id", 1)])
            classroom = {
                "total_classrooms": len(list(DB.DATABASE['classroom'].find({"user_id": [googleUserId]}))),
                "classroom_list": list(
                    DB.DATABASE['classroom'].find({"user_id": [googleUserId]}).skip(perPage * (page - 1)).limit(perPage)
                )
            }
        except:
            classroom = {
                "total_classrooms": 0,
                "classroom_list": []
            }
        return Response(content=ujson.dumps(classroom))

    @staticmethod
    def getById(user_id, course_id):
        try:
            AssignmentServices.getAll(user_id, course_id)
            DB.DATABASE['classroom'].drop_indexes()
            DB.DATABASE['classroom'].create_index([("_id", 1)])
            return list(DB.DATABASE['classroom'].aggregate([{
                "$match": {"_id": course_id}
            }, {
                "$lookup": {
                    "from": 'assignment',
                    "localField": '_id',
                    "foreignField": 'course_id',
                    "as": "assignment_list",
                }
            }, ]))[0]
        except:
            return "The classroom is not available for this ID or the classroom ID is not correct"
