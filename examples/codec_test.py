# -*- coding: byfon -*-
import byfon


tp = byfon.Transpiler()

b = tp.alloc(init=1)
b2 = tp.alloc(init=0)
if! b or! b2:
    b.write()

print(tp.result)
