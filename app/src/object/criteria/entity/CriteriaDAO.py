class Criteria(object):
    __slots__ = "course_id", "first", "second", "third"

    def __init__(self, course_id, first, second, third):
        self.course_id: str = course_id
        self.first: bool = first
        self.second: object = second
        self.third: bool = third
