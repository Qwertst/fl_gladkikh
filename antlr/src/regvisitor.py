from antlr4 import *
from .antlr.RegexLexer import RegexLexer
from .antlr.RegexParser import RegexParser
from .antlr.RegexVisitor import RegexVisitor

class RegVMVisitor(RegexVisitor):

    def visitRegex(self, ctx:RegexParser.RegexContext):
        return self.visit(ctx.expr())

    def visitPlusExpr(self, ctx:RegexParser.PlusExprContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.append(4)
        args.append([-expr_len, +1])
        return program, args

    def visitQmarkExpr(self, ctx:RegexParser.QmarkExprContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.insert(0, 4)
        args.insert(0, [1, expr_len+1])
        return program, args

    def visitStarExpr(self, ctx:RegexParser.StarExprContext):
        program, args = self.visit(ctx.atom())
        expr_len = len(program)
        program.insert(0, 4)
        args.insert(0, [1, expr_len+2])
        program.append(3)
        args.append([-expr_len-1])
        return program, args

    def visitOrExpr(self, ctx:RegexParser.OrExprContext):
        program_l, args_l = self.visit(ctx.left)
        program_r, args_r = self.visit(ctx.right)
        left_len = len(program_l)
        right_len = len(program_r)

        program = [4]
        args = [[1,left_len+2]]

        program.extend(program_l)
        args.extend(args_l)

        program.append(3)
        args.append([right_len+1])

        program.extend(program_r)
        args.extend(args_r)

        return program, args

    def visitConExpr(self, ctx:RegexParser.ConExprContext):
        program_l, args_l = self.visit(ctx.left)
        program_r, args_r = self.visit(ctx.right)

        program_l.extend(program_r)
        args_l.extend(args_r)

        return program_l, args_l

    def visitAtom(self, ctx:RegexParser.AtomContext):
        if ctx.expr() == None:
            return [1], [[ctx.getText()]]
        return self.visit(ctx.expr())

    def visitAtomExpr(self, ctx:RegexParser.AtomExprContext):
        return self.visit(ctx.atom())
