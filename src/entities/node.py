from services.alphabet_utils import CHAR_COUNT


class Node:
    """A class representing a node in a Trie data structure

    Attributes:
        is_valid_end: A boolean describing if the node is a valid ending
                      for a word.
        children: A list with cells containing nodes representing the possible
                  next characters in a string. The indices of the cells
                  correspond to the running order of the characters
                  in the used alphabet, where the first character in the alphabet
                  has the index 0.
    """

    def __init__(self):
        """ The class constructor.
        """

        self.is_valid_end = False
        self.children = [None] * CHAR_COUNT
