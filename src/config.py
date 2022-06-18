import os
from dotenv import load_dotenv


dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    print(".env file not found")

WORDLIST_FILENAME = os.getenv("WORDLIST_FILENAME") or "google-10000-english-no-swears.txt"
WORDLIST_PATH = os.path.join(dirname, "..", "data", WORDLIST_FILENAME)

SPELLING_ERRORS_FILENAME = os.getenv("SPELLING_ERRORS_FILENAME") or "wikipedia-spelling-errors.txt"
SPELLING_ERRORS_PATH = os.path.join(dirname, "..", "data", SPELLING_ERRORS_FILENAME)
