import unittest
from services.spellchecker_service import SpellcheckerService


class TestSpellcheckerService(unittest.TestCase):
    def setUp(self):
        self.sp_service = SpellcheckerService()
        self.sp_service.delete_all()

    def test_adding_the_first_word_works_correctly(self):
        self.sp_service.add_word("car")

        words = self.sp_service.get_all()
        self.assertEqual(len(words), 1)
        self.assertEqual(words[0], "car")
    
    def test_adding_an_already_existing_word_does_nothing_and_returns_False(self):
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")

        words_1 = self.sp_service.get_all()
        result = self.sp_service.add_word("car")
        words_2 = self.sp_service.get_all()

        self.assertEqual(len(words_1), len(words_2))
        self.assertEqual(result, False)

    def test_searching_for_word_that_exists_in_dictionary_returns_True(self):
        self.sp_service.add_word("zoo")

        result = self.sp_service.find_word("zoo")
        self.assertEqual(result, True)

    def test_searching_for_word_that_does_not_exists_in_dictionary_returns_False(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_word("zoo")
        self.assertEqual(result, False)

    def test_loading_wordlist_works_correctly(self):
        wordlist_content = ["art", "pass", "value"]
        for word in wordlist_content:
            self.sp_service.add_word(word)

        self.sp_service.load_wordlist()
        wordlist = self.sp_service.get_all()
        self.assertEqual(len(wordlist), 3)
        self.assertListEqual(wordlist, wordlist_content)
    
    def test_finding_closest_match_for_misspelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match("vaule")
        self.assertListEqual(result, ["value(1)"])
    
    def test_finding_closest_match_for_correctly_spelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match("car")
        self.assertListEqual(result, ["car"])
    
    def test_calculating_damerau_lewenshtein_distance_returns_correct_value(self):
        result = self.sp_service.calculate_distance("glamourous", "glamorous")
        self.assertEqual(result, 1)

        result = self.sp_service.calculate_distance("iresistable", "irresistible")
        self.assertEqual(result, 2)

        result = self.sp_service.calculate_distance("correct", "correct")
        self.assertEqual(result, 0)
