from collections import deque
from typing import Self


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
