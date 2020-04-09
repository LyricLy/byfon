from contextlib import contextmanager

from .cell import Cell
from .word import Word


class Transpiler:
    def __init__(self):
        self._ptr = 0
        self._last_open = 0
        self._temps = []
        self._restores = []
        self._code = []
        from collections import defaultdict
        self._ptrs = defaultdict(list)

    def seek(self, seek_ptr):
        if seek_ptr > self._ptr:
            self._code.append(">" * (seek_ptr-self._ptr))
        else:
            self._code.append("<" * (self._ptr-seek_ptr))
        self._ptr = seek_ptr

    def exe(self, code):
        self._code.append(code)

    def alloc(self):
        while self._temps:
            old_cell = self._temps.pop(0)
            # it could have been un-freed, in which case we shouldn't use it
            if old_cell.freed:
                old_cell <- 0
                return old_cell
        b = Cell(self, self._last_open)
        self._ptrs[self._last_open].append(b)
        self._last_open += 1
        return b

    def alloc_word(self, size=8):
        return Word([self.alloc() for _ in range(size)])

    @property
    def result(self):
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
