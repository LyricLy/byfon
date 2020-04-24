from contextlib import contextmanager
import sys

from .errors import FreedCellError
from .logical import And, Or
from .while_ import while_expr


def need_alloc(func):
    def new_meth(self, *args):
        for arg in args:
            if func.__name__ != "mov" and getattr(arg, "freed", False):
                raise FreedCellError(f"cell at {arg.ptr} was already freed")
        if self.freed:
            raise FreedCellError(f"cell at {self.ptr} was already freed")
        return func(self, *args)
    return new_meth

def resolve_diff(diff):
    """Find the shortest BF code to change a cell by `diff`, making use of overflow."""
    diff %= 256
    if diff < 128:
        return "+" * diff
    else:
        return "-" * (256 - diff)

def unpack(ts, default=None):
    for t in ts:
        try:
            x, y = t
        except TypeError:
            x = t
            y = default
        yield x, y

class Cell:
    def __init__(self, tp, ptr, *, is_zero=True):
        self.tp = tp
        self.ptr = ptr
        self.freed = False
        self._mov_on_lt = False
        self._must_be_zero = is_zero

    @need_alloc
    def free(self):
        # the ultimate space optimization
        if self._must_be_zero:
            self.tp._temps.append(self)
        self.freed = True

    def _exe_on(self, code, reset_zero=True):
        self.tp.seek(self.ptr)
        self.tp.exe(code)
        if code and reset_zero:
            self._must_be_zero = False

    def _ensure_zero(self):
        if not self._must_be_zero:
            self._exe_on("[-]")
            self._known_zero()

    def _known_zero(self):
        if not self._must_be_zero:
            try:
                self.tp._restores[-1].append(self)
            except IndexError:
                pass
        self._must_be_zero = True

    @need_alloc
    def copy(self):
        """Create a copy of the cell and return the new cell."""
        c1 = self.tp.alloc()
        c2 = self.tp.alloc()
        self.mov(c1, c2)
        self |= c2

        return c1

    @need_alloc
    def mov(self, *args):
        """Move the cell's value to one or more other cells. Destructive (replaces destinations, frees source)"""
        for b, _ in unpack(args):
            b.freed = False
            b._ensure_zero()

        self.tp.seek(self.ptr)
        with self.tp.loop():
            self.tp.exe("-")
            for b, m in unpack(args, 1):
                b._exe_on("+" * m)
            self.tp.seek(self.ptr)

        self._known_zero()
        self.free()

    def write(self):
        """Write the cell's current value to stdout. Non-destructive."""
        self._exe_on(".", False)

    @need_alloc
    def read(self):
        """Read a single byte from stdin into the cell. Returns self for chaining with Transpiler.alloc(). Destructive (replaces current value)."""
        self._exe_on(",")
        return self

    @need_alloc
    def __iter__(self):
        self.tp.seek(self.ptr)
        if self._must_be_zero:
            print(f"WARNING: redundant if detected, cell at {self.ptr} is guaranteed to be 0", file=sys.stderr)
        with self.tp.loop():
            yield
            self |= 0
        self._known_zero()
        self.free()

    @contextmanager
    @need_alloc
    def _while(self):
        self.tp.seek(self.ptr)
        if self._must_be_zero:
            print(f"WARNING: redundant while detected, cell at {self.ptr} is guaranteed to be 0", file=sys.stderr)
        with self.tp.loop():
            yield
            if self._must_be_zero:
                print(f"WARNING: while loop is equivalent to if, cell at {self.ptr} is guaranteed to be 0 after first loop", file=sys.stderr)
        self._known_zero()

    @need_alloc
    def not_(self):
        """Negate the cell with boolean logic. Sets cell to 0 if it is nonzero, and 1 otherwise. Destructive (might replace current value, might destroy and make a new one)."""
        if self._must_be_zero:
            self += 1
            self._must_be_zero = False
            return self
        else:
            res = self.tp.alloc()
            res += 1
            for if_ in self:
                res -= 1
            return res

    @need_alloc
    def and_(self, other):
        """Perform logical AND on two cells. Destructive (frees both cells)."""
        res = self.tp.alloc()
        for if_ in self:
            for if_ in other:
                res += 1
        return res

    @need_alloc
    def or_(self, other, *, normal=False):
        """Perform logical OR on two cells. Destructive (replaces first cell, frees second one).
        If normal is True, forces result to be one of 0 or 1. Allocates an additional cell.
        """
        result = self + other
        if normal:
            new_result = self.tp.alloc()
            for if_ in result:
                new_result += 1
            result = new_result
        return result

    def __hash__(self):
        return self.ptr

    def __repr__(self):
        after = " = 0" if self._must_be_zero else ""
        return f"Cell(*{self.ptr}{after})"

    def __invert__(self):
        return self.copy()

    def __neg__(self):
        self._mov_on_lt = True
        return self

    def __ior__(self, other):
        if isinstance(other, Cell):
            other.mov(self)
        else:
            self.freed = False
            self._ensure_zero()
            self._exe_on(resolve_diff(other))
        return self

    @need_alloc
    def __and__(self, other):
        """Create a dummy object for use in if_ that acts like the logical AND of two cells.
        Does not actually perform AND, use Cell.and_ for this.
        """
        return And(self, other)

    @need_alloc
    def __or__(self, other):
        """Create a dummy object for use in if_ that acts like the logical OR of two cells.
        Does not actually perform OR, use Cell.or_ for this.
        """
        return Or(self, other)

    @need_alloc
    def __iadd__(self, other):
        """Add a cell or integer to the cell. Frees the cell being added."""
        if isinstance(other, Cell):
            self.tp.seek(other.ptr)
            with self.tp.loop():
                self.tp.exe("-")
                self._exe_on("+")
                self.tp.seek(other.ptr)
            other._known_zero()
            other.free()
        else:
            self._exe_on(resolve_diff(other))
        return self

    @need_alloc
    def __isub__(self, other):
        """Subtract a cell or integer from the cell. Frees the cell being subtracted."""
        if isinstance(other, Cell):
            self.tp.seek(other.ptr)
            with self.tp.loop():
                self.tp.exe("-")
                self._exe_on("-")
                self.tp.seek(other.ptr)
            other._known_zero()
            other.free()
        else:
            self._exe_on(resolve_diff(-other))
        return self

    @need_alloc
    def __add__(self, other):
        """Sum two cells or a cell and an integer. Destructive, non-commutative (mutates left argument, frees right). For non-destructive, commutative behaviour, copy both sides."""
        self += other
        return self
    __radd__ = __add__

    @need_alloc
    def __sub__(self, other):
        """Subtract two cells or a cell and an integer. Destructive. (mutates left argument, frees right). For non-destructive behaviour, copy both sides."""
        self -= other
        return self

    @need_alloc
    def __rsub__(self, other):
        """Subtract the cell from an integer. Destructive (frees)."""
        res = self.tp.alloc()
        res += other
        res -= self
        return res

    @need_alloc
    def __mul__(self, other):
        """Multiply a cell and an integer. Destroys the cell."""
        new = self.tp.alloc()
        self.mov((new, other))
        return new
    __rmul__ = __mul__

    @need_alloc
    def __eq__(self, other):
        """Check if the value pointed to by two cells is identical. Destroys both cells (frees them).
        Does not compare the pointers themselves; for that, compare the ptr attributes of the cells.
        """
        return (self != other).not_()

    @need_alloc
    def __ne__(self, other):
        """Check if the value pointed to by two cells differs. Destroys the first cell (frees it), returns the second un-normalized.
        Does not compare the pointers themselves; for that, compare the ptr attributes of the cells.
        """
        if isinstance(other, Cell):
            with self._while():
                self -= 1
                other -= 1
            self.free()
            return other
        else:
            self -= other
            return self
