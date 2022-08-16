class AssignmentDAO(object):
    __slots__ = "name", "course_id", "due_date", "due_time", "max_point", "student_submission"

    def __init__(self, name, course_id, due_date, due_time, max_point, student_submission):
        self.name: str = name
        self.course_id: str = course_id
        self.due_date: object = due_date
        self.due_time: object = due_time
        self.max_point: int = max_point
        self.student_submission: list[object] = student_submission
