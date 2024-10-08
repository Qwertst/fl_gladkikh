from ..src.automata import Automaton
from ..src.utils import read_automaton
import pytest


def test_basic():
    aut = read_automaton("test_data/dfa_finite.txt")
    assert aut.is_dfa() == True


@pytest.mark.parametrize("word, expected", [("12345", True), ("2146342543", False), ("54321", False), ("", False), ("12346", False)])
def test_accepts_simple(word, expected):  # accepts only 12345
    aut = read_automaton("test_data/dfa_finite.txt")
    assert aut.accepts(word) == expected


@pytest.mark.parametrize("word, expected", [("", False), ("1", True), ("111111111", True), ("11011111", False), ("0111111", False)])
def test_accepts_only_ones(word, expected):  # accepts 11*
    aut = read_automaton("test_data/dfa_onlyones.txt")
    assert aut.accepts(word) == expected


@pytest.mark.parametrize("word, expected", [("", True), ("1010", True), ("010", False), ("11110000", True), ("00011111", False)])
# accepts strings with even number of 0's and 1'
def test_accepts_even_numbers(word, expected):
    aut = read_automaton("test_data/dfa_even.txt")
    assert aut.accepts(word) == expected
