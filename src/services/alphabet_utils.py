import string

CHAR_COUNT = 26

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

    Only ASCII-letters allowed for now (A-Z, a-z).

    Args:
        string_to_check: The string to check.

    Returns:
      A boolean describing the result of the check. True if all characters are in
      the allowed alphabet, False if any non-alphabet characters were found.
    """

    return all(char in string.ascii_letters for char in string_to_check)

def get_allowed_chars():
    """Returns the allowed characters in the used alphabet.

    Returns:
        A string containing all the allowed characters.
    """

    return string.ascii_letters
