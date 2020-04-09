from .control import if_


class Word:
    def __init__(self, cells):
        self.cells = cells

    def _succ(self):
        self.cells[0] += 1
        last = self.cells[0]
        tp = self.cells[0].tp
        loops = []
        for c in self.cells[1:]:
            last._tp.seek(last.ptr)
            ptr = ~last.not_()
            ptr._exe_on("[")
            
