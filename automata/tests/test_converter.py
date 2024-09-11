from src.automata import Automaton
from src.utils import read_automaton
import pytest


def test_basic():
    aut = read_automaton("test_data/nfa_01ending.txt")
    aut_dfa = aut.get_dfa()
    assert aut.is_dfa() == False
    assert aut_dfa.is_dfa() == True
    assert aut.sigma == aut_dfa.sigma


@pytest.mark.parametrize("test_file", ["nfa_01ending.txt", "nfa_twostarts.txt", "dfa_onlyones.txt"])
@pytest.mark.parametrize("word", ["", "01", "111111101", "11111111111", "10101011010101",
                                  "01", "0", "1", "001", "01",
                                  "1010", "010", "11110000", "00011111"])
def test_to_dfa(test_file, word):
    aut = read_automaton(f"test_data/{test_file}")
    aut_dfa = aut.get_dfa()
    assert aut.accepts(word) == aut_dfa.accepts(word)
