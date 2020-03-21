import byfon


tp = byfon.Transpiler()

x = tp.alloc()
y = tp.alloc()
y += 1
tmp = tp.alloc()

with tp.while_(y):
    y.output()
    tmp <- ~y
    y += x
    x <- tmp

print(tp.result)
