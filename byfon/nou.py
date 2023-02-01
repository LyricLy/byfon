def write_literal(cell, lit):
    """Writes a string literal to stdout using the given cell. Destructive (frees)."""
    cell |= 0
    val = 0
    for c in lit:
        cell += ord(c) - val
        cell.write()
        val = ord(c)
    cell -= val
    cell.free()

def index(cells, i):
    """Indexes into a list of cells using a seperate cell as an index. O(n)."""
    r = i.tp.alloc()
    for j, cell in enumerate(cells):
        for if_ in ~i == j:
             r |= cell
    return r

def index_code(cells, i):
    """Iterator version of `index`."""
    for j, cell in enumerate(cells):
        for if_ in ~i == j:
            yield cell
