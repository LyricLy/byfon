from byfon import Transpiler, if_, write_literal


tp = Transpiler()

word = tp.alloc_word(4)
word._succ()

print(tp.result)
