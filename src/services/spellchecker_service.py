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
            The added word if the operation was carried out (i.e. the word was not already
            present in the wordlist), None if the word was already found in the
            wordlist.
        """

        if not self._dictionary.find(word):
            new_word = wordlist_repository.add(word)
            self._dictionary.add(new_word)
            return new_word
        return None

    def find_word(self, word: str):
        """ Checks if the word exists in the dictionary.

        Args:
            word: The word to look for as a string.

        Returns:
            True if the word was found, False otherwise.
        """

        return self._dictionary.find(word)

    def calculate_distance(self, word_a: str, word_b: str, neighbour_check=False, debug_flag=False):
        """ Calculates the Damerau-Lewenshtein distance between two words.

        Args:
            word_a: The source word as a string.
            word_b: The target word as a string.
            neighbour_check: A boolean indicating whether substitutions by
                             neighbouring characters on the keyboard should be
                             assigned a slightly lower edit cost than other
                             substitutions.
            debug_flag: A boolean describing whether the matrix
                        resulting from the calculation should be
                        returned in its entirety. Defaults to False.

        Returns:
            The Damerau-Lewnshtein distance as an integer (or float, if neighbouring key
            priority is activated).
        """

        return calculate_dl_distance(word_a, word_b, neighbour_check, debug_flag)

    def find_closest_match(self, word:str, max_edit=None, neighbour_check=False):
        """ Finds closest matching words in the dictionary for the given word.

        Args:
            word: The word to be matched.
            max_edit: An integer describing the maximum edit distance
                      allowed. Defaults to None.
            neighbour_check: A boolean indicatiing whether substitutions by
                             neighbouring characters on the keyboard should be
                             prioritised.

        Returns:
            A list of candidate words with the lowest Damerau-Lewenshtein
            distance to the given word. If the word itself was found in the
            dictionary (i.e. was correctly spelled) the list contains
            only the word itself.
        """

        if self.find_word(word):
            return [word]

        start = perf_counter()

        candidates = []
        wordlist = self.get_all()
        min_dist = max_edit if max_edit else max(len(word), len(wordlist[0]))
        for dict_word in wordlist:
            if abs(len(word)-len(dict_word)) > min_dist:
                continue
            dl_dist = calculate_dl_distance(word, dict_word, neighbour_check)
            if dl_dist <= min_dist:
                if dl_dist < min_dist:
                    candidates.clear()
                    min_dist = dl_dist
                candidates.append(f"{dict_word}({dl_dist})")

        end = perf_counter()
        self._latest_search_time = end-start

        return candidates

    def find_closest_match_recursively(self, word: str, max_edit=None, neighbour_check=False):
        """ Finds closest matching words in the dictionary for the given word.

        The search utilizes a recursive traversal of the trie for
        faster perfomance.

        Args:
            word: The word to be matched.
            max_edit: An integer describing the maximum edit distance
                      allowed. Defaults to None.
            neighbour_check: A boolean indicating whether substitutions by
                             neighbouring characters on the keyboard should be
                             prioritised.

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

        candidates = calculate_dl_distance_recursive(word, self._dictionary,
                                                     max_edit, neighbour_check)
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

    def get_search_time(self):
        """Returns time spent for latest search

        Returns:
            A float representing the search time in seconds.
        """

        return self._latest_search_time

    def get_dictionary_size(self):
        """Gets the size of the used dictionary.

        Returns:
            The amount of words stored in the dictionary as an integer.
        """

        return self._dictionary.get_size()


    def get_info(self):
        """ Returns information about the setup and performance
        of the spellchecker.

        Returns:
          A string containing:
          - the time used for the latest search in the dictionary
          for correctly spelled words with a low edit distance
          to the given word
          -  the size of the dictionary (number of words)
        """

        return (
            f"\nSearch took {self.get_search_time()} seconds."
            + f"\n({self.get_dictionary_size()} words in dictionary.)"
        )


spellchecker_service = SpellcheckerService()
