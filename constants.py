from pathlib import PurePath

ROOT_DIR = PurePath(__file__).parent

PROJECTS_DIR = PurePath(ROOT_DIR, "projects")

PROJECT_GAME_DIR = "game"
PROJECT_CACHE_DIR = "cache"
PROJECT_EXTRACT_DIR = "extract"
PROJECT_TRANSLATE_DIR = "translate"
PROJECT_RESULT_DIR = "result"

TEXT_ORIGIN_FILE = "origin.json"
TEXT_TRANSLATE_FILE = "translate.json"
TRANSLATE_CACHE_FILE = "translate_cache.json"

CSV_HEADER = ["ID", "Label", "Context", "Original text", "Translated text"]