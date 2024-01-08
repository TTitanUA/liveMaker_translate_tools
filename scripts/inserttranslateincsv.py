import json
from pathlib import PurePath
from pathlib import Path
from constants import PROJECTS_DIR, PROJECT_TRANSLATE_DIR
import csv


def _save_translate_values(csv_file, translate):
    csv_data = []

    # load the csv file
    with open(csv_file, newline="\n", encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in csv_reader:
            csv_data.append(row)

    for row in csv_data:
        if len(row) <= 3:
            continue
        if row[3] == "":
            continue
        if row[3] == "\r\n":
            continue
        if row[0] == "ID":
            continue

        if row[0] in translate:
            if len(row) < 5:
                row.append("")
            row[4] = translate[row[0]]

    with open(csv_file, 'w', newline="\n", encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        for row in csv_data:
            csv_writer.writerow(row)


def insert_translate_to_csv(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    translate_dir = PurePath(project_dir, PROJECT_TRANSLATE_DIR)
    translate_file = Path(translate_dir, 'translate.json')

    try:
        Path(translate_file).exists()
    except:
        print("Error: translate_file file not found.")
        return

    with open(translate_file, 'r', encoding='utf-8') as f:
        translate = json.load(f)

    path = Path(translate_dir)
    for subpath in path.rglob('*.csv'):
        print(subpath)
        _save_translate_values(subpath, translate)
        print("CSV saved.")
