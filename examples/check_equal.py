import byfon


tp = byfon.Transpiler()


x = tp.alloc().read()
y = tp.alloc().read()

res = x == y
res += ord("0")
res.write()

print(tp.result)
