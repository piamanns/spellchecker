import unittest
from repositories.wordlist_repository import wordlist_repository
from services.alphabet_utils import get_allowed_chars

class TestWordlistRepository(unittest.TestCase):
    def setUp(self):
        wordlist_repository.delete_all()
        self.words = [
            "art",
            "artist",
            "car",
            "carbon",
            "difficult",
            "difficulties",
            "difficulty",
            "pass",
            "passage",
            "passed",
            "value",
            "valued",
            "values",
            "zoo",
            "zoom"
        ]
    
    def test_writing_word_to_wordlist_works(self):
        wordlist_repository.add(self.words[0])
        
        wordlist = wordlist_repository.get_wordlist()

        self.assertEqual(wordlist[0], self.words[0])


    def test_reading_entire_wordlist_works(self):
        for word in self.words:
            wordlist_repository.add(word)
        
        wordlist = wordlist_repository.get_wordlist()

        self.assertEqual(len(wordlist), len(self.words))
        self.assertListEqual(wordlist, self.words)
    
    def test_words_in_file_with_characters_not_in_alphabet_are_skipped(self):
        for word in self.words:
            wordlist_repository.add(word)
        non_letter_word = "%&!123"
        wordlist_repository.add(non_letter_word)

        wordlist =  wordlist_repository.get_wordlist()
        self.assertEqual(len(wordlist), len(self.words))
        self.assertNotIn(non_letter_word, wordlist)
