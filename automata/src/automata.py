from collections import deque
from typing import Self, List
from itertools import permutations


class Automaton:
    sigma: set[int]
    states: set[int]
    initial_states: set[int]
    accepting_states: set[int]
    transition_function: dict[int, dict[int, set[int]]]

    def __init__(
        self,
        sigma: set[int],
        states: set[int],
        initial_states: set[int],
        accepting_states: set[int],
        transition_function: dict[int, dict[int, set[int]]]
    ):
        self.sigma = sigma
        self.states = states
        self.initial_states = initial_states
        self.accepting_states = accepting_states
        self.transition_function = transition_function

    def to_file(self, file_name: str) -> None:
        with open(file_name, "w") as f:
            f.write(f"{len(self.states)}\n")
            f.write(f"{len(self.sigma)}\n")
            f.write(f"{(" ").join(map(str, self.initial_states))}\n")
            f.write(f"{(" ").join(map(str, self.accepting_states))}\n")
            for src in self.transition_function:
                for edge in self.transition_function[src]:
                    for dst in self.transition_function[src][edge]:
                        f.write(f"{src} {edge} {dst}\n")

    def accepts(self, word: str) -> bool:
        que: deque[tuple[int, int]] = deque()
        que.extend((s, 0) for s in self.initial_states)

        n = len(word)
        is_final_reached = False
        while que and not is_final_reached:
            state, it = que.popleft()
            if state in self.accepting_states and it == n:
                is_final_reached = True
                break
            if it == n:
                continue
            next_char = int(word[it])
            if state in self.transition_function and next_char in self.transition_function[
                    state]:
                que.extend((s, it + 1)
                           for s in self.transition_function[state][next_char])
        return is_final_reached

    def __get_useless_states(self) -> set[int]:
        que: deque[int] = deque()
        useless: set[int] = self.states.copy()

        que.extend(self.initial_states)
        while que:
            state = que.popleft()
            if state in useless:
                useless.remove(state)
                if state in self.transition_function:
                    for edge in self.transition_function[state]:
                        for next_state in self.transition_function[state][edge]:
                            if next_state in useless:
                                que.append(next_state)

        que.extend(self.accepting_states)
        while que:
            state = que.popleft()
            if state in useless:
                useless.remove(state)
                for next_state in self.transition_function:
                    for edge in self.transition_function[state]:
                        if state in self.transition_function[next_state][edge]:
                            que.append(next_state)
        return useless

    def is_dfa(self) -> bool:
        flag: bool = True
        flag &= len(self.initial_states) == 1

        for src in self.transition_function:
            for edge in self.transition_function[src]:
                flag &= len(self.transition_function[src][edge]) == 1

        return flag

    def get_dfa(self) -> Self:
        useless_states: set[int] = self.__get_useless_states()

        new_sigma: set[int] = self.sigma.copy()
        new_initial_states: set[int] = set([0])
        new_accepting_states: set[int] = set()
        new_transition_function: dict[int, dict[int, set[int]]] = {}

        new_initial_state = frozenset(
            st for st in self.initial_states - useless_states)

        que: deque[tuple[frozenset[int], int]] = deque()
        que.append((new_initial_state, 0))

        new_id: dict[frozenset[int], int] = {new_initial_state: 0}
        id_counter = 1

        while que:
            src, src_id = que.popleft()

            for state in src:
                if state in self.accepting_states:
                    new_accepting_states.add(src_id)

            for edge in new_sigma:
                dst: set[int] | frozenset[int] = set()
                for state in src:
                    if state in self.transition_function and edge in self.transition_function[
                            state]:
                        dst |= self.transition_function[state][edge]
                dst -= useless_states
                if dst:
                    dst = frozenset(dst)
                    was_processed: bool = False
                    if dst not in new_id:
                        new_id[dst] = id_counter
                        id_counter += 1
                    else:
                        was_processed = True
                    if src_id not in new_transition_function:
                        new_transition_function[src_id] = {}
                    if edge not in new_transition_function[src_id]:
                        new_transition_function[src_id][edge] = set()
                    new_transition_function[src_id][edge].add(new_id[dst])
                    if not was_processed and src_id != new_id[dst]:
                        que.append((dst, new_id[dst]))
        new_states = set(i for i in range(id_counter))

        return Automaton(new_sigma, new_states, new_initial_states,
                         new_accepting_states, new_transition_function)

    def minimize(self) -> Self:
        assert (self.is_dfa())

        usefull_states: List[int] = list(
            self.states - self.__get_useless_states())
        states_size: int = len(usefull_states)
        distinguishable: List[List[int]] = [
            [-2]*states_size for i in range(states_size)]

        for i in range(states_size):
            for j in range(i+1, states_size):
                if usefull_states[i] in self.accepting_states and usefull_states[j] not in self.accepting_states:
                    distinguishable[i][j] = -1
                    distinguishable[j][i] = -1
                if usefull_states[i] not in self.accepting_states and usefull_states[j] in self.accepting_states:
                    distinguishable[i][j] = -1
                    distinguishable[j][i] = -1

        while True:
            is_changed: bool = False
            for i in range(states_size):
                for j in range(i+1, states_size):
                    for a in self.sigma:
                        if usefull_states[i] not in self.transition_function or \
                                usefull_states[j] not in self.transition_function:
                            continue
                        if a not in self.transition_function[usefull_states[i]] or \
                                a not in self.transition_function[usefull_states[j]]:
                            continue
                        delta_i_a = list(
                            self.transition_function[usefull_states[i]][a])[0]
                        delta_j_a = list(
                            self.transition_function[usefull_states[j]][a])[0]
                        if distinguishable[i][j] == -2 and distinguishable[delta_i_a][delta_j_a] != -2:
                            distinguishable[i][j] = a
                            distinguishable[j][i] = a
                            is_changed = True

            if not is_changed:
                break

        new_states_id: dict[int, int] = {}
        id_counter: int = 0
        for i in range(states_size):
            p: int = usefull_states[i]
            if p not in new_states_id:
                new_states_id[p] = id_counter
                id_counter += 1
            for j in range(i+1, states_size):
                q: int = usefull_states[j]
                if distinguishable[i][j] == -2:
                    new_states_id[q] = new_states_id[p]

        new_transition_function: dict[int, dict[int, set[int]]] = {}
        for src in self.transition_function:
            new_id = new_states_id[src]
            if new_id not in new_transition_function:
                new_transition_function[new_id] = {}
            for edge in self.transition_function[src]:
                if edge not in new_transition_function[new_id]:
                    new_transition_function[new_id][edge] = set()
                new_transition_function[new_id][edge] |= set(
                    [new_states_id[q] for q in self.transition_function[src][edge]])

        new_states = set([i for i in range(id_counter)])
        new_initial_state = set([new_states_id[q]
                                for q in self.initial_states])
        new_accepting_states = set([
            new_states_id[q] for q in self.accepting_states])

        return Automaton(self.sigma.copy(), new_states,
                         new_initial_state, new_accepting_states, new_transition_function)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Automaton):
            return False
        min_self: Self = self.get_dfa().minimize()
        min_other: Self = other.get_dfa().minimize()

        if min_self.sigma != min_other.sigma:
            return False

        if len(min_self.states) != len(min_other.states):
            return False

        if len(min_self.accepting_states) != len(min_other.accepting_states):
            return False

        if len(min_self.transition_function) != len(min_other.transition_function):
            return False

        state_size = len(min_self.states)
        perm = [-1] * state_size
        perm_inv = [-1] * state_size
        queue_self: Deque[int] = deque([list(min_self.initial_states)[0]])
        queue_other: Deque[int] = deque([list(min_other.initial_states)[0]])

        while queue_self and queue_other:
            q_self = queue_self.popleft()
            q_other = queue_other.popleft()
            perm[q_self] = q_other
            perm_inv[q_other] = q_self
            if (q_self in min_self.transition_function) != (q_other in min_other.transition_function):
                return False
            if q_self not in min_self.transition_function:
                continue
            if min_self.transition_function[q_self].keys() != min_other.transition_function[q_other].keys():
                return False
            for edge in min_self.transition_function[q_self]:
                dst_self = list(min_self.transition_function[q_self][edge])[0]
                dst_other = list(
                    min_other.transition_function[q_other][edge])[0]
                if (perm[dst_self] == -1) != (perm_inv[dst_other] == -1):
                    return False
                if perm[dst_other] not in [-1, dst_other]:
                    return False

                if (perm[dst_self] == -1):
                    queue_self.append(dst_self)
                    queue_other.append(dst_other)

        return not (queue_self or queue_other)

    @staticmethod
    def get_sigma_star(sigma: set[int]) -> Self:
        states = set([0])
        initial_states = set([0])
        accepting_states = set([0])
        transition_function = {0: {i: set([0]) for i in sigma}}
        return Automaton(sigma.copy(), states, initial_states, accepting_states, transition_function)

    def accepts_all_words(self) -> bool:
        Sigma_star: Self = self.get_sigma_star(self.sigma)
        return self == Sigma_star
