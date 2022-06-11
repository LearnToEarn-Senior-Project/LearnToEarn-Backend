class Classroom(object):
    __slots__ = "name", "total_member", "environment", "teacher", "student_list", "assignment_list", "criteria"

    def __init__(self, name, total_member, environment, teacher, student_list, assignment_list, criteria):
        self.name: str = name
        self.total_member: int = total_member
        self.environment: str = environment
        self.teacher: object = teacher
        self.student_list: list[object] = student_list
        self.assignment_list: list[object] = assignment_list
        self.criteria: list[object] = criteria
