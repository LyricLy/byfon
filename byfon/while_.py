from contextlib import contextmanager


def while_(obj):
    return obj._while()

@contextmanager
def while_expr(expr, *, do=None):
    """While loop using an expression instead of a fixed cell. Takes a function and evaluates the expression every loop.
    If `do` is set, uses that as the initial value for the condition (for a do-while loop). Otherwise, it evaluates the expression twice, once inside the loop and once before it.
    """
    cell = do or expr()
    with while_(cell):
        yield
        cell <- expr()
