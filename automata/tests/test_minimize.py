from ..src.automata import Automaton
from ..src.utils import read_automaton
import pytest


@pytest.mark.parametrize("test_file", ["dfa_notmin.txt", "dfa_min.txt", "dfa_finite.txt", "dfa_even.txt"])
def test_basic(test_file):
    dfa = read_automaton(f"test_data/{test_file}")
    min_dfa = dfa.minimize()
    assert dfa.is_dfa() == True
    assert min_dfa.is_dfa() == True
    assert dfa.sigma == min_dfa.sigma

@pytest.mark.parametrize("test_file", ["dfa_notmin.txt", "dfa_min.txt", "dfa_finite.txt", "dfa_even.txt", "dfa_onlyones.txt"])
@pytest.mark.parametrize("word", ["", "01", "111111101", "11111111111", "10101011010101",
                                  "01", "0", "1", "001", "01",
                                  "1010", "010", "11110000", "00011111"])
def test_min_same_language(test_file, word):
    dfa = read_automaton(f"test_data/{test_file}")
    min_dfa = dfa.minimize()
    assert dfa.accepts(word) == min_dfa.accepts(word)

@pytest.mark.parametrize("test_file", ["dfa_notmin.txt", "dfa_min.txt", "dfa_finite.txt", "dfa_even.txt"])
def test_equal_itself(test_file):
    dfa = read_automaton(f"test_data/{test_file}")
    assert dfa == dfa
    assert dfa == dfa.minimize()

@pytest.mark.parametrize("first", ["dfa_notmin.txt", "dfa_finite.txt", "dfa_even.txt", "dfa_onlyones.txt"])
@pytest.mark.parametrize("second", ["dfa_notmin.txt", "dfa_finite.txt", "dfa_even.txt", "dfa_onlyones.txt"])
def test_unequal(first, second):
    if (first == second):
        return
    fst = read_automaton(f"test_data/{first}")
    snd = read_automaton(f"test_data/{second}")
    assert fst != snd


def test_equal():
    dfa_1 = read_automaton("test_data/dfa_notmin.txt")
    dfa_2 = read_automaton("test_data/dfa_notmin2.txt")
    assert dfa_1 == dfa_2

@pytest.mark.parametrize("test_file", ["dfa_notmin.txt", "dfa_finite.txt", "dfa_even.txt", "dfa_onlyones.txt"])
def test_unequal_sigma(test_file):
    dfa = read_automaton(f"test_data/{test_file}")
    assert not dfa.accepts_all_words()

@pytest.mark.parametrize("test_file", ["dfa_sigma0.txt", "dfa_sigma1.txt"])
def test_equal_sigma(test_file):
    dfa = read_automaton(f"test_data/{test_file}")
    assert dfa.accepts_all_words()
