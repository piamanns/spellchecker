"""Spellchecker Performance Tester

A script for running performance tests on the Spellchecker app.

"""


from datetime import datetime
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SPELLING_ERRORS_FILENAME, SPELLING_ERRORS_PATH, WORDLIST_FILENAME
from random import choice, sample
from tests.spelling_error_parser import SpellingErrorParser
from services.alphabet_utils import get_allowed_chars
from services.spellchecker_service import spellchecker_service


class PerformanceTester:
    """A class for performance testing of the Spellchecker app.

    Attributes:
            spell_error_parser: An instance of the SpellingErrorParser class. The
                                parser extracts data from a file with misspelled words.
            default_error_word_len: An integer describing the default length of misspelled
                                    words used if no length is given.
            default_error_list_len: An integer describing the default length for the
                                    list containing misspellings.
    """

    def __init__(self):
        """The class constructor.
        """

        self.spell_error_parser = SpellingErrorParser(SPELLING_ERRORS_PATH)
        self.default_error_word_len = 7
        self.default_error_list_len = 10
        self._error_dict = self.spell_error_parser.get_errordict()

    def run(self, error_list=None, max_edit=None, neighbour_prio=False):
        """Runs performance tests on the Spellchecker app.

          Results are written to files in the test_results directory
          in the project root.

        Args:
            error_list: A list of misspelled words separated by a single space.
                        Spell checking is run on every word in the list. Defaults to None.
            max_edit: An integer describing the maximum edit distance allowed when searching 
                      for suggestions for correct spelling. Defaults to None.
            neighbour_prio: A boolean indicating whether to prioritise substitutions 
                            by neighbouring keys. Defaults to False.
        """

        print("Running performance tests... (this might take a while!)\n", flush=True)
      
        if not error_list or len(error_list) == 0:
            error_list = self.create_error_list(
                self.default_error_word_len,
                self.default_error_list_len,
                False
            )

        # Baseline:
        results = self._run_speed_test(error_list, "baseline", max_edit, neighbour_prio)
        suffix = f"_{str(max_edit)}_{str(neighbour_prio)}"
        self._write(results, f"_baseline{suffix}")
 
        # Recursive:
        results = self._run_speed_test(error_list, "recursive", max_edit, neighbour_prio)
        self._write(results, f"_recursive{suffix}")
  
        print(f"\nSpelling errors used in tests: {' ' .join(error_list)}")
        print(f"Params: max_edit: {max_edit}, neighbour_prio: {neighbour_prio}")
        print(f"Spelling error file: {SPELLING_ERRORS_FILENAME}")
        print(f"Dictionary used: {WORDLIST_FILENAME}")
        print(f"Dictionary size: {spellchecker_service.get_dictionary_size()} words\n")

    def create_error_list(self, error_len=None, list_len=None, distribute=False):
        """Creates a list of spelling errors from the dict returned by
          the spelling error parser.

        Args:
            error_len: The wanted length of misspelled words as an integer.
                       Defaults to None.
            list_len: The wanted length of the list containing misspellings.
                      Defaults to None.
            distribute: A boolean describing whether to return a maximum of one
                        spelling error per first letter. Defaults to False.

        Returns:
            A list containing misspelled words as strings.
        """

        error_list = []

        if not list_len:
            list_len = self.default_error_list_len

        if distribute:
            if error_len:
                errors = self.spell_error_parser.get_errors_per_letter(True)
                for key in errors:
                    if len(errors[key][error_len]) > 0:
                        error_list.append(choice(errors[key][error_len]))
            else:
                errors = self.spell_error_parser.get_errors_per_letter(False)
                for key in errors:
                     if len(errors[key]) > 0:
                        error_list.append(choice(errors[key]))
        else: 
            if error_len: 
                error_list = self.spell_error_parser.get_errors_per_length()[error_len]
            else:
                sample_size = list_len if list_len else self.default_error_list_len
                error_list = sample(list(self._error_dict.keys()), sample_size)

        if list_len and list_len < len(error_list):
            return sorted(sample(error_list, list_len))   
        return sorted(error_list)

    def _run_speed_test(self, error_list: list, search_type=None,
                       max_edit=None, neighbour_prio=None):
        results = []
        for error in error_list:
            search_time, result = self._run_search(error, search_type, max_edit, neighbour_prio)
            success, correct_spelling = self._check_result(error, result)
            results.append([error, correct_spelling, search_time, result, success])
        return results

    def _run_search(self, error: str, search_type=None,
                    max_edit=None, neighbour_prio=None):
        result = []
        if search_type == "recursive":
            result = spellchecker_service.find_closest_match_recursively(
                error, max_edit, neighbour_prio
            )
        else: 
            result = spellchecker_service.find_closest_match(error, max_edit, neighbour_prio)
        search_time = spellchecker_service.get_search_time()
        return search_time, result
 
    def _check_result(self, error: str, result: list):
        correct_spelling = []
        if error not in self._error_dict:
            # Intended spelling is unknown
            correct_spelling = None
        else:
            correct_spelling = self._error_dict[error]
            for suggestion in result:
                if suggestion.split("(")[0] in correct_spelling:
                    return True, correct_spelling
        return False, correct_spelling

    def _write(self, results: list, file_suffix=None):
        test_time = datetime.now().strftime("%Y%m%d%H%M%S")       
        file_name = test_time + "_perf_test" + file_suffix + ".csv"
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "..", "..", "test_results", file_name)

        print(f"Results: root/test_results/{file_name}")
        column_names = ["misspelling", "intended", "time", "suggested", "success"]

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(";".join(column_names) + "\n")
            for result in results:
                misspelling = result[0]
                correct_spellings = ",".join(result[1])
                search_time = result[2]
                suggestions = ",".join(result[3])
                success = result[4]
                row = f"{misspelling};{correct_spellings};{search_time};{suggestions};{success}\n"
                file.write(row)


