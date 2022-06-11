# Weekly Progress Report 4

This week I have tweaked the algorithms for finding suggestions for correct spelling further, in order to achieve higher search speed and, potentially, higher relevance for the suggestions. (The latter task is naturally much harder to both implement and evaluate, since relevance is highly context dependent and the current program is limited to handling single words only.)

As the course instructor pointed out after last week, the maximum edit distance allowed could be utilized even more effectively in the algorithms by successively lowering the limit as words with a lower Damerau-Levenshtein distance were found during the search. I made this change in both the baseline algorithm and the recursive implementation, which increased the performance of both versions.  

As a heuristic experiment to achieve better word suggestion quality, I also added the possibility to prioritise substitutions with characters on neighbouring keys on the keyboard, by assigning neighbouring key substitutions a lower edit cost than other substitutions while calculating DL-distances. Since hitting a neighbouring key instead of the intended is only one of a plethora of different mechanical typing errors that might occur while typing on a keyboard (as a quick review on reasearch done on the subject revealed), I do not expect this addition to the algorithms to increase the quality of the suggestions dramatically. I still intend to do some accuracy testing using some of the typo corpuses available online ([GitHub Typo Corpus](https://github.com/mhagiwara/github-typo-corpus), [Twitter Typo Corpus](http://luululu.com/tweet/)), as well as lists of commonly misspelled English words.

I also implemented a simple check for allowed characters to prevent annoying crashes when entering words containing characters not included in the used alphabet. I continued writing on the project documentation, which still needs work.

I also spent some time reading up on Markov chains, which were utilized in the project I was assigned to peer-review.

Time used: 16 h.
