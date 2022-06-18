from pathlib import Path
from services.alphabet_utils import check_allowed_chars


class SpellingErrorParser:
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._error_count = 0
        self._max_error_len = 0

    def get_errordict(self):
        return self._read()

    def get_errors_per_letter_and_length(self):
        error_dict = self._read()
        return self._parse_errors_per_letter_and_length(error_dict)

    def print_error_stats(self):
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

    def _parse_errors_per_letter_and_length(self, error_dict: dict):
        errors_per_letter = {}
        for error in error_dict.keys():
            first_letter = error[0]
            if first_letter not in errors_per_letter:
                errors_per_letter[first_letter] = [[] for i in range(self._max_error_len + 1)]
            errors_per_letter[first_letter][len(error)].append(error)
        return errors_per_letter

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
                suggestions_ok = all(check_allowed_chars(sgn) for sgn in correct_spellings)
                if check_allowed_chars(misspelling) and suggestions_ok:
                    self._error_count += 1
                    self._max_error_len = max(len(misspelling), self._max_error_len)

                    if misspelling not in error_dict:
                        error_dict[misspelling] = []
                    for correct in correct_spellings:
                        error_dict[misspelling].append(correct)
        return error_dict
