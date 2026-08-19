class RecursoNaoEncontrado(Exception):
    def __init__(self, recurso: str):
        self.recurso = recurso