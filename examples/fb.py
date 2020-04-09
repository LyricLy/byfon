from byfon import Transpiler, if_, while_, while_expr


tp = Transpiler()

b = tp.alloc().read()

def half(x):
    halved = tp.alloc()
    with while_expr(lambda: (~x != 0).and_(~x != 1)):
        halved += 1
        x -= 2
    return halved

def msb(byte):
    for _ in range(2):
        byte = half(byte)
    return byte

msb(b).write()

print(tp.result)
