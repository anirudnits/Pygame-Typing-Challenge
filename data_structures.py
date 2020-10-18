from collections import deque
from typing import List


def fast_power(a: int, b: int, mod: int):
    power = 1

    while b:
        if b & 1:
            power = (power * a) % mod

        a = (a * a) % mod
        b >>= 1

    return power


class trie_node(object):
    def __init__(self):
        self.node = {}
        self.end_of_word = False
        self.end_index = -1


class Trie(object):
    def __init__(self, word_list: List[str]):
        self.head = trie_node()
        self.curr = [self.head]

        for index, word in enumerate(word_list):
            self._insert(word, index)

    def _insert(self, word: str, index: int) -> None:
        temp = self.head

        for ch in word:
            if ch not in temp.node:
                temp.node[ch] = trie_node()

            temp = temp.node[ch]

        temp.end_of_word = True
        temp.end_index = index

    def _search_character(self, ch: chr) -> int:
        if ch not in self.curr[-1].node:
            self.curr.append(trie_node())
            return -1

        self.curr.append(self.curr[-1].node[ch])

        if self.curr[-1].end_of_word:
            ret_index = self.curr[-1].end_index
            self.curr = [self.head]
            return ret_index

        return -1

    def pop_node(self) -> None:
        if len(self.curr) > 1:
            self.curr.pop(-1)


class Rolling_hash(object):
    def __init__(self, word_list: List[str]):
        self.BASE = 257
        self.mod = 1000446217
        self.word_list = word_list

        # contains (BASE^n)%mod in an array of length n
        self.p_b = [1]
        for _ in range(1000):
            self.p_b.append((self.p_b[-1] * self.BASE) % self.mod)

        # two deques to store character to left and right of cursor position
        self.left_deque = deque()
        self.right_deque = deque()

        self.left_hash = 0
        self.right_hash = 0

        # store the word hashes in a dict
        # with hash value as key and index as value
        self.hash_dict = {}
        for word_index, word in enumerate(word_list):
            hash_value = 0

            for index, ch in enumerate(word):
                hash_value = (
                    hash_value + ord(ch) * self.p_b[index]
                ) % self.mod

            self.hash_dict[hash_value] = word_index

    def mod_sub(self, a: int, b: int) -> int:
        return (a - b + self.mod) % self.mod

    def mod_inverse(self, a: int) -> int:
        return fast_power(a, self.mod - 2, self.mod)

    def mod_div(self, a: int, b: int) -> int:
        return (a * self.mod_inverse(b)) % self.mod

    def _check(self) -> int:
        adjusted_right_hash = (
            self.right_hash * self.p_b[len(self.left_deque)]
        ) % self.mod
        total_hash = (self.left_hash + adjusted_right_hash) % self.mod

        if total_hash in self.hash_dict:
            # if string hash is present in self.hash_dict
            # then check the entire string

            r = "".join(self.left_deque) + "".join(self.right_deque)
            word_list_index = self.hash_dict[total_hash]

            if self.word_list[word_list_index] == r:
                self.right_deque.clear()
                self.left_deque.clear()
                self.right_hash = 0
                self.left_hash = 0

                return word_list_index

        return -1

    def add_character(self, ch: str) -> int:
        added_value = (ord(ch) * self.p_b[len(self.left_deque)]) % self.mod

        self.left_hash = (self.left_hash + added_value) % self.mod

        self.left_deque.append(ch)

        return self._check()

    def add_backspace(self) -> int:
        if not self.left_deque:
            return -1

        ch = self.left_deque.pop()

        hash_value_of_ch = (
            ord(ch) * self.p_b[len(self.left_deque)]
        ) % self.mod

        self.left_hash = self.mod_sub(self.left_hash, hash_value_of_ch)

        return self._check()

    def add_right_movement(self) -> None:
        if not self.right_deque:
            return

        # pop element from the right deque and recalucate right hash
        ch = self.right_deque.popleft()

        self.right_hash = self.mod_sub(self.right_hash, ord(ch))

        self.right_hash = self.mod_div(
            self.right_hash, self.BASE
        )

        # push element into the left deque and recalculate left hash
        added_value = (ord(ch) * self.p_b[len(self.left_deque)]) % self.mod

        self.left_hash = (self.left_hash + added_value) % self.mod

        self.left_deque.append(ch)

    def add_left_movement(self) -> None:
        if not self.left_deque:
            return

        # pop element from the left deque and recalculate left hash
        ch = self.left_deque.pop()

        hash_value_of_ch = (
            ord(ch) * self.p_b[len(self.left_deque)]
        ) % self.mod
        self.left_hash = self.mod_sub(self.left_hash, hash_value_of_ch)

        # push element to the right deque and recalculate right hash

        self.right_hash = (ord(ch) + self.right_hash * self.BASE) % self.mod

        self.right_deque.appendleft(ch)
