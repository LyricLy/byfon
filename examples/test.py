from byfon import Transpiler, if_, while_, while_expr, write_literal


tp = Transpiler()

b = tp.alloc()
b <- 10

with if_((~b != 0).and_(b != 1)):
    write_literal(tp.alloc(), "true")

print(tp.result)
