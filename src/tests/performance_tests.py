from datetime import datetime
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SPELLING_ERRORS_PATH
from random import choice
from repositories.spelling_error_repository import SpellingErrorRepository
from services.spellchecker_service import spellchecker_service


class PerformanceTester:
    def __init__(self):
        self._spelling_error_repository = SpellingErrorRepository(SPELLING_ERRORS_PATH)
        self._error_dict = self._spelling_error_repository.get_errordict()

    def run_all(self):
        """Runs performance tests on the spellchecker.

        The list of misspelled words utilized in the tests is created
        randomly for now.
        Results are written to a file in the data/test_results directory.
        """

        print("Running performance tests...", flush=True)

        error_list = self.create_error_list(5)

        # Baseline:
        results = self.run_speed_test(error_list)
        self._write(results, "_baseline")

        # Recursive:
        results = self.run_speed_test(error_list, "recursive")
        self._write(results, "_recursive")

    def create_error_list(self, error_len=5):
        """Creates a list of misspelled words with the given length.

        One word per first letter is chosen. The letter is skipped 
        if no word of the wanted length is found for the letter.
        This means the resulting list may vary in length.

        Args:
            error_len: The wanted word length. Defaults to 5.

        Returns:
            A list of strings representing misspellings, all with the same length.
        """

        error_list = []
        errors = self._spelling_error_repository.get_errors_per_letter_and_length()
        for key in errors:
            if len(errors[key][error_len]) > 0:
                error_list.append(choice(errors[key][error_len]))
        return error_list

    def run_speed_test(self, error_list: list, search_type="None"):
        results = []
        for error in error_list:
            search_time, result = self._run_search(error, search_type)
            success, correct_spelling = self._check_result(error, result)
            results.append([error, correct_spelling, search_time, result, success])
        return results

    def _run_search(self, error: str, search_type=None):
        result = []
        if search_type == "recursive":
            result = spellchecker_service.find_closest_match_recursively(error)
        else: 
            result = spellchecker_service.find_closest_match(error)
        search_time = spellchecker_service.get_search_time()
        return search_time, result
 
    def _check_result(self, error: str, result: list):
        correct_spelling = self._error_dict[error]
        for suggestion in result:
            if suggestion.split("(")[0] in correct_spelling:
                return True, correct_spelling
        return False, correct_spelling

    def _write(self, results: list, file_suffix=None):
        test_time = datetime.now().strftime("%Y%m%d%H%M%S")       
        file_name = test_time + "_performance_test" + file_suffix + ".txt"
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "..", "..", "data", "test_results", file_name)

        print(f"Results: data/test_results/{file_name}")
   
        with open(file_path, "w", encoding="utf-8") as file:
            for result in results:
                misspelling = result[0]
                correct_spellings = ",".join(result[1])
                search_time = result[2]
                suggestions = ",".join(result[3])
                success = result[4]
                row = f"{misspelling};{correct_spellings};{search_time};{suggestions};{success}\n"
                file.write(row)


if __name__ == "__main__":
    pt = PerformanceTester()
    pt.run_all()
