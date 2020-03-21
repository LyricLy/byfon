from .cell import Cell
from contextlib import contextmanager


class Transpiler:
    def __init__(self):
        self._ptr = 0
        self._last_open = 0
        self.temps = []
        self._code = []

    def seek(self, seek_ptr):
        if seek_ptr > self._ptr:
            self._code.append(">" * (seek_ptr-self._ptr))
        else:
            self._code.append("<" * (self._ptr-seek_ptr))
        self._ptr = seek_ptr

    def exe(self, code):
        self._code.append(code)

    def if_(self, obj):
        return obj._if()

    def while_(self, obj):
        return obj._while()

    def alloc(self):
        if not self.temps:
            b = Cell(self, self._last_open)
            self._last_open += 1
            return b
        else:
            old_cell = self.temps.pop(0)
            old_cell <- 0
            return old_cell

    @property
    def result(self):
        return "".join(self._code)

    @contextmanager
    def loop(self):
        base_ptr = self._ptr
        self.exe("[")
        yield
        self.seek(base_ptr)
        self.exe("]")
