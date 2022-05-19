from entities.trie import Trie

def show_commands():
    print("1 - Add a word to the dictionary")
    print("2 - Search for a word in the dictionary")
    print("3 - Print dictionary")
    print("4 - Quit")
    print()


def main():
    dictionary = Trie()

    while True:
        show_commands()
        try:
            command = int(input("Choose a command: "))
        except ValueError:
            continue
        if command == 1:
            word = input("Type a word: ")
            dictionary.add(word)
            print(f"\"{word}\" was added.\n")
        if command == 2:
            word = input("Type word to search for: ")
            result = dictionary.find(word)
            if result:
                print(f"The word \"{word}\" was found in the dictionary.\n")
            else:
                print("No such word in the dictionary.\n")
        if command == 3:
            words = dictionary.get_all()
            print("\n* Words in the dictionary: *")
            for word in words:
                print(word)
            print()
        if command == 4:
            break


if __name__ == "__main__":
    main()
