class ClassroomDAO(object):
    __slots__ = "name", "total_member", "environment", "teacher", "user_id"

    def __init__(self, name, environment, teacher, user_id):
        self.name: str = name
        self.environment: str = environment
        self.teacher: object = teacher
        self.user_id: list[str] = user_id
