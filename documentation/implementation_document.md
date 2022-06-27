# Implementation Document

## Architecture

The code of the application is split into three layers: the user interface, the service layer and the repository layer.
- The _user interface_ is handled by [index.py](../src/index.py).
- The _services package_ contains the service layer code, i.e. the app logic and the algorithms for calculating Damerau-Levenshtein distances. The application logic is handled by the [SpellcheckerService-class](../src/services/spellchecker_service.py). The module [distance_service.py](../src/services/distance_service.py) contains the basic algorithm for calculating the Damerau-Levenshtein distance between two words. The module [distance_service_recursive.py](../src/services/distance_service_recursive.py) contains a recursive implementation of the Damerau-Levenshtein algorithm where the calculations of edit distances are done while traversing the trie data structure containing the reference word list. The classes related to the Trie data structure ([Trie](../src/entities/trie.py) and [Node](../src/entities/node.py)) are contained in the _entities package_.  
- The _repositories package_ contains the class [WordlistRepository](../src/repositories/wordlist_repository.py), which handles the reading from and writing to the file on disk containing the wordlist used as a reference dictionary when checking the spelling of a given word. The filename of the wordlist used can be set in the [.env-file](../.env) in the project root.

![Package diagram with classes](./images/spellchecker-package-diagram.png)

## Algorithms and data structures utilized

### Trie

The reference dictionary used for checking the spelling of and finding correctly spelled suggestions for a given word is loaded from a file on disk into a [trie](https://en.wikipedia.org/wiki/Trie) when the program starts. 

The time complexity for insertion, lookup and deletion in a trie is O(m), where m is the length of the key (in this case, a string representing a word). The time complexity of building the trie is thus O(n * m), where n is the number of words in the dictionary.

Every node in the trie contains a Python list of pointers to possible child nodes. The list has a constant size for every node in the trie, with the number of elements in the list corresponding to the number of characters in the alphabet used. This makes the lookup for child nodes fast, but increases the space complexity of the trie, since memory is allocated for a list of the size of the alphabet for every node, even if most nodes will never use some of the pointers.


### Algorithms for calculating Damerau-Levenshtein distance

When the user enters a word into the program, the word is searched for in the dictionary stored in the trie. If the word cannot be found, the word is assumed to be misspelled, and the program attempts to find one or more close matches in the dictionary to return as a suggested spellings. This process requires a metric for measuring the difference between two strings. The [Damerau-Levenshtein distance](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance) is such a metric, providing a value desicribing the smallest possible number of edit operations (*insertion*, *deletion*, *substitution* or *transposition of two adjacent characters*) needed to transform one string into another.

The Damerau-Levensthein distance between two strings is calculated using an extended version of the [Wagner-Fischer](https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm) dynamic programming algorithm. The algorithm requires calculating the contents of a matrix with the dimensions (source word length) x (target word length), which means the algorithm has a time complexity of O(n x m). The application contains a functionality for calculating the Damerau-Levenshtein distance between two given strings. In addition to the edit distance value, the functionality also prints out the matrix resulting from the algorithm.

The actual spell checker (and generator of suggested spellings) has **two implementations** in the application:

A **baseline version** with a for-loop. The entire word list is retrieved from the trie. The list is then iterated, while calculating the Damerau-Levenshtein distance to every word. As words with lower edit distances to the misspelled word are encountered, the maximum edit distance allowed is successively lowered, allowing for some words to be _skipped without any calculations_. (Words with an absolute length difference to the misspelled word larger than the maximum edit distance allowed can be ignored. Even if the prefixes of the words are identical, inserting or deleting the remaining characters - each operation with an edit cost of 1 - would result in the edit distance value being higher than a closer match already found.)  
The time complexity for the baseline spell checker implementation is O(number of words in the dictionary x (maximum word length)^2).

A **recursive approach**: The Damerau-Levenshtein distances to the words in the dictionary are calculated recursively while traversing the trie. In this implementation the misspelling is set as the target word (represented by the columns in the matrix), and only one new row needs to be calculated per node/letter in the trie, while the previous rows are shared by all words with the same prefix, and can be reused.  
As in the baseline version, the maximum allowed edit distance is succesively lowered as closer matches are found. This means entire branches of the trie can be skipped without calculation, if the smallest value in the current matrix row exceeds the maximum edit distance allowed.  
The time complexity of the recursive implementation of the spell checker is O(maximum word length x number of nodes in the trie)

Both spell checker implementations include the possibility for the user to **set the maximum allowed edit distance beforehand**. This speeds up the search for spelling suggestions if the automatic capping of the maximum edit distance takes effect slowly (i.e. the maximum allowed edit distance stays high for a long time).  

Both implementations also allow for an optional prioritisation of correctly spelled words where a character has been replaced in the misspelling with a character on a **neighbouring key** on the keyboard (one of several possible typographical errors that might occur when typing on a keyboard.) This priorisation is achieved by assigning substitutions by a neighbouring key a lower edit cost than other substitutions when calculating Damerau-Levenshtein distances.

## Wordlist used:

- List of English words: https://github.com/first20hours/google-10000-english ([License](https://github.com/first20hours/google-10000-english/blob/master/LICENSE.md))
- [Wikipedia: List of common misspellings](https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines) ([CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/))  

A more extensive wordlist (ca 90 000 words) downloaded from [http://app.aspell.net/create](http://app.aspell.net/create) has been used for performance tests run locally. This list was not added to the repository.

## Sources

- https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
- https://web.archive.org/web/20180814145642/https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html, copy on https://www.lemoda.net/text-fuzzy/damerau-levenshtein/index.html
- http://stevehanov.ca/blog/index.php?id=114
- https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
- https://en.wikipedia.org/wiki/Trie
- https://medium.com/smucs/trie-data-structure-fd2de3304e6e
