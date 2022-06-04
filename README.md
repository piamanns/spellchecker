# Spellchecker

A Python spelling checker and corrector. A course assignment for the Data Structures Project-course at the University of Helsinki.

## Weekly progress reports
- [Week 1](/documentation/weekly_report_1.md)
- [Week 2](/documentation/weekly_report_2.md)
- [Week 3](/documentation/weekly_report_3.md)
- [Week 4](/documentation/weekly_report_4.md)

## Documentation
- [Implementation](/documentation/implementation_document.md)
- [Testing](/documentation/testing_document.md)

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

### Check code quality with pylint:

```bash
poetry run invoke lint
```
