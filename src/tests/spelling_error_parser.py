from pathlib import Path
from services.alphabet_utils import check_allowed_chars
from services.spellchecker_service import spellchecker_service


class SpellingErrorParser:
    """Helper class for parsing a list of misspellings

    Implemented for the format of the Wikipedia list of common misspellings
    (https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines).
    Each row in the file contains a misspelled word separated
    from the intended word(s) by the character sequence '->'.
    If there are several possible intended spellings, they are separated
    from each other by a comma and a single space character.

    """

    def __init__(self, file_path: str):
        """The class constructor.

        Args:
            The path to the file containing the list of misspelled words.
        """

        self._file_path = file_path
        self._error_count = 0
        self._max_error_len = 0
        self._min_error_len = None

    def get_errordict(self):
        """Returns a dictionary with all misspellings.

        Misspellings where either the misspelled word or the intended
        word contains characters not in the alphabet used (as defined in 
        alphabet_utils) are skipped.
        Misspellings were the intended spelling is not present in the 
        reference dictionary used in the application are skipped.

        Returns:
            A Python dict with the misspellings as keys and lists containing 
            the intended spelling(s) as values.
        """

        return self._read()

    def get_max_error_len(self):
        """Gets the length of the longest misspelled word.

        Returns:
            The length of the longest misspelled word in the file as an integer.
        """

        return self._max_error_len
    
    def get_min_error_len(self):
        """Gets the length of the shortest misspelled word.

        Returns:
            The length of the shortest misspelled word in the file as an integer.
        """

        return self._min_error_len

    def get_errors_per_letter(self, collate_by_length=False):
        """Gets misspellings grouped by first character.

        Args:
            collate_by_length: A boolean describing whether the misspellings
            should be grouped by length. Defaults to False.

        Returns:
            A Python dict with the first letters of the misspellings as keys.
            If collate_by_length is set to True, the values are lists of lists, where
            the index in the first list corresponds to the length of the misspellings
            contained in the list in that particular index.
            If collate_by_length is set to False, the values are lists containing 
            all misspellings beginning with the letter indicated by the key.
        """

        error_dict = self._read()
        return self._parse_errors_per_letter(error_dict, collate_by_length)
    
    def get_errors_per_length(self):
        """Gets misspellings grouped by length.

        Returns:
            A Python dict with the lengths of the misspellings as keys, and
            lists containing all misspellings of that particular length as values.
        """

        error_dict = self._read()
        return self._parse_errors_per_length(error_dict)

    def print_error_stats(self):
        """Prints some statistics for the misspelling data.

        Prints a table showing the distribution of misspelled words in the 
        misspelling file by first letter and length.
        
        """

        error_dict = self.get_errordict()
        error_stats = self._parse_stats(error_dict)

        for i in range(self._max_error_len+1):
            print(f"{i:3}|", end="")
        print()
        for letter, wordlist in error_stats.items():
            row = f"{letter:3}"
            for j in range(1, self._max_error_len+1):
                row += f"{wordlist[j]:4}"
            print(row)
        print(f"A total of {self._error_count} errors.\n")

    def _parse_stats(self, error_dir: dict):
        stats = {}
        for error in error_dir:
            first_letter = error[0]
            if first_letter not in stats:
                stats[first_letter] = [0] * (self._max_error_len + 1)
            error_len = len(error)
            stats[first_letter][error_len] += 1
        return stats

    def _parse_errors_per_letter(self, error_dict: dict, collate_by_length=False):
        errors_per_letter = {}
        for error in error_dict:
            first_letter = error[0]
            if first_letter not in errors_per_letter:
                if collate_by_length:
                    errors_per_letter[first_letter] = [[] for i in range(self._max_error_len + 1)]
                else:
                    errors_per_letter[first_letter] = []
            if collate_by_length:
                errors_per_letter[first_letter][len(error)].append(error)
            else:
                errors_per_letter[first_letter].append(error)
        return errors_per_letter

    def _parse_errors_per_length(self, error_dict: dict):
        errors_per_length = {}
        for error in error_dict:
            length = len(error)
            if length not in errors_per_length:
                errors_per_length[length] = []
            errors_per_length[length].append(error)
        return errors_per_length

    def _check_correct_spellings(self, correct_spellings: list):
        if not all(check_allowed_chars(csp) for csp in correct_spellings):
            return False
        for correct in correct_spellings:
            if not spellchecker_service.find_word(correct):
                return False
        return True

    def _check_for_file(self):
        Path(self._file_path).touch()

    def _read(self):
        self._check_for_file()

        error_dict = {}

        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                parts = row.split("->")
                misspelling = parts[0]
                correct_spellings = parts[1].split(", ")
                corrects_ok = self._check_correct_spellings(correct_spellings)
                if check_allowed_chars(misspelling) and corrects_ok:
                    self._error_count += 1

                    self._max_error_len = max(len(misspelling), self._max_error_len)
                    if not self._min_error_len or len(misspelling) < self._min_error_len:
                        self._min_error_len = len(misspelling)

                    if misspelling not in error_dict:
                        error_dict[misspelling] = []
                    for correct in correct_spellings:
                        error_dict[misspelling].append(correct)
        return error_dict
