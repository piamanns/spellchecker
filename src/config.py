import os
from dotenv import load_dotenv


dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".envi"))
except FileNotFoundError:
    pass

WORDLIST_FILENAME = os.getenv("WORDLIST_FILENAME") or "google-10000-english-no-swears.txt"
WORDLIST_PATH = os.path.join(dirname, "..", "data", WORDLIST_FILENAME)
