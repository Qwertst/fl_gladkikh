from src.automata import Automaton
from src.utils import read_automaton

NFA = read_automaton("test_data/nfa_twostarts.txt")
DFA = NFA.get_dfa()
DFA.to_file("output.txt")
