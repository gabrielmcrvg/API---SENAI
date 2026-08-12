class Paginacao:
    def __init__(self, skip: int, limit:int = 10):
        self.skip = skip
        self.limit = limit 