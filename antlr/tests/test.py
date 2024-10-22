from ..src.regex import RegexMachine
import pytest
import re


@pytest.mark.parametrize("regex, program, args",
                         [
                             (
                                 "a+b*",
                                 [
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Jmp,
                                     RegexMachine.Instructions.Match
                                 ],
                                 [
                                     ["a"],
                                     [0, 2],
                                     [3, 5],
                                     ["b"],
                                     [2],
                                     []
                                 ]

                             ),
                             (
                                 "a|(b|c)",
                                 [
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Jmp,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Jmp,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Match
                                 ],
                                 [
                                     [1, 3],
                                     ["a"],
                                     [7],
                                     [4, 6],
                                     ["b"],
                                     [7],
                                     ["c"],
                                     []
                                 ]

                             ),
                             (
                                 "(a+b?)|c*",
                                 [
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Jmp,
                                     RegexMachine.Instructions.Split,
                                     RegexMachine.Instructions.Char,
                                     RegexMachine.Instructions.Jmp,
                                     RegexMachine.Instructions.Match
                                 ],
                                 [
                                     [1, 6],
                                     ["a"],
                                     [1, 3],
                                     [4, 5],
                                     ["b"],
                                     [9],
                                     [7, 9],
                                     ["c"],
                                     [6],
                                     []
                                 ]

                             )
                         ])
def test_parse(regex, program, args):
    VM = RegexMachine(regex)
    assert VM.program == program
    assert VM.args == args


@pytest.mark.parametrize("regex, true_regex", [("aboba", "aboba"), ("a+b+", "a+b+"), ("a|b|c", "a|b|c"), ("(a+)|(b?)|(c*d)", "(a+)|(b?)|(c*d)"), ("ab?", "ab?"), ("a*b", "a*b"), ("ab+", "ab+"), ("(a+b?)|(c*)", "(a+b?)|(c*)"), ("(a|b)", "(a|b)"), ("a+|b?|a*b", "a+|b?|a*b")])
@pytest.mark.parametrize("word", ["", "aboba", "aaaab", "a", "b", "c", "bb", "cccccccccd", "ab", "abbbbbbb", "aaaaaaa", "ccccccc", "baba", "bbbaa"])
def test_accepts(regex, true_regex, word):
    VM = RegexMachine(regex)
    assert VM.accepts(word) == (re.fullmatch(true_regex, word) != None)


@pytest.mark.parametrize("regex", ["())", "((z)", "z)", "abc(", "?abc?"])
def test_validation(regex):
    with pytest.raises(RuntimeError):
        VM = RegexMachine(regex)
