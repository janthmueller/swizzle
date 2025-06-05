class TrieNode:
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
    def __init__(self, words=None):
        self.root = TrieNode()
        if words:
            for word in words:
                self.add(word)

    def add(self, word):
        self.root.add(word)

    def split_longest_prefix(self, query):
        result = []
        length = len(query)
        i = 0
        while i < length:
            node = self.root
            longest_end = -1
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
                return None
            result.append(query[i:longest_end])
            i = longest_end
        return result


if __name__ == "__main__":
    words = ["mango", "man", "go", "bat", "manbat"]
    trie = Trie(words)

    print(trie.split_longest_prefix("mangomanmanbat"))  # ['mango', 'man', 'bat']
    print(trie.split_longest_prefix("manbat"))  # ['manbat']
    print(trie.split_longest_prefix("mango"))  # ['mango']
    print(trie.split_longest_prefix("mangoman"))  # ['mango', 'man']
    print(trie.split_longest_prefix("unknownword"))  # None
