from pathlib import PurePath
from pathlib import Path
from constants import PROJECTS_DIR, PROJECT_TRANSLATE_DIR, TEXT_ORIGIN_FILE
import csv
import json


def _read_csv_as_dict(csv_file, from_column=3):
    csv_data = dict()
    with open(csv_file, newline="\n", encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in csv_reader:
            if len(row) <= from_column:
                continue
            if row[from_column] == "":
                continue
            if row[from_column] == "\r\n":
                continue
            if row[0] == "ID":
                continue
            if row[0] in csv_data:
                continue
            print(row[from_column])
            csv_data[row[0]] = row[from_column]
    return csv_data


def csv_to_json(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    translate_dir = PurePath(project_dir, PROJECT_TRANSLATE_DIR)

    try:
        Path(translate_dir).exists()
    except OSError:
        print("Error: Translate directory %s not found." % translate_dir)
        return

    path = Path(translate_dir)
    result = dict()
    for subpath in path.rglob('*.csv'):
        print(subpath)
        result.update(_read_csv_as_dict(subpath))

    with open(Path(translate_dir, TEXT_ORIGIN_FILE), 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))
