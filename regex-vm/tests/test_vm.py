from src.regex import RegexMachine
import pytest
import re


@pytest.mark.parametrize("regex, program, args",
    [
        (
            "a+b*",
            {
                0: RegexMachine.Instructions.Char,
                1: RegexMachine.Instructions.Split,
                2: RegexMachine.Instructions.Split,
                3: RegexMachine.Instructions.Char,
                4: RegexMachine.Instructions.Jmp,
                5: RegexMachine.Instructions.Match
            },
            {
                0: ["a"],
                1: [0, 2],
                2: [3, 5],
                3: ["b"],
                4: [2],
                5: []
            }

        ),
        (
            "a|b|c",
            {
                0: RegexMachine.Instructions.Split,
                1: RegexMachine.Instructions.Char,
                2: RegexMachine.Instructions.Jmp,
                3: RegexMachine.Instructions.Split,
                4: RegexMachine.Instructions.Char,
                5: RegexMachine.Instructions.Jmp,
                6: RegexMachine.Instructions.Char,
                7: RegexMachine.Instructions.Match
            },
            {
                0: [1, 3],
                1: ["a"],
                2: [7],
                3: [4, 6],
                4: ["b"],
                5: [7],
                6: ["c"],
                7: []
            }

        ),
        (
            "a+b?|c*",
            {
                0: RegexMachine.Instructions.Split,
                1: RegexMachine.Instructions.Char,
                2: RegexMachine.Instructions.Split,
                3: RegexMachine.Instructions.Split,
                4: RegexMachine.Instructions.Char,
                5: RegexMachine.Instructions.Jmp,
                6: RegexMachine.Instructions.Split,
                7: RegexMachine.Instructions.Char,
                8: RegexMachine.Instructions.Jmp,
                9: RegexMachine.Instructions.Match
            },
            {
                0: [1, 6],
                1: ["a"],
                2: [1, 3],
                3: [4, 5],
                4: ["b"],
                5: [9],
                6: [7, 9],
                7: ["c"],
                8: [6],
                9: []
            }

        )            
    ])
def test_parse(regex, program, args):
    VM = RegexMachine(regex)
    assert VM.program == program
    assert VM.args == args

    

@pytest.mark.parametrize("regex, true_regex", [("",""), ("aboba","aboba"), ("a+b+","a+b+"), ("a|b|c","a|b|c"), ("a+|b?|c*d","(a+)|(b?)|(c*d)"), ("ab?", "ab?"), ("a*b", "a*b"), ("ab+","ab+"), ("a+b?|c*", "(a+b?)|(c*)")])
@pytest.mark.parametrize("word", ["", "aboba", "aaaab", "a", "b", "c", "bb", "cccccccccd", "ab", "abbbbbbb", "aaaaaaa", "ccccccc"])
def test_accepts(regex, true_regex, word):
    VM = RegexMachine(regex)
    assert VM.accepts(word) == (re.fullmatch(true_regex, word) != None)
