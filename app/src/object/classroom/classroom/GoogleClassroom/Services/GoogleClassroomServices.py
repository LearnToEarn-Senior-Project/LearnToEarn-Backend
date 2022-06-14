from app.src.object.assignment.services.AssignmentServices import AssignmentServices
from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class GoogleClassroomServices:

    @staticmethod
    def getAllPagination(user_id, page, perPage):
        try:
            google = Google.GoogleCredential(user_id)
            googleUserId = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["google_object"]["_id"]
            try:
                response = google.courses().list().execute()
            except:
                Google.GoogleCredential(user_id)
                response = google.courses().list().execute()
            DATA = []
            for data in response.get("courses"):
                teacher = google.courses().teachers().get(courseId=data.get("id"), userId=data.get("ownerId")).execute()
                DATA.append(UpdateOne({"_id": data.get("id")}, {"$set": {
                    "_id": data.get("id"),
                    "name": data.get("name"),
                    "user_id": [googleUserId],
                    "teacher": teacher.get("profile").get("name").get("fullName"),
                    "environment": "google_classroom",
                }}, upsert=True))
                if len(DATA) == 4:
                    DB.DATABASE['classroom'].bulk_write(DATA, ordered=False)
                    DATA = []
            if len(DATA) > 0:
                DB.DATABASE['classroom'].bulk_write(DATA, ordered=False)

            DB.DATABASE['classroom'].drop_indexes()
            DB.DATABASE['classroom'].create_index([("user_id", 1)])
            totalClassroom = len(list(DB.DATABASE['classroom'].find({"user_id": [googleUserId]})))
            classroom_list = list(
                DB.DATABASE['classroom'].find({"user_id": [googleUserId]}).skip(perPage * (page - 1)).limit(perPage)
            )
            classroom = {
                "total_classrooms": totalClassroom,
                "classroom_list": classroom_list
            }
        except:
            classroom = {
                "total_classrooms": 0,
                "classroom_list": []
            }
        return classroom

    @staticmethod
    def getById(user_id, course_id):
        AssignmentServices.updateAndAdd(user_id, course_id)
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
