import byfon


tp = byfon.Transpiler()

byfon.write_literal(tp.alloc(), "Hello, World!")

print(tp.result)
