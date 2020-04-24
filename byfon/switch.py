from contextlib import contextmanager


class Switch:
    def __init__(self, cell):
        self._cell = cell
        self._offset = 0

    @contextmanager
    def case(self, value):
        diff = value + self._offset
        self._offset = -value
        self._cell -= diff
        for if_ in (~self._cell).not_():
            yield
