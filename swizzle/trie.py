class TrieNode:
    __slots__ = "children", "is_end"

    def __init__(self):
        self.children = {}
        self.is_end = False

    def add(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def step(self, char):
        return self.children.get(char)


class Trie:
    def __init__(self, words=None, sep=""):
        self.root = TrieNode()
        self.sep = sep
        self.sep_len = len(sep)
        if words:
            for word in words:
                self.add(word)

    def add(self, word):
        self.root.add(word)

    def split_longest_prefix(self, query):
        length = len(query)
        i = 0
        while i < length:
            node = self.root
            longest_end = -1
            if i and self.sep_len:
                if query.startswith(self.sep, i):
                    i += self.sep_len
                    if i == length:
                        raise AttributeError(
                            f"Seperator can not be at the end of the string: {query}"
                        )
                else:
                    raise AttributeError(
                        f"Expected separator '{self.sep}' at pos {i} in "
                        f"'{query}', found '{query[i : i + self.sep_len]}'"
                    )
            j = i
            children = node.children  # cache children dict
            while j < length:
                next_node = children.get(query[j])
                if not next_node:
                    break
                node = next_node
                children = node.children  # update cache
                j += 1
                if node.is_end:
                    longest_end = j
            if longest_end == -1:
                raise AttributeError(
                    f"No matching attribute found for substring: {query[i:]} at pos {i}"
                )
            yield query[i:longest_end]
            i = longest_end
