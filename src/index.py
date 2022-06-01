from services.spellchecker_service import spellchecker_service

def show_commands():
    print()
    print("1 - Add a word to the dictionary")
    print("2 - Search for a word in the dictionary")
    print("3 - Print dictionary")
    print("4 - Calculate Damerau-Levensthein distance")
    print("5 - Check spelling")
    print("6 - Check spelling, recursive")
    print("99 - Quit")
    print()


def main():
    while True:
        show_commands()
        try:
            command = int(input("Choose a command: "))
        except ValueError:
            continue

        if command == 1:
            word = input("Type a word: ")
            if spellchecker_service.add_word(word):
                print(f"\n\"{word}\" was added.")
            else:
                print(f"\n{word} is already in the dictionary.")
        if command == 2:
            word = input("Type word to search for: ")
            if spellchecker_service.find_word(word):
                print(f"\nFound \"{word}\" in the dictionary!")
            else:
                print("\nNo such word in the dictionary.")
        if command == 3:
            words = spellchecker_service.get_all()
            print("\n** Words in the dictionary: **")
            for word in words:
                print(word)
            print()
        if command == 4:
            word_a = input("Type first word: ")
            word_b = input("Type second word: ")
            dist = spellchecker_service.calculate_distance(word_a, word_b)
            print(f"\nThe Demerau-Levenshtein distance between the words is {dist}.")
        if command == 5:
            word = input("Type word to be spell checked: ")
            result = spellchecker_service.find_closest_match(word)
            if result[0] == word:
                print("The word is correctly spelled.")
            else:
                print(f"Did you mean {', ' .join(result)}?")
        if command == 6:
            word = input("Type word to be spell checked: ")
            spellchecker_service.find_closest_match_recursively(word)
        if command == 99:
            break


if __name__ == "__main__":
    main()
