# Weekly Progress Report 2

I implemented a simple prefix trie data structure for storing the wordlist used by the app. The program currently has the following functionalities:
- Read the wordlist from a file on disk and generate the trie
- Search for a word in the trie
- Add a word to the trie and the wordlist file. 

I also added unittests for both the Trie class and the WordlistRepository class that handles reading from and writing to the wordlist file.

The current implementation of the trie is very unflexible with regard to the alphabet used, allowing only for the letters a-z. This is due to the fact that the child nodes of every node are currently stored in a list, where the index number in the list corresponds to the ordinal number of the letter in the alphabet used, calculated from the ASCII-code for the letter. 
Furthermore, the length of the child node list is constant for every node in the trie, even if some of the indices in the list are never used. 

I am contemplating different options for allowing for a more flexible alphabet. 
Some Python spelling checker implementations seem to utilize a dict for storing the child nodes. The flexibility of the dict comes with the cost of a potential increase in time complexity, however (https://wiki.python.org/moin/TimeComplexity).

Next I will start work on the algorithm for calculating Damerau–Levenshtein distances.

Time used: 11 h
