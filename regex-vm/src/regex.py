from enum import Enum

class RegexMachine:
    Instructions: Enum = Enum("Instructions", ["Char", "Match", "Jmp", "Split"])

    def __move(self, dst: int, src: int):
        if (dst >= src):
            for k in range(dst, src, -1):
                self.program[k], self.program[k-1] = self.program[k-1], self.program[k]
                self.args[k], self.args[k-1] = self.args[k-1], self.args[k]
        else:
            for k in range(dst, src):
                self.program[k], self.program[k+1] = self.program[k+1], self.program[k]
                self.args[k], self.args[k+1] = self.args[k+1], self.args[k]


    def print(self):
        print(self.regex)
        for ip in self.program:
            print(ip, " ", self.program[ip].name, " ", *self.args[ip])

    def __init__(self, regex: str):
        self.regex: str = regex
        self.program: dict[int, Instructions] = {}
        self.args: dict[int, list[chr] | list[int]] = {}


        pc = 0
        prev = 0
        for a in self.regex:
            match a:
                case '|':
                    self.program[pc] = self.Instructions.Split
                    self.args[pc] = [1, 2+pc-prev]
                    self.__move(pc, prev)
                    self.program[pc + 1] = self.Instructions.Jmp
                    self.args[pc + 1] = ["end"]
                    pc += 2
                    prev = pc
                case '?':
                    self.program[pc] = self.Instructions.Split
                    self.args[pc] = [1, 2]
                    self.__move(pc, pc - 1)
                    pc += 1
                case '*':
                    self.program[pc] = self.Instructions.Split
                    self.args[pc] = [1, 3]
                    self.__move(pc, pc - 1)
                    self.program[pc + 1] = self.Instructions.Jmp
                    self.args[pc + 1] = [-2]
                    pc += 2
                case '+':
                    self.program[pc] = self.Instructions.Split
                    self.args[pc] = [-1, 1]
                    pc += 1
                case _:
                    self.program[pc] = self.Instructions.Char
                    self.args[pc] = [a]
                    pc += 1  
        self.program[pc] = self.Instructions.Match
        self.args[pc] = []

        for ip in self.program:
            if self.program[ip] == self.Instructions.Jmp:
                if self.args[ip][0] != "end":
                    self.args[ip][0] += ip
                else:
                    self.args[ip][0] = pc
            if self.program[ip] == self.Instructions.Split:
                self.args[ip][0] += ip
                self.args[ip][1] += ip


    def accepts(self, word: str, pc: int = 0, wc: int = 0):
        if pc not in self.program:
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

