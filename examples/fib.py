import byfon
from byfon import while_


tp = byfon.Transpiler()

x = tp.alloc()
y = tp.alloc()
y += 1
tmp = tp.alloc()

with while_(y):
    y.write()
    tmp <- ~y
    y += x
    x <- tmp

print(tp.result)
