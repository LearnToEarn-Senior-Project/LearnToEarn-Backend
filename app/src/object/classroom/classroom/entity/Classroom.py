class Classroom(object):
    __slots__ = "name", "total_member", "environment", "teacher", "user_id", "criteria"

    def __init__(self, name, environment, teacher, user_id, criteria):
        self.name: str = name
        self.environment: str = environment
        self.teacher: object = teacher
        self.user_id: list[object] = user_id
        self.criteria: list[object] = criteria
