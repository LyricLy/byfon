from contextlib import contextmanager


class Switch:
    def __init__(self, cell):
        self._cell = cell
        self._offset = 0
        self._not_cell = self._cell._tp.alloc()

    @contextmanager
    def case(self, value):
        diff = value + self._offset
        self._offset = -value
        self._cell -= diff
        self._cell._tp.temps.append(self._not_cell)
        with (~self._cell).not_()._if():
            yield
