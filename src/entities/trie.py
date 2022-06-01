from entities.node import Node
from services.alphabet_utils import(
    CHAR_COUNT,
    calc_char,
    calc_index
)


class Trie:
    """Class describing a trie data structure
    """

    def __init__(self):
        """The class constructor.
        """

        self._root = Node()
        self._max_keylength = 0

    def add(self, key: str):
        """Adds keys to the trie.

        Args:
            key: The key to be added as a string.
        """

        if len(key) > self._max_keylength:
            self._max_keylength = len(key)

        node = self._root

        for char in key.lower():
            index = calc_index(char)
            if not node.children[index]:
                child = Node()
                node.children[index] = child
            node = node.children[index]

        node.is_valid_end = True

    def find(self, key: str):
        """Searches for the given key in the trie

        Args:
            key: The string to be searched for.

        Returns:
            True if the key was found, otherwise False.
        """

        node = self._root

        for char in key.lower():
            index = calc_index(char)
            if node.children[index]:
                node = node.children[index]
            else:
                return False

        return node.is_valid_end

    def get_all(self):
        """Returns all keys in the trie

        Returns:
            A list containing all keys
        """

        keys = []
        self._traverse(self._root, "", keys)
        return keys

    def get_root(self):
        """Returns the root node of the trie.

        Returns:
            The root node as a Node-object.
        """

        return self._root

    def get_max_keylength(self):
        """Returns the length of the longest key in the trie.

        Returns:
            The length of the longest key as an integer.
        """

        return self._max_keylength

    def _traverse(self, node, key: str, result: list):
        if node.is_valid_end:
            result.append(key)
        for i in range(CHAR_COUNT):
            child = node.children[i]
            if child:
                self._traverse(child, key+calc_char(i), result)
