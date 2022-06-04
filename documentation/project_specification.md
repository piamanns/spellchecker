# Project Specification

The aim of the project is to implement a spelling checker and corrector in Python. 

## Algorithms and Data Structures

The dictionary with correctly spelled words is generated from a text file containing a word list for some language and stored as a **trie data structure**.

When the user enters a word for spellchecking, the program will attempt to find the word in the dictionary. If the word does not match, the program will utilize an algorithm for calculating the **Damerau–Levenshtein distance** from the misspelled word to the words in the dictionary. Words with the lowest Damerau–Levenshtein distances are returned as possible candidates for correct spelling. 

## Sources

- https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
- https://web.archive.org/web/20180814145642/https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html, copy on https://www.lemoda.net/text-fuzzy/damerau-levenshtein/index.html
- http://stevehanov.ca/blog/index.php?id=114
- https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
- https://medium.com/smucs/trie-data-structure-fd2de3304e6e

## Degree programme

Bachelor's Programme in Computer Science

## Project language

English
