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
