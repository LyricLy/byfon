from .errors import FreedCellError
from contextlib import contextmanager


def need_alloc(func):
    def new_meth(self, *args):
        if self.freed:
            raise FreedCellError(f"cell at {self.ptr} was already freed")
        return func(self, *args)
    return new_meth


class Cell:
    def __init__(self, tp, ptr):
        self._tp = tp
        self.ptr = ptr
        self.freed = False
        self.mov_on_lt = False
        self.is_zero = True

    @need_alloc
    def free(self):
        self.freed = True

    @need_alloc
    def ensure_zero(self):
        if not self.is_zero:
            self._exe_on("[-]")
            self.is_zero = True

    @need_alloc
    def _exe_on(self, code):
        self.is_zero = False
        self._tp.seek(self.ptr)
        self._tp.exe(code)

    @need_alloc
    def copy(self):
        c1 = self._tp.alloc()
        c2 = self._tp.alloc()
        self.mov(c1, c2)
        self <- c2
    
        return c1

    @need_alloc
    def mov(self, *args):
        for b in args:
            b.freed = False
            b.ensure_zero()
        self._tp.seek(self.ptr)
        with self._tp.loop():
            self._tp.exe("-")
            for b in args:
                b._exe_on("+")
            self._tp.seek(self.ptr)
        self.free()

    @need_alloc
    def output(self):
        self._exe_on(".")

    @need_alloc
    def input(self):
        self._exe_on(",")
        return self

    @contextmanager
    @need_alloc
    def _if(self):
        self._tp.seek(self.ptr)
        with self._tp.loop():
            yield
            self <- 0
        self.free()

    @contextmanager
    @need_alloc
    def _while(self):
        """Run the code in the block only while cell is nonzero.

        Usage:
        with cell._w
        """
        self._tp.seek(self.ptr)
        with self._tp.loop():
            yield

    @need_alloc
    def not_(self):
        """Negate a cell with boolean logic. Sets cell to 0 if it is nonzero, and 1 otherwise."""
        res = self._tp.alloc()
        res += 1
        with self._if():
            res -= 1
        return res

    @need_alloc
    def __invert__(self):
        return self.copy()

    def __neg__(self):
        self.mov_on_lt = True
        return self

    def __lt__(self, other):
        if self.mov_on_lt:
            self.mov_on_lt = False
            if isinstance(other, Cell):
                other.mov(self)
            else:
                self.freed = False
                self.ensure_zero()
                self._exe_on("+" * -other)
        else:
            return NotImplemented

    @need_alloc
    def __iadd__(self, other):
        if isinstance(other, Cell):
            self._tp.seek(other.ptr)
            with self._tp.loop():
                self._tp.exe("-")
                self._exe_on("+")
                self._tp.seek(other.ptr)
            other.free()
        else:
            if other >= 0:
                self._exe_on("+" * other)
            else:
                self._exe_on("-" * -other)
        self.is_zero = False
        return self

    @need_alloc
    def __isub__(self, other):
        if isinstance(other, Cell):
            self._tp.seek(other.ptr)
            with self._tp.loop():
                self._tp.exe("-")
                self._exe_on("-")
                self._tp.seek(other.ptr)
            other.free()
        else:
            if other >= 0:
                self._exe_on("-" * other)
            else:
                self._exe_on("+" * -other)
        self.is_zero = False
        return self

    @need_alloc
    def __imul__(self, other):
        if isinstance(other, Cell):
            cur = ~self
            with other._while():
                self += ~cur
                other -= 1
            other.free()
        else:
            cur = ~self
            for _ in range(other):
                self += ~cur
        return self

    @need_alloc
    def __add__(self, other):
        res = ~self
        if isinstance(other, Cell):
            res += ~other
        else:
            res += other
        res.is_zero = False
        return res
    __radd__ = __add__

    @need_alloc
    def __sub__(self, other):
        res = ~self
        if isinstance(other, Cell):
            res -= ~other
        else:
            res -= other
        res.is_zero = False
        return res

    @need_alloc
    def __rsub__(self, other):
        res = self._tp.alloc()
        res += other
        res -= ~self
        return res

    @need_alloc
    def __eq__(self, other):
        return (self != other).not_()

    @need_alloc
    def __neq__(self, other):
        if isinstance(other, Cell):
            with self._while():
                self -= 1
                other -= 1
            return other
        else:
            self -= other
            return self
