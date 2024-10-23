from enum import Enum
from antlr4 import *
from .antlr.src.RegexLexer import RegexLexer
from .antlr.src.RegexParser import RegexParser
from .antlr.src.RegexVisitor import RegexVisitor
from .regvisitor import RegVMVisitor


class RegexMachine:
    Instructions: Enum = Enum(
        "Instructions", ["Char", "Match", "Jmp", "Split"])

    def print(self):
        print(self.regex)
        for ip in range(len(self.program)):
            print(ip, " ", self.program[ip].name, " ", *self.args[ip])

    def __init__(self, regex: str):
        self.regex: str = regex
        self.program: List[Instructions] = []
        self.args: list[list[chr] | list[int]] = []

        input_stream = InputStream(regex)

        lexer = RegexLexer(input_stream)
        stream = CommonTokenStream(lexer)

        parser = RegexParser(stream)
        visitor = RegVMVisitor()

        try:
            res = visitor.visit(parser.expr())

            if res is None or stream.LT(1).type != Token.EOF or parser.getNumberOfSyntaxErrors() > 0:
                raise RuntimeError("Parse error")
            else:
                self.program, self.args = res
        except TypeError:
            raise RuntimeError("Parse error")

        length = len(self.program)
        for ip in range(length):
            self.program[ip] = self.Instructions(self.program[ip])
            if self.program[ip] == self.Instructions.Split:
                self.args[ip][0] += ip
                self.args[ip][1] += ip
            if self.program[ip] == self.Instructions.Jmp:
                self.args[ip][0] += ip
        self.program.append(self.Instructions.Match)
        self.args.append([])

    def accepts(self, word: str, pc: int = 0, wc: int = 0):
        if pc >= len(self.program):
            return False
        args = self.args[pc]
        match self.program[pc]:
            case self.Instructions.Char:
                if wc >= len(word) or word[wc] != args[0]:
                    return False
                return self.accepts(word, pc + 1, wc + 1)
            case self.Instructions.Match:
                return wc == len(word)
            case self.Instructions.Jmp:
                return self.accepts(word, args[0], wc)
            case self.Instructions.Split:
                if self.accepts(word, args[0], wc):
                    return True
                return self.accepts(word, args[1], wc)
        return False
