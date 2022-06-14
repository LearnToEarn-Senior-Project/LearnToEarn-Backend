from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class AssignmentServices:

    @staticmethod
    def updateAndAdd(id, course_id):
        submitList = None
        submission = None
        google = Google.GoogleCredential(id)
        googleUserId = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]["_id"]
        DATA = []
        for assignment in google.courses().courseWork().list(courseId=course_id).execute().get("courseWork"):
            try:
                submission = google.courses().courseWork().studentSubmissions().list(
                    courseId=course_id, courseWorkId=assignment.get("id"), userId=googleUserId).execute().get(
                    "studentSubmissions")[0]
                submitList = list(
                    DB.DATABASE["assignment"].find(
                        {"_id": assignment.get("id"), "student_submission.user_id": submission.get("userId")}))
                if submission.get("userId") not in submitList:
                    submitList.append({
                        "user_id": submission.get("userId"),
                        "state": submission.get("state"),
                        "score": submission.get("assignedGrade") if submission.get("assignedGrade") is not None else 0
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
                "student_submission": submitList if submission is not None else {}
            }}, upsert=True))
            if len(DATA) == 10:
                DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
                DATA = []
        if len(DATA) > 0:
            DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
