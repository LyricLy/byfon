from contextlib import contextmanager

from .control import if_


class Switch:
    def __init__(self, cell):
        self._cell = cell
        self._offset = 0
        self._not_cell = self._cell.tp.alloc()

    @contextmanager
    def case(self, value):
        diff = value + self._offset
        self._offset = -value
        self._cell -= diff
        self._cell.tp._temps.append(self._not_cell)
        with if_((~self._cell).not_()):
            yield
