import random
import string

from RxParseVisitor import RxParseVisitor
from antlr4 import *

class ParseVisitor(RxParseVisitor):

    def __init__(self, s, vars, log=None):
        self.s = self.sorg = s
        self.vars = vars
        self.p = self.pold = 0
        self.log = log
        self.lastpart = ''
        self.lasttype = ''
        self.res = dict()

    def visitTmpl(self, ctx):
        self.visitChildren(ctx)
        return self.res

    def visitVariable(self, ctx):
        txt = ctx.var.text
        self.lastpart = txt
        self.res[txt] = self.reduce(txt)
        if self.log:
            self.log.info(txt + " ---> (" + self.res[txt] + "," + self.s + ")")
        self.lasttype = 'var'
        self.visitChildren(ctx)

    def visitOneVariable(self, ctx):
        txt = ctx.var.text
        self.lastpart = txt
        if self.lasttype == 'str':
            self.res[txt] = self.s
        else:
            self.res[txt] = self.s.lstrip()
        self.s = ''
        if self.log:
            self.log.info(txt + " ---> (" + self.res[txt] + "," + self.s + ")")
        self.lasttype = 'var'

    def visitDummy(self, ctx):
        txt = ctx.var.text
        self.lastpart = ''
        self.reduce(txt)
        if self.log:
            self.log.info(txt + " ---> (," + self.s + ")")
        self.lasttype = 'dum'
        self.visitChildren(ctx)

    def visitOneDummy(self, ctx):
        txt = ctx.var.text
        self.lastpart = ''
        self.s = ''
        if self.log:
            self.log.info(txt + " ---> (," + self.s + ")")
        self.lasttype = 'dum'

    def visitOneString(self, ctx):
        self.visString(ctx.var.text[1:-1])

    def visitString(self, ctx):
        self.visString(ctx.var.text[1:-1])
        self.visitChildren(ctx)

    def visitOneNumber(self, ctx):
        txt = ctx.var.text
        nbr = int(txt)
        if self.lasttype == 'var':
            self.res[self.lastpart] = self.sorg[self.pold: nbr - 1]
        self.pold = self.p
        self.p = nbr
        self.lasttype = 'nbr'
        self.lastpart = txt

    def visitNumber(self, ctx):
        self.visitOneNumber(ctx)
        self.visitChildren(ctx)

    def visitOnePattern(self, ctx):
        pat = ctx.var.text
        if pat in self.res:
            self.visString(self.res[pat])
        elif pat in self.vars:
            self.visString(self.vars[pat])
        else:
            if self.log:
                self.log.error('Failed to determine value of variable "{}"'.format(pat))
            self.visString(''.join(random.choices(string.ascii_letters, k=15)))

    def visitPattern(self, ctx):
        self.visitOnePattern(ctx)
        self.visitChildren(ctx)

    def reduce(self, txt):
        prelen = len(self.s)
        if self.lasttype == 'str':
            lis = self.s.split(' ', maxsplit=1)
        elif self.lasttype == 'nbr':
            lis = self.sorg[self.p:].split(' ', maxsplit=1)
        else:
            lis = self.s.lstrip().split(' ', maxsplit=1)
        if len(lis) == 1:
            self.s = ''
        else:
            self.s = lis[1]
        self.pold = self.p
        self.p += prelen - len(self.s)
        return lis[0]

    def visString(self, txt):
        prelen = len(self.s)
        if self.lastpart:
            lis = self.sorg[self.pold:].split(txt, maxsplit=1)
            if len(lis) == 1:
                self.res[self.lastpart] += " " + self.s
                self.s = ''
            else:
                self.res[self.lastpart] = lis[0]
                self.s = lis[1]
            if self.log:
                self.log.info(txt + " ---> (" + self.res[self.lastpart] + "," + self.s + ")")
            self.lastpart = ''
        elif self.lasttype == 'dum':
            lis = self.sorg[self.pold:].split(txt, maxsplit=1)
            if len(lis) == 1:
                self.s = ''
            else:
                self.s = lis[1]
            if self.log:
                self.log.info(txt + " ---> (," + self.s + ")")
            self.lastpart = ''
        else:
            lis = self.s.split(txt, maxsplit=1)
            if len(lis) == 1:
                self.s = ''
            else:
                self.s = lis[1]
            if self.log:
                self.log.info(txt + " ---> (," + self.s + ")")
        self.pold = self.p
        self.p += prelen - len(self.s)
        self.lasttype = 'str'
