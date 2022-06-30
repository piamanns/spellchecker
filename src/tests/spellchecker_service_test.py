import unittest
from time import perf_counter
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
    
    def test_adding_an_already_existing_word_does_nothing_and_returns_None(self):
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")

        words_1 = self.sp_service.get_all()
        result = self.sp_service.add_word("car")
        words_2 = self.sp_service.get_all()

        self.assertEqual(len(words_1), len(words_2))
        self.assertEqual(result, None)

    def test_searching_for_word_that_exists_in_dictionary_returns_True(self):
        self.sp_service.add_word("zoo")

        result = self.sp_service.find_word("zoo")
        self.assertEqual(result, True)

    def test_searching_for_word_that_does_not_exist_in_dictionary_returns_False(self):
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
    
    def test_calculating_damerau_lewenshtein_distance_returns_correct_value(self):
      result = self.sp_service.calculate_distance("glamourous", "glamorous")
      self.assertEqual(result, 1)

      result = self.sp_service.calculate_distance("iresistable", "irresistible")
      self.assertEqual(result, 2)

      result = self.sp_service.calculate_distance("correct", "correct")
      self.assertEqual(result, 0)

    def test_baseline_finding_closest_match_for_misspelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match("vaule")
        self.assertListEqual(result, ["value(1)"])

        result = self.sp_service.find_closest_match("crabone")
        self.assertListEqual(result, ["carbon(2)"])

    def test_baseline_finding_closest_match_for_correctly_spelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match("car")
        self.assertListEqual(result, ["car"])
    
    def test_baseline_capping_edit_distance_for_matches_works_correctly(self):
        self.sp_service.add_word("artist")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("passport")
        self.sp_service.add_word("valuable")

        result = self.sp_service.find_closest_match("carb")
        self.assertEqual(result, ["carbon(2)"])

        result = self.sp_service.find_closest_match("car", 2)
        self.assertEqual(len(result), 0)
    
    def test_baseline_prioritising_substitutions_by_neighbouring_keys_works_correctly(self):
        self.sp_service.add_word("bank")
        self.sp_service.add_word("band")

        result = self.sp_service.find_closest_match("banf", None, True)
        self.assertEqual(result, ["band(0.5)"])
    
    def test_recursive_search_for_closest_match_for_misspelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match_recursively("vaule")
        self.assertListEqual(result, ["value(1)"])

        result = self.sp_service.find_closest_match("crabone")
        self.assertListEqual(result, ["carbon(2)"])
    
    def test_recursive_search_for_closest_match_for_correctly_spelled_word_works_as_expected(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match_recursively("car")
        self.assertListEqual(result, ["car"])

    def test_recursive_search_capping_edit_distance_works_correctly(self):
        self.sp_service.add_word("artist")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("passport")
        self.sp_service.add_word("valuable")

        result = self.sp_service.find_closest_match("carb")
        self.assertEqual(result, ["carbon(2)"])

        result = self.sp_service.find_closest_match("car", 2)
        self.assertEqual(len(result), 0)

    def test_recursive_search_prioritising_substitutions_by_neighbouring_keys_works_correctly(self):
        self.sp_service.add_word("bale")
        self.sp_service.add_word("ball")
        self.sp_service.add_word("balm")
        self.sp_service.add_word("bawl")

        result = self.sp_service.find_closest_match_recursively("balw", None, False)
        self.assertEqual(result, ["bale(1)", "ball(1)", "balm(1)", "bawl(1)"])

        result = self.sp_service.find_closest_match_recursively("balw", None, True)
        self.assertEqual(result, ["bale(0.5)"])

    def test_empty_list_is_returned_if_no_candidates_are_found(self):
        self.sp_service.add_word("art")
        self.sp_service.add_word("car")
        self.sp_service.add_word("carbon")
        self.sp_service.add_word("pass")
        self.sp_service.add_word("value")

        result = self.sp_service.find_closest_match_recursively("endeavrour", 1)
        self.assertListEqual(result, [])
    
    def test_get_latest_search_time_returns_correct_value(self):
        wordlist = ["art", "bale", "ball", "balm", "car", "carbon", "pass",
                    "passport", "value", "water", "what", "whether"]
        for word in wordlist:
            self.sp_service.add_word(word)

        start = perf_counter()
        self.sp_service.find_closest_match_recursively("pass")
        end = perf_counter()
        self.assertAlmostEqual(start-end, self.sp_service.get_search_time(), places=3)
    
    def test_get_dictionary_size_returns_correct_value(self):
        wordlist = ["art", "bale", "ball", "balm", "car", "carbon", "pass",
                    "passport", "value", "water", "what", "whether"]
        for word in wordlist:
            self.sp_service.add_word(word)
        
        result = self.sp_service.get_dictionary_size()
        
        self.assertEqual(len(wordlist), result)

    def test_get_info_returns_correct_string(self):
        wordlist = ["art", "bale", "ball", "balm", "car", "carbon", "pass",
                    "passport", "value", "water", "what", "whether"]
        for word in wordlist:
            self.sp_service.add_word(word)

        self.sp_service.find_closest_match_recursively("whether")
        ref_string = (f"\nSearch took {self.sp_service.get_search_time()} seconds."
                     + f"\n({len(wordlist)} words in dictionary.)")
        self.assertEqual(ref_string, self.sp_service.get_info())
