# Spellchecker

A Python spelling checker and corrector. A course assignment for the Data Structures Project-course at the University of Helsinki.

## Weekly progress reports
- [Week 1](/documentation/weekly_report_1.md)
- [Week 2](/documentation/weekly_report_2.md)
- [Week 3](/documentation/weekly_report_3.md)
- [Week 4](/documentation/weekly_report_4.md)
- [Week 5](/documentation/weekly_report_5.md)
- [Week 6](/documentation/weekly_report_6.md)

## Documentation
- [Project specification](/documentation/project_specification.md)
- [Implementation](/documentation/implementation_document.md)
- [Testing](/documentation/testing_document.md)

## Wordlists used
- List of English words: https://github.com/first20hours/google-10000-english ([License](https://github.com/first20hours/google-10000-english/blob/master/LICENSE.md))
- [Wikipedia: List of common misspellings](https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines) ([CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/))

## Install and run

1. Install dependencies:

```bash
poetry install
```

2. Start the app:

```bash
poetry run invoke start
````

## Other commands:

### Run unit tests:

```bash
poetry run invoke test
```

### Generate test coverage report:

Report is created in htmlcov/index.html in the root directory.

```bash
poetry run invoke coverage-report
```

### Run performance test:

```bash
poetry run invoke performance-test
```
The test results are written to the test_results-directory in the project root.  

Row content in test result files:  
_misspelling;correct spelling(s);search duration;suggested spelling(s);correct spelling among suggestions (True or False)_

### Check code quality with pylint:

```bash
poetry run invoke lint
```

## Credits

- Inspired by [Steve Hanov's blog post](http://stevehanov.ca/blog/index.php?id=114) on utilizing the trie data structure for calculating (Levenshtein) edit distances recursively
- The Wikipedia pseudocode for calculating true Damerau-Levensthein distance is excellently clarified in [James M. Jensen II´s blog post](https://web.archive.org/web/20180814145642/https://scarcitycomputing.blogspot.com/2013/04/damerau-levenshtein-edit-distance.html).
