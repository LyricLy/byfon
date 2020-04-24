def write_literal(cell, lit):
    """Writes a string literal to stdout using the given cell. Destructive (replaces the cell with the last character in the literal)."""
    cell |= 0
    val = 0
    for c in lit:
        cell += ord(c) - val
        cell.write()
        val = ord(c)

def index(cells, i):
    """Indexes into a list of cells using a seperate cell as an index. O(n)."""
    r = i.tp.alloc()
    for j, cell in cells:
        for if_ in i == j:
             r |= cell
    return r