def print_commands():
    print("Commands:")
    print("1: Print misspelling distribution stats (freq per first letter and length)")
    print("2: Create random list of misspellings")
    print("3: Run tests")
    print("0: Quit")

def get_list_params_input(default_list_len: int, min_error_len: int, max_error_len: int):
    print("Randomizing list of misspellings:")
    try:
        list_len = int(input(f"Enter maximum list length (defaults to {default_list_len}): "))
    except ValueError:
        list_len = None
    try: 
        error_len = int(input("Enter length for misspelled words"
                              + f" (min:{min_error_len}, max:{max_error_len}, "
                              + "empty for no restrictions): "))
    except ValueError:
        error_len = None
    
    distr_input = input("Distribute misspellings over alphabet?\n"
                        + "A maximum of one misspelling per first letter" 
                        + " is returned (y/n): ")
    distribute = True if distr_input == "y" else False
    return error_len, list_len, distribute

def get_test_params_input():
    max_edit = None
    try:
        value = int(input("Enter max edit distance allowed (empty for unrestricted): "))
        max_edit = value if value > 0 else None
    except ValueError:
        pass
    
    neighbour_input = input("Prioritise substitutions by neighbouring keys? (y/n): ")
    neighbour_prio = True if neighbour_input == "y" else False
    return max_edit, neighbour_prio

def main():
    pt = PerformanceTester()

    while True: 
        print_commands()
        try:
            cmd = int(input("Choose a command: "))
        except ValueError:
            continue

        if cmd == 0:
            break
        if cmd == 1:
            pt.spell_error_parser.print_error_stats()
        if cmd == 2:
            error_len, list_len, distribute = get_list_params_input(
                                                  pt.default_error_list_len,
                                                  pt.spell_error_parser.get_min_error_len(),
                                                  pt.spell_error_parser.get_max_error_len()
                                              )
            result = pt.create_error_list(error_len, list_len, distribute)
            print(" ".join(result))
        if cmd == 3:
            predefined = input("Use predefined error list? (y/n, n generates random list): ")
            error_list = []
            if predefined == "y":
                errors = input("Enter list (misspellings separated by space): ")
                allowed = get_allowed_chars()
                pattern = f"([{allowed}][ ]?)+"
                match = re.fullmatch(pattern, errors)
                if not match:
                    print("Check your list syntax")
                    print(f"Only characters {allowed} allowed")
                    print("Separate misspellings with single space character")
                    continue
                if not errors == "":
                    errors = errors.strip()
                    error_list = errors.split(" ")
            max_edit, neighbour_prio = get_test_params_input()            
            pt.run(error_list, max_edit, neighbour_prio)


if __name__ == "__main__":
    main()
