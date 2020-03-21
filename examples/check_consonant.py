import byfon


tp = byfon.Transpiler()


x = tp.alloc().input()
writer = tp.alloc()

s = byfon.Switch(x)
with s.case(ord("a")):
    byfon.write_literal(writer, "not ")
with s.case(ord("e")):
    byfon.write_literal(writer, "not ")
with s.case(ord("i")):
    byfon.write_literal(writer, "not ")
with s.case(ord("o")):
    byfon.write_literal(writer, "not ")
with s.case(ord("u")):
    byfon.write_literal(writer, "not ")

byfon.write_literal(writer, "consonant")


print(tp.result)
