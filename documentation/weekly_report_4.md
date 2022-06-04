# Weekly Progress Report 4

This week I focused on speeding up the search for correctly spelled candidate words in the dictionary stored in the trie. My naive baseline implementation from last week retrieved a list of all words in the trie and calculated the Damerau-Levenshtein distance from the misspelled word to each word in the list using a for loop. A list containing the word(s) with the lowest edit distance was then returned.

Since this baseline implementation involves calculating the DL-distance for each and every word in the dictionary, it becomes very slow when the wordlist with correctly spelled words is large. 

A straightforward way of speeding things up is introducing a maximum edit distance: if the difference in length between the misspelled word and the candidate word is bigger than the maximum edit distance allowed, the candidate word can simply be skipped, without any calculations. This pruning of the candidate word wordlist made the spellchecking search somewhat faster.

The key to a big performance improvement, however, lies in utilizing the nature of the trie data structure while calculating DL-distances, as explained by Steve Hanov (http://stevehanov.ca/blog/index.php?id=114) in his informative blogpost.
Instead of recalculating the entire matrix for the Damerau-Levensthein algorithm from scratch for every word in the trie, the calculations are done recursively while traversing the trie, one matrix row at a time. For each node in the trie, that is, each new letter added to the prefix represented by the previous nodes, only the row corresponding to the added letter needs to be calculated, while the previous rows in the matrix can be reused.  

While Hanov's algorithm only calculates the Levenshtein distance, omitting transpositions of two characters, I reintroduced transpositions in my implementation. (On a personal note: if I had not read up on the basic unrestricted Damerau-Levenshtein algorithm the week before, this would probably have been a much harder task.)

As was the case with the baseline implementation, capping the allowed edit distance naturally speeds the process up even further, since the traversal of a particular prefix branch in the trie can be stopped if the minimum value in the current matrix row exceeds the maximum edit distance allowed. 

The program now contains two spelling correctors: one utilizing the baseline implementation ("5 - Check spelling (baseline for-loop)") and one utilizing the recursive approach (("6 - Check spelling (recursive)").
Both functionalities include the opportunity to set a maximum edit distance.

In addition to the list with suggested correctly spelled words, the program also reports the time used for the search and the size of the dictionary, which allows for comparing performance between the two search approaches and the effect of the dictionary size.

Next week I will do systematic performance testing, and also address the problem with the currently very limited allowed input alphabet (a-z), which I have not tackled yet. 

Time used: 16 h