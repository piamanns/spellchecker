import unittest
from entities.trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
    
    def test_adding_a_word_to_an_empty_trie_works_as_expected(self):
        self.trie.add("foo")
        
        word = self.trie.find("foo")
        self.assertEqual(word, True)

        words = self.trie.get_all()
        self.assertEqual(len(words), 1)
        self.assertIn("foo", words)

    def test_adding_a_word_to_a_trie_with_previous_content_works_as_expected(self):
        self.trie.add("banana")
        self.trie.add("car")
        self.trie.add("zebra")

        word = self.trie.find("zebra")
        self.assertEqual(word, True)

        words = self.trie.get_all()
        self.assertEqual(len(words), 3)
        self.assertIn("zebra", words)

    def test_adding_a_word_with_the_same_prefix_as_some_shorter_word_works(self):
        self.trie.add("car")
        self.trie.add("carbon")

        word_1 = self.trie.find("car")
        word_2 = self.trie.find("carbon")

        self.assertEqual(word_1, True)
        self.assertEqual(word_2, True)

        words = self.trie.get_all()
        self.assertEqual(len(words), 2)
        self.assertIn("car", words)
        self.assertIn("carbon", words)
    
    def test_adding_a_word_with_the_same_prefix_as_some_longer_word_works(self):
        self.trie.add("carbon")
        self.trie.add("car")

        word_1 = self.trie.find("carbon")
        word_2 = self.trie.find("car")

        self.assertEqual(word_1, True)
        self.assertEqual(word_2, True)

        words = self.trie.get_all()
        self.assertEqual(len(words), 2)
        self.assertIn("carbon", words)
        self.assertIn("car", words)

    def test_finding_a_word_not_in_the_trie_returns_False(self):
        self.trie.add("foo")
        
        word = self.trie.find("bar")
        self.assertEqual(word, False)
