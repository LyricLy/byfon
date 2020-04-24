# -*- coding: byfon -*-
import byfon


tp = byfon.Transpiler()

one = tp.alloc(init=1)
zero = tp.alloc(init=0)

if! (~one or! ~zero) or! (~one or! (~one and! one)):
    byfon.write_literal(tp.alloc(), "write")
    one <- 0

print(tp.result)
