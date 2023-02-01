from contextlib import contextmanager

from .cell import Cell
from .word import Word


class Transpiler:
    def __init__(self, *, optimise_clears=True, file=None):
        self._ptr = 0
        self._last_open = 0
        self._temps = []
        self._restores = []
        self._code = []
        self._backtracks = []
        self.optimise_clears = optimise_clears
        self._file = file

    def seek(self, seek_ptr):
        if seek_ptr > self._ptr:
            self.exe(">" * (seek_ptr-self._ptr))
        else:
            self.exe("<" * (self._ptr-seek_ptr))
        self._ptr = seek_ptr

    def exe(self, code):
        if not self._file:
            self._code.append(code)
        else:
            self._file.write(code)

    def alloc(self, *, init=0, consecutive=False, **kwargs):
        if not consecutive:
            while self._temps:
                old_cell = self._temps.pop(0)
                # it could have been un-freed, in which case we shouldn't use it
                if old_cell.freed:
                    old_cell |= init
                    return old_cell
        b = Cell(self, self._last_open, **kwargs)
        self._last_open += 1
        b += init
        return b

    def alloc_word(self, size=8):
        return Word([self.alloc() for _ in range(size)])

    @property
    def result(self):
        if not self._file:
            code = "".join(self._code)
            while True:
                old_code = code
                # simple optimizations
                replacements = {
                    "+-": "",
                    "-+": "",
                    "><": "",
                    "<>": ""
                }
                for trigger, repl in replacements.items():
                    code = code.replace(trigger, repl)
                if code == old_code:
                    return code
        else:
            self._file.close()
            return "output in file"

    @contextmanager
    def loop(self):
        base_ptr = self._ptr
        self.exe("[")
        self._restores.append([])
        yield
        for cell in self._restores.pop():
            cell._must_be_zero = False
        self.seek(base_ptr)
        self.exe("]")
