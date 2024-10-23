from ..src.automata import Automaton
from ..src.utils import read_automaton
import pytest

def test_basic():
    aut = read_automaton("test_data/nfa_01ending.txt")
    assert aut.is_dfa() == False

@pytest.mark.parametrize("word, expected", [("", False), ("01", True), ("111111101", True), ("11111111111", False), ("10101011010101", True)])
def test_accepts_simple(word, expected):
    aut = read_automaton("test_data/nfa_01ending.txt")
    assert aut.accepts(word) == expected

@pytest.mark.parametrize("word, expected", [("", True), ("01", True), ("0", False), ("1", True), ("001", True)])
def test_accepts_multiple_starts(word, expected):
    aut = read_automaton("test_data/nfa_twostarts.txt")
    assert aut.accepts(word) == expected    
