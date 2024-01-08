import json
import time
from pathlib import PurePath
from pathlib import Path
from constants import PROJECTS_DIR, PROJECT_CACHE_DIR, PROJECT_TRANSLATE_DIR, TEXT_ORIGIN_FILE, TEXT_TRANSLATE_FILE, \
    TRANSLATE_CACHE_FILE
from scripts.translators.azureai import azure_translate


def _store_translate_cache(project_name, translate_cache):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    cache_dir = PurePath(project_dir, PROJECT_CACHE_DIR)
    translate_cache_file = Path(cache_dir, TRANSLATE_CACHE_FILE)

    try:
        if not Path(cache_dir).exists():
            Path(cache_dir).mkdir(parents=True, exist_ok=True)
    except:
        return {}

    with open(translate_cache_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(translate_cache, ensure_ascii=False))


def _load_translate_cache(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    cache_dir = PurePath(project_dir, PROJECT_CACHE_DIR)
    translate_cache_file = Path(cache_dir, TRANSLATE_CACHE_FILE)

    try:
        if not Path(translate_cache_file).exists():
            return {}
    except:
        return {}

    with open(translate_cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def translate(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    translate_dir = PurePath(project_dir, PROJECT_TRANSLATE_DIR)
    origin_file = Path(translate_dir, TEXT_ORIGIN_FILE)
    translate_file = Path(translate_dir, TEXT_TRANSLATE_FILE)
    translate_cache = _load_translate_cache(project_name)

    try:
        Path(origin_file).exists()
    except:
        print("Error: origin_file file not found.")
        return

    unique_strings = set()
    with open(origin_file, 'r', encoding='utf-8') as f:
        origin = json.load(f)
        for key in origin:
            unique_strings.add(origin[key])

    batch_size = 50
    sleep_time = 2
    unique_strings = list(unique_strings)
    need_translate = []

    for origin_value in unique_strings:
        if origin_value in translate_cache:
            continue
        need_translate.append(origin_value)

    if len(need_translate) > 0:
        batched_values = [need_translate[i:i + batch_size] for i in range(0, len(need_translate), batch_size)]

        count = 0
        for batch in batched_values:
            count += 1
            time.sleep(sleep_time)
            try:
                print(batch)
                translated_batch = azure_translate(batch)

                for i in range(len(batch)):
                    translate_cache[batch[i]] = translated_batch[i]

                print(translated_batch)
                print("Translate batch %s of %s." % (count, len(batched_values)))
            except Exception as e:
                for i in range(len(batch)):
                    translate_cache[batch[i]] = batch[i]
                print("Error: translate batch %s failed." % count)

    _store_translate_cache(project_name, translate_cache)

    translated = {}
    for key in origin:
        if origin[key] in translate_cache:
            translated[key] = translate_cache[origin[key]]
        else:
            translated[key] = origin[key]

    with open(translate_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(translated, ensure_ascii=False))

