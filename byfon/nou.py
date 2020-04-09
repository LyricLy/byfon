from contextlib import contextmanager

from .control import if_, while_


def write_literal(cell, lit):
    """Writes a string literal to stdout using the given cell. Destructive (replaces the cell with the last character in the literal)."""
    cell <- 0
    val = 0
    for c in lit:
        cell += ord(c) - val
        cell.write()
        val = ord(c)

@contextmanager
def while_expr(expr, *, do=None):
    """While loop using an expression instead of a fixed cell. Takes a function and evaluates the expression every loop.
    If `do` is set, uses that as the initial value for the condition (for a do-while loop). Otherwise, it evaluates the expression twice, once inside the loop and once before it.
    """
    cell = do or expr()
    with while_(cell):
        yield
        cell <- expr()

def index(cells, i):
    """Indexes into a list of cells using a seperate cell as an index. O(n)."""
    r = i.tp.alloc()
    for j, cell in cells:
        with if_(i == j):
             r <- cell
    return r
