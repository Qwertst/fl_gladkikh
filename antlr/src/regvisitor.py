from antlr4 import *
from .antlr.src.RegexLexer import RegexLexer
from .antlr.src.RegexParser import RegexParser
from .antlr.src.RegexVisitor import RegexVisitor


class RegVMVisitor(RegexVisitor):

    def visitRegex(self, ctx: RegexParser.RegexContext):
        return self.visit(ctx.expr())

    def visitPlusQuant(self, ctx: RegexParser.PlusQuantContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.append(4)
        args.append([-expr_len, +1])
        return program, args

    def visitQmarkQuant(self, ctx: RegexParser.QmarkQuantContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.insert(0, 4)
        args.insert(0, [1, expr_len+1])
        return program, args

    def visitStarQuant(self, ctx: RegexParser.StarQuantContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.insert(0, 4)
        args.insert(0, [1, expr_len+2])
        program.append(3)
        args.append([-expr_len-1])
        return program, args

    def visitOrExpr(self, ctx: RegexParser.OrExprContext):
        program_l, args_l = self.visit(ctx.left)
        program_r, args_r = self.visit(ctx.right)
        left_len = len(program_l)
        right_len = len(program_r)

        program = [4]
        args = [[1, left_len+2]]

        program.extend(program_l)
        args.extend(args_l)

        program.append(3)
        args.append([right_len+1])

        program.extend(program_r)
        args.extend(args_r)

        return program, args

    def visitConExpr(self, ctx: RegexParser.ConExprContext):
        program_l, args_l = self.visit(ctx.left)
        program_r, args_r = self.visit(ctx.right)

        program_l.extend(program_r)
        args_l.extend(args_r)

        return program_l, args_l


    def visitAtomQuant(self, ctx: RegexParser.AtomQuantContext):
        return self.visit(ctx.atom())


    def visitTermExpr(self, ctx:RegexParser.TermExprContext):
        return self.visit(ctx.term())


    def visitQuantExpr(self, ctx:RegexParser.QuantExprContext):
        return self.visit(ctx.quant())


    def visitCharAtom(self, ctx:RegexParser.CharAtomContext):
        return [1], [[ctx.getText()]]


    def visitParExpr(self, ctx:RegexParser.ParExprContext):
        return self.visit(ctx.expr())

