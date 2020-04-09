from contextlib import contextmanager

from .control import if_, while_


# TODO: add more functionality to this and an Or type (probably has to use for instead of with for control over how many times the code is executed)

class And:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2

    @contextmanager
    def _if(self):
        with if_(self.cell1):
            with if_(self.cell2):
                yield

    def __and__(self, other):
        return And(self, other)
