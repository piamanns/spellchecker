import string

CHAR_COUNT = 26
NEIGHBOURING_KEYS = {
    "a": ["q", "w", "s", "z"],
    "b": ["v", "g", "h", "n"],
    "c": ["x", "d", "f", "v"],
    "d": ["s", "e", "r", "f", "c", "x"],
    "e": ["w", "r", "d", "s"],
    "f": ["d", "r", "t", "g", "v", "c"],
    "g": ["f", "t", "y", "h", "b", "v"],
    "h": ["g", "y", "u", "j", "n", "b"],
    "i": ["u", "o", "l", "k", "j"],
    "j": ["h", "u", "i", "k", "m", "n"],
    "k": ["j", "i", "o", "l", "m"],
    "l": ["k", "o", "p"],
    "m": ["n", "j", "k"],
    "n": ["b", "h", "j", "m"],
    "o": ["i", "p", "l", "k"],
    "p": ["o", "l"],
    "q": ["w", "a"],
    "r": ["e", "t", "f", "d"],
    "s": ["a", "w", "e", "d", "x", "z"],
    "t": ["r", "y", "g", "f"],
    "u": ["y", "i", "h", "j"],
    "v": ["c", "f", "g", "b"],
    "w": ["q", "e", "s", "a"],
    "x": ["z", "s", "d", "c"],
    "y": ["t", "u", "h", "g"],
    "z": ["a", "s", "x"]
}

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

def check_allowed_chars(string_to_check: str):
    """Checks if all characters in a given string are in the allowed alphabet.

    Only lowercase ASCII-letters allowed for now (a-z).

    Args:
        string_to_check: The string to check.

    Returns:
      A boolean describing the result of the check. True if all characters are in
      the allowed alphabet, False if any non-alphabet characters were found.
    """

    return all(char in string.ascii_lowercase for char in string_to_check)

def get_allowed_chars():
    """Returns the allowed characters in the used alphabet.

    Returns:
        A string containing all the allowed characters.
    """

    return string.ascii_lowercase
