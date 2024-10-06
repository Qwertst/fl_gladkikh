from src.automata import Automaton
from src.utils import read_automaton

DFA = read_automaton("aboba.txt")
min_dfa = DFA.minimize()
min_dfa.to_file("output.txt")

print(DFA == min_dfa)
