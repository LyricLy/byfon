from collections import Iterable


class And:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2

    def __iter__(self):
        for if_ in self.cell1:
            for if_ in self.cell2:
                yield

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)


class Or:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2

    def __iter__(self):
        for if_ in self.cell1:
            yield
        for if_ in self.cell2:
            yield

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)
