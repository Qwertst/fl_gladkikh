from .automata import Automaton


def read_automaton(file_name: str) -> Automaton:
    with open(file_name, 'r') as f:
        states_number = int(f.readline())
        states = set(i for i in range(states_number))
        sigma_cardinality = int(f.readline())
        sigma = set(i for i in range(sigma_cardinality))
        initial_states = set(map(int, f.readline().split()))
        accepting_states = set(map(int, f.readline().split()))
        transition_function: dict[int, dict[int, set[int]]] = {}
        for line in f:
            src, edge, dst = list(map(int, line.split()))
            if src in transition_function:
                if edge in transition_function[src]:
                    transition_function[src][edge].add(dst)
                else:
                    transition_function[src][edge] = set([dst])
            else:
                transition_function[src] = {edge: set([dst])}
        return Automaton(sigma, states, initial_states, accepting_states, transition_function)
