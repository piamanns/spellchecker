# Testing Document

## Automated unit tests

The program has been automatically tested using the _unittest_ framework.

- The app logic class SpellCheckerService.py is tested with the class [TestSpellcheckerService](../src/tests/spellchecker_service_test.py). This test class also includes tests for the module providing the recursive implementation of traversing the trie and calculating Damerau-Levenshtein distances on the fly (distance_service_recursive).

- The WordlistRepository class, handling the reading from and writing to the wordlist file on disk, is tested with the class [TestWordlistRepository](../src/tests/wordlist_repository_test.py). The tests utlize a separate wordlist, used for testing purposes only. The filename of the test wordlist is configured in the .env.test-file.

- The module providing the basic functions for calculating the Damerau-Levenshtein distance (distance_service) is tested with the class [TestDistanceService](../src/tests/distance_service_test.py).

- The classes for the implementation of the trie data structure (Trie and Node) are tested with the class [TestTrie](../src/tests/trie_test.py).

The current overall branch coverage of the automated tests is 97%:

![Picture of coverage report](./images/coverage-report_100622.png)

## Performance testing

Testing of the performance of the two spellchecker implementations on different size dictionaries has been carried out manually, and can be repeated through the user interface.

The program prints out the time used for the search for correctly spelled alternatives for a misspelled word after each spelling check, as well as the size of the dictionary. The timing is handled by the [SpellcheckerService-class](../src/services/spellchecker_service.py#L94).

The dictionary used can be changed by changing the filename of the file containing the wordlist with correctly spelled (WORDLIST_FILENAME) in the [.env-file](../.env). The wordlist file should be placed in the data directory and contain one word per row.  
**Only letters a-z** are allowed in the current implementation. Parameters and functions relating to the allowed alphabet can be changed in the [alphabet_utils.py](../src/services/alphabet_utils.py)-file.

### Some initial results

Wordlist used for tests downloaded from [http://app.aspell.net/create](http://app.aspell.net/create).

**Word searched for:** "zooom"  
**Dictionary size:** 90 555 words.  


| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | zoom(1)| None | 1.3358805160969496 |
| Recursive | zoom(1) | None | 0.06754672597162426 |

| Baseline (for-loop) | zoom(1)| 2 | 1.285144078778103 |
| Recursive | zoom(1) | None | 0.05830277199856937 |

| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | zoom(1)| 1 | 0.8230881099589169 |
| Recursive | zoom(1) | 1 | 0.011647125007584691 |


**Word searched for:** "definateyl"  
**Dictionary size:** 90 555 words. 


| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | definitely(2) | None | 4.629521565977484 |
| Recursive | definitely(1) | None | 0.31806356809102 |

| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | definitely(2) | 3 | 4.439275296870619|
| Recursive | definitely(1) | 3 | 0.14999102288857102 |

| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | definitely(2) | 2 | 4.132949609076604|
| Recursive | definitely(1) | 3 | 0.1062636328861117 |


**Word searched for:** "asdfgh"  
**Dictionary size:** 90 555 words. 


| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | adage(3), ash(3), asiago(3), assign(3), aweigh(3), sigh(3), singh(3), sough(3) | None | 2.771614557830617 |
| Recursive | adage(3), ash(3), asiago(3), assign(3), aweigh(3), sigh(3), singh(3), sough(3) | None | 0.23779252800159156 |

| Algorithm | Result | Max edit distance | Time used (seconds) |
| --- | --- | --- | --- | 
| Baseline (for-loop) | adage(3), ash(3), asiago(3), assign(3), aweigh(3), sigh(3), singh(3), sough(3) | 3 | 2.63363699009642 |
| Recursive | adage(3), ash(3), asiago(3), assign(3), aweigh(3), sigh(3), singh(3), sough(3) | 3 | 0.21872165193781257 |


The recursive algorithm is clearly much faster than the baseline implementation of looping through every word in the wordlist and calculating the Damerau-Levenshtein distance to the each word separately.

Capping the allowed Damerau-Levensthein distance from the beginning speeds up both search implementations, especially if the automatic capping built-in in the algorithms kicks in slowly (i.e., the current lowest Damerau-Levenshtein distance found in the wordlist is high for a long time.)    
The capping of the maximum edit distance allowed should on average have a bigger effect on the speed of the recursive algorithm, since entire trie branches of words with common prefixes can be skipped at one go if the limit is exceeded.
