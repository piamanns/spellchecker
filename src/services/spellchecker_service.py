from entities.trie import Trie
from repositories.wordlist_repository import wordlist_repository
from services.distance_service import calculate_dl_distance


class SpellcheckerService:
    """ Class responsible for the app logic.
    """

    def __init__(self):
        """ The class constructor.
        """
        self._dictionary = Trie()
        self._wordlist = []
        self.load_wordlist()

    def load_wordlist(self):
        """ Loads a wordlist from file on disk and creates a trie dictionary.
        """

        wordlist = wordlist_repository.get_wordlist()
        for word in wordlist:
            self._dictionary.add(word)

    def add_word(self, word: str):
        """ Adds a new word to the dictionary and the wordlist file.

        Args:
            word: The word to be added as a string.

        Returns:
            True if the operation was carried out (i.e. the word was not already
            present in the wordlist), False if the word was already found in the
            wordlist.
        """

        if not self._dictionary.find(word):
            new_word = wordlist_repository.add(word)
            self._dictionary.add(new_word)
            return True
        return False

    def find_word(self, word: str):
        """ Checks if the word exists in the dictionary.

        Args:
            word: The word to look for as a string.

        Returns:
            True if the word was found, False otherwise.
        """

        return self._dictionary.find(word)

    def find_closest_match(self, word:str):
        """ Find closest match in the dictionary for the given word.

        Args:
            word: The word to be matched.

        Returns:
            A string describing the result of the search. If the
            given word was not found in the dictionary a list of
            candidate words with the lowest Damerau-Lewenshtein distance
            is included.
        """

        if self.find_word(word):
            return "The word is spelled correctly."
        suggestions = []
        wordlist = self.get_all()
        min_dist = max(len(word), len(wordlist[0]))
        for dict_word in wordlist:
            dl_dist = calculate_dl_distance(word, dict_word)
            if dl_dist <= min_dist:
                if dl_dist < min_dist:
                    suggestions.clear()
                    min_dist = dl_dist
                suggestions.append(f"{dict_word}({dl_dist})")
        result = ", ".join(suggestions)
        return f"Did you mean {result}?"

    def get_all(self):
        """ Returns all words in the dictionary as a list.

        Returns:
            A list containing all the words in the dictionary as strings.
        """

        return self._dictionary.get_all()

    def delete_all(self):
        """ Clears the dictionary and deletes the content in the wordlist file.
        """

        self._dictionary = Trie()
        wordlist_repository.delete_all()

    def calculate_distance(self, word_a: str, word_b: str):
        return calculate_dl_distance(word_a, word_b)


spellchecker_service = SpellcheckerService()
