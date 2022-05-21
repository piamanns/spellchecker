from pathlib import Path
from config import WORDLIST_PATH


class WordlistRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def get_wordlist(self):
        return self._read()

    def add(self, word: str):
        self._write(word)
        return word

    def delete_all(self):
        open(self._file_path, "w", encoding="utf-8").close()

    def _check_for_file(self):
        Path(self._file_path).touch()

    def _read(self):
        self._check_for_file()

        wordlist = []

        with open(self._file_path, encoding="utf-8") as file:
            for row in file:
                row = row.replace("\n", "")
                wordlist.append(row)

            return wordlist

    def _write(self, word: str):
        self._check_for_file()

        with open(self._file_path, "a", encoding="utf-8") as file:
            file.write(f"{word}\n")


wordlist_repository = WordlistRepository(WORDLIST_PATH)
