from orjson import orjson
from starlette.responses import Response
from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class AssignmentServices:

    @staticmethod
    def getAll(id, course_id):
        try:
            submission = None
            google = Google.GoogleCredential(id)
            googleUserId = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]["_id"]
            DATA = []
            for assignment in google.courses().courseWork().list(courseId=course_id).execute().get(
                    "courseWork"):
                arr = []
                try:
                    submission = google.courses().courseWork().studentSubmissions().list(
                        courseId=course_id, courseWorkId=assignment.get("id"), userId=googleUserId).execute().get(
                        "studentSubmissions")[0]
                    submitList = list(
                        DB.DATABASE["assignment"].find(
                            {"_id": assignment.get("id"), "student_submission.user_id": submission.get("userId")}))
                    if submission.get("userId") not in submitList:
                        arr.append({
                            "user_id": submission.get("userId"),
                            "state": submission.get("state"),
                            "score": submission.get("assignedGrade") if submission.get(
                                "assignedGrade") is not None else 0
                        })
                except:
                    pass
                DATA.append(UpdateOne({'_id': assignment.get("id")}, {'$set': {
                    "_id": assignment.get("id"),
                    "course_id": assignment.get("courseId"),
                    "name": assignment.get("title"),
                    "due_date": assignment.get("dueDate"),
                    "due_time": assignment.get("dueTime"),
                    "max_point": assignment.get("maxPoints"),
                    "student_submission": arr if submission is not None else []
                }}, upsert=True))
                if len(DATA) == 10:
                    DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
                    DATA = []
            if len(DATA) > 0:
                DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
            return Response(content=orjson.dumps(list(DB.DATABASE['assignment'].find({"course_id": course_id}))))
        except:
            return "The assignment is not available for this ID or the classroom ID is not correct"
