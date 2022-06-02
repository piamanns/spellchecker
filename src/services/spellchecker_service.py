from time import perf_counter
from entities.trie import Trie
from repositories.wordlist_repository import wordlist_repository
from services.distance_service import calculate_dl_distance
from services.distance_service_recursive import calculate_dl_distance_recursive


class SpellcheckerService:
    """ Class responsible for the app logic.
    """

    def __init__(self):
        """ The class constructor.
        """
        self._dictionary = Trie()
        self._latest_search_time = 0
        self._max_edit = None
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

    def calculate_distance(self, word_a: str, word_b: str):
        """ Calculates the Damerau-Lewenshtein distance between two words.

        Args:
            word_a: The source word as a string.
            word_b: The target word as a string,

        Returns:
            The Damerau-Lewnshtein distance as an integer.
        """

        return calculate_dl_distance(word_a, word_b)

    def find_closest_match(self, word:str, max_edit=None):
        """ Finds closest matching words in the dictionary for the given word.

        Args:
            word: The word to be matched.

        Returns:
            A list of candidate words with the lowest Damerau-Lewenshtein
            distance to the given word. If the word itself was found in the
            dictionary (i.e. was correctly spelled) the list contains
            only the word itself.
        """
        if max_edit:
            self._max_edit = max_edit

        if self.find_word(word):
            return [word]

        start = perf_counter()

        candidates = []
        wordlist = self.get_all()
        min_dist = max(len(word), len(wordlist[0]))
        for dict_word in wordlist:
            if max_edit and abs(len(word)-len(dict_word)) > max_edit:
                continue
            dl_dist = calculate_dl_distance(word, dict_word)
            if dl_dist <= min_dist:
                if dl_dist < min_dist:
                    candidates.clear()
                    min_dist = dl_dist
                candidates.append(f"{dict_word}({dl_dist})")

        end = perf_counter()
        self._latest_search_time = end-start

        return candidates

    def find_closest_match_recursively(self, word: str, max_edit=None):
        """ Finds closest matching words in the dictionary for the given word.

        The search utilizes a recursive traversal of the trie for
        faster perfomance.

        Args:
            word: The word to be matched.

        Returns:
            Returns:
            A list of candidate words with the lowest Damerau-Lewenshtein
            distance to the given word. If the word itself was found in the
            dictionary (i.e. was correctly spelled) the list contains
            only the word itself.
        """

        if self.find_word(word):
            return [word]

        start = perf_counter()

        candidates = calculate_dl_distance_recursive(word, self._dictionary, max_edit)

        end = perf_counter()
        self._latest_search_time = end-start

        return candidates

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

    def get_info(self):
        """ Returns information about the setup and performance
        of the spellchecker.

        Returns:
          A string containing
          - the time used for the latest search in the dictionary
          for correctly spelled words with a low edit distance
          to the given word
          -  the size of the dictionary (number of words)
        """

        return (
            f"\nSearch took {self._latest_search_time} seconds."
            + f"\n({self._dictionary.get_size()} words in dictionary.)\n"
        )

spellchecker_service = SpellcheckerService()
