# Implementation Document

(Work in progress)

## Architecture

The code of the application is split into three layers: the user interface, the service layer and the repository layer.
- The _user interface_ is handled by [index.py](../src/index.py).
- The _services package_ contains the service layer code, i.e. the app logic and the algorithms for calculating Damerau-Levenshtein distances. The application logic is handled by the [SpellcheckerService-class](../src/services/spellchecker_service.py). The module [distance_service.py](../src/services/distance_service.py) contains the basic algorithm for calculating the Damerau-Levenshtein distance between two words. The module [distance_service_recursive.py](../src/services/distance_service_recursive.py) contains a recursive implementation of the Damerau-Levenshtein algorithm where the calculations of edit distances are done while traversing the trie data structure containing the reference word list. The classes related to the Trie data structure ([Trie](../src/entities/trie.py) and [Node](../src/entities/node.py)) are contained in the _entities package_.  
- The _repositories package_ contains the class  [WordlistRepository](../src/repositories/wordlist_repository.py), which handles the reading from and writing to the file on disk containing the wordlist used as a reference dictionary when checking the spelling of a given word. The filename of the wordlist used can be set in the [.env-file](../.env) in the project root.


## Algorithms and data structures utilized

(Work in progress)

### Trie

- Also called prefix tree; the time complexity for insertion, lookup and deletion is O(n), where n is the length of the key.
- Space complexity of a trie can be high

### Damerau-Levenshtein algorithm

- Basic implementation: comparing two words. Requires calculating the contents of a matrix with the dimensions len(source word) x len(target word), i.e. 
O(n x m)-time complexity.
- Comparing misspelled word to all words in large dictionary:
    - for-loop: matrix is calculated for each word in the dictionary separately.  
    Upper bound for time complexity: O(number of words x (maximum word length)^2)
    - recursive approach: Only one matrix row is calculated per node in the trie.  
    Upper bound for time complexity: O(maximum word length * number of nodes in the trie)
    - the effect of introducing a maximum allowed edit distance.

## Sources

- https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
- https://web.archive.org/web/20180814145642/https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html, copy on https://www.lemoda.net/text-fuzzy/damerau-levenshtein/index.html
- http://stevehanov.ca/blog/index.php?id=114
- https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
- https://en.wikipedia.org/wiki/Trie
- https://medium.com/smucs/trie-data-structure-fd2de3304e6e
