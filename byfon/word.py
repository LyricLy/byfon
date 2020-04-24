class Word:
    def __init__(self, cells):
        if not cells:
            raise ValueError("word cannot contain 0 cells")
        self.cell = cells[0]
        self.rest = Word(cells[1:]) if cells[1:] else None

    def _clear(self):
        self.cell |= 0
        if self.rest:
            self.rest.clear()

    def _succ(self):
        self.cell += 1
        if self.rest:
            for if_ in (~self.cell).not_():
                self.rest._succ()

    def _pred(self):
        if self.rest:
            for if_ in (~self.cell).not_():
                self.rest._pred()
        self.cell -= 1

    def _if(self):
        if self.rest:
            for if_ in self.cell | self.rest:
                self.rest.clear()
                yield
        else:
            for if_ in self.cell:
                yield

    def _while(self):
        ...
