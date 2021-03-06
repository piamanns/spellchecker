""" Module for the command line user interface.
"""

from services.spellchecker_service import spellchecker_service
from services.alphabet_utils import check_allowed_chars, get_allowed_chars


def show_commands():
    print()
    print("1 - Add a word to the dictionary")
    print("2 - Search for a word in the dictionary")
    print("3 - Print dictionary")
    print("4 - Calculate Damerau-Levensthein distance")
    print("5 - Check spelling (baseline for-loop)")
    print("6 - Check spelling (recursive)")
    print("0 - Quit")
    print()


def input_word(prompt: str):
    while True:
        word = input(prompt)
        if check_allowed_chars(word):
            return word
        print(f"\nOnly the characters '{get_allowed_chars()}'\nare allowed. Try again!\n")

def input_yes_no(prompt: str):
    answer = input(prompt)
    return answer == "y"

def add_word():
    word = input_word("Type a word: ")
    if spellchecker_service.add_word(word):
        print(f"\n'{word}' was added.")
    else:
        print(f"\n'{word}' is already in the dictionary.")

def find_word():
    word = input_word("Type word to search for: ")
    if spellchecker_service.find_word(word):
        print(f"\nFound '{word}' in the dictionary!")
    else:
        print("\nNo such word in the dictionary.")

def get_all():
    words = spellchecker_service.get_all()
    print("\n*** Words in the dictionary: ***")
    for word in words:
        print(word)
    print()

def calculate_distance():
    word_a = input_word("Type first word: ")
    word_b = input_word("Type second word: ")
    neighbour_check = input_yes_no("Adjust for neighbouring keys? (y/n): ")
    matrix = spellchecker_service.calculate_distance(word_a, word_b, neighbour_check, True)
    print_matrix(matrix)
    print(f"\nThe Demerau-Levenshtein distance between the words is {matrix[-1][-1]}.")

def check_spelling(method: str):
    word = input_word("Type word to be spell checked: ")
    try:
        max_edit = int(input(
            "Enter maximum edit distance (empty for unrestricted): "
        ))
    except ValueError:
        max_edit = None

    neighbour_check = input_yes_no("Prioritise words with neighbouring keys? (y/n): ")

    result = []
    if method == "recursive":
        result = spellchecker_service.find_closest_match_recursively(
                 word, max_edit, neighbour_check
        )
    else:
        result = spellchecker_service.find_closest_match(word, max_edit, neighbour_check)

    if len(result) == 0:
        print("No suggestions for correct spelling were found.")
    elif result[0] == word:
        print("The word is correctly spelled.")
    else:
        print(f"Did you mean {', ' .join(result)}?")
        print(spellchecker_service.get_info())

def print_matrix(matrix):
    print()
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            print(f"{matrix[row][col]:2} | ", end="")
        print()

def main():
    dispatcher = {
        1: add_word,
        2: find_word,
        3: get_all,
        4: calculate_distance,
        5: lambda: check_spelling(None),
        6: lambda: check_spelling("recursive")
    }

    while True:
        show_commands()
        try:
            command = int(input("Choose a command: "))
        except ValueError:
            command = None

        if command == 0:
            break
        if command and command in dispatcher:
            dispatcher[command]()
        else:
            print("No such command.\nTry again!")


if __name__ == "__main__":
    main()
