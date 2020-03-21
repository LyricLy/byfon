def write_literal(cell, lit):
    cell <- 0
    val = 0
    for c in lit:
        cell += ord(c) - val
        cell.output()
        val = ord(c)

def index(cells, i):
    tp = i._tp
    r = tp.allocate()
    for j, cell in cells:
        with tp.if_(i == j):
             r <- cell
    return r


