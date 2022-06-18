# Weekly Progress Report 6

This week I have spent most on my time on pondering performance testing: which tests to run and how, and on what kind of material. Spelling errors occur for many different kinds of reasons (lack of knowledge of correct spelling, homonym errors, mechanical slips when typing on a keyboard), and are affected by a multitude of variables (age, native vs non-native speakers, handwriting vs keyboard or touch screen device, touch typing vs hunt and peck typing and so on).

I decided on downloading a list of common English misspellings from Wikipedia (https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines), which contains common misspellings encountered in Wikipedia entries. My best guess is that this material contains spelling errors made by both native and non-native speakers, mainly typing on a computer keyboard. Since the list is quite long, I implemented a parser for reading the file and generating error lists [(spelling_error_parser.py)](../src/tets/spelling_error_parser.py).

The class [PerformanceTester](../src/tests/performance_tests.py) runs performance tests utilizing the Wikipedia spelling errors and writes the results to csv-files, which I intend to use for generating visual charts of the results.
For now a new list of misspelled words is generated randomly for each run of the performance tester; I intend to add the possibility to run the tests on a list of spelling errors given by the user for better reproducibility of the test results.

This week I was also assigned to peer review a very interesting project on maze generation and solving, and I ended up spending quite a few hours on getting acquainted with the algorithms utilized in the program.

Time used: 20 h.
