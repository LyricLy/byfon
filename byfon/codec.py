import codecs
import re
import encodings
from typing import Tuple


utf8 = encodings.search_function("utf8")

repl_table = {
    "if!": "for _BYFON_DUMMY in",
    "while! (.*?):": r"with byfon.while_(\1):",
    "whilex! (.*?):": r"with byfon.while_expr(lambda: \1):",
    "or!": ")|(",
    "and!": ")&(",
    "<-": "|=",
    r"\.not([^a-zA-Z_])": r".not_()\1"
}

def decode(text, errors="strict"):
    text, _ = utf8.decode(text, errors)
    for pttrn, repl in repl_table.items():
        text = re.sub(pttrn, repl, text)
    return text, len(text)

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input_, errors, final):
        if final:
            return decode(input_, errors)
        else:
            return "", 0

class StreamReader(utf8.streamreader):
    _stream = None
    _decoded = False

    @property
    def stream(self):
        if not self._decoded:
            text, _ = decode(self._stream.read())
            self._stream = io.BytesIO(text.encode("utf8"))
            self._decoded = True
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream
        self._decoded = False

def register():
    codecs.register(lambda n: None if n != "byfon" else codecs.CodecInfo(
        name = "byfon",
        encode = utf8.encode,
        decode = decode,
        incrementalencoder = utf8.incrementalencoder,
        incrementaldecoder = IncrementalDecoder,
        streamwriter = utf8.streamwriter,
        streamreader = StreamReader
    ))
