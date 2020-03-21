import byfon


tp = byfon.Transpiler()


x = tp.alloc().input()
y = tp.alloc().input()

res = x == y
res += ord("0")
res.output()


print(tp.result)
