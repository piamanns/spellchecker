from entities.trie import Trie
from repositories.wordlist_repository import wordlist_repository

def show_commands():
    print()
    print("0 - Load wordlist")
    print("1 - Add a word to the dictionary")
    print("2 - Search for a word in the dictionary")
    print("3 - Print dictionary")
    print("4 - Quit")
    print()

def main():
    dictionary = Trie()
    wordlist = []

    while True:
        show_commands()
        try:
            command = int(input("Choose a command: "))
        except ValueError:
            continue
        if command == 0:
            wordlist = wordlist_repository.get_wordlist()
            for word in wordlist:
                dictionary.add(word)
        if command == 1:
            word = input("Type a word: ")
            if dictionary.find(word):
                print(f"\n{word} is already in the dictionary.")
            else:
                dictionary.add(word)
                added = wordlist_repository.add(word)
                print(f"\n\"{added}\" was added.")
        if command == 2:
            word = input("Type word to search for: ")
            result = dictionary.find(word)
            if result:
                print(f"\nFound \"{word}\" in the dictionary!")
            else:
                print("\nNo such word in the dictionary.")
        if command == 3:
            words = dictionary.get_all()
            print("\n** Words in the dictionary: **")
            for word in words:
                print(word)
            print()
        if command == 4:
            break


if __name__ == "__main__":
    main()
