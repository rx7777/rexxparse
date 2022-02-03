from ParseVisitor import ParseVisitor
from RxParseLexer import RxParseLexer
from RxParseParser import RxParseParser
from antlr4 import *

def rexxparse(s, tmplstr, vars=None):
    return ParseVisitor(s, vars).visitTmpl(RxParseParser(CommonTokenStream(RxParseLexer(InputStream(tmplstr)))).tmpl())

def rexxparse_tes():
    line = " one  two three four five six "
    print("    " + str(rexxparse(line, "key1 key2 key3 key4 key5")))
    print("    " + str(rexxparse(line, "key1 key2 key3 . ")))
    print("    " + str(rexxparse(line, "key1 . . key4 key5")))
    print("    " + str(rexxparse(line, ". key2 key3 . key5")))
    print("    " + rexxparse(line, "key1 . . key4 key5")['key4'])
    print("    " + str(rexxparse(line, "key1 'ree' key3")))
    print("    " + str(rexxparse(line, "key1 (part) key3", {'part': 'ree'})))
    print("    " + str(rexxparse(line, "key1 'rEe' key3")))
    print("    " + str(rexxparse(line, "key1 (part) key3", {'part': 'rEe'})))
    print("    " + str(rexxparse(line, 'key1 key2 "ree"')))
    print("    " + str(rexxparse(line, 'key1 key2 "rEe"')))
    print("    " + str(rexxparse(line, '2 key1 7 key2 key3')))
    print("    " + str(rexxparse(line, '2 key1 15')))
    print("    " + str(rexxparse(line, '=2 key1 =7 key2 key3')))
    print("    " + str(rexxparse(line, '=2 key1 =15')))

if __name__ == '__main__':
    rexxparse_tes()
