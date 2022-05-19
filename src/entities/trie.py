from entities.node import Node, CHAR_COUNT


def calc_index(char: str):
    """Calculates an index number for the given character

    Args:
        char: The character as a string.

    Returns:
        An integer representing the ordinal number of the character
        in the used alphabet.
    """

    return ord(char) - ord("a")

def calc_char(index: int):
    """Calculates the corresponding character from the given integer.

    Args:
        index: The ordinal number in the used alphabet for the character.

    Returns:
        The corresponding character as a string.
    """

    return chr(index + ord("a"))


class Trie:
    """Class describing a trie data structure
    """

    def __init__(self):
        """The class constructor.
        """

        self._root = Node()

    def add(self, key: str):
        """Adds keys to the trie.

        Args:
            key: The key to be added as a string.
        """

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

    def _traverse(self, node, key: str, result: list):
        if node.is_valid_end:
            result.append(key)
        for i in range(CHAR_COUNT):
            child = node.children[i]
            if child:
                self._traverse(child, key+calc_char(i), result)
