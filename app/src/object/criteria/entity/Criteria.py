class Criteria(object):
    __slots__ = "name", "top_rank", "submit_stack"

    def __init__(self, name, top_rank, submit_stack):
        self.name: str = name
        self.top_rank: int = top_rank
        self.submit_stack: int = submit_stack
