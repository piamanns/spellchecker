# Weekly Progress Report 3

I implemented the algorithm calculating the Damerau-Levenshtein distance between two words, using the pseudocode found in the Wikipedia article on Damerau-Levenshtein distance (https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance). Since the pseudocode in Wikipedia is quite sparsely commented, I found a blogpost by James M. Jensen II on the subject (https://web.archive.org/web/20180814145642/https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html, copy on https://www.lemoda.net/text-fuzzy/damerau-levenshtein/index.html) very clarifying with regard to some of the variables used.

The program now has two added features:
- Calculating the Damerau-Levenshtein distance between two given words
- The actual spell checker: finding and returning a list of correctly spelled candidate words from the app dictionary for a given, potentially misspelled word. 

I also wrote some unit tests for the new features.

The current implementation of the spell checker is very slow, especially when running the program on a large wordlist (> 90 000 words). I will attempt to explore alternatives for speeding up the process. 
It might also be interesting to do a comparison of the current spelling checker implementation and the approach suggested by Peter Norvig (http://norvig.com/spell-correct.html) with regard to speed.

Other possible next steps:
- Allowing the user to set a maximum value for the Damera-Levenshtein distance when searching for candidate words
- A graphical user interface utilizing tkinter

Time used: 11 h
