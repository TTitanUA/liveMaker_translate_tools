from pathlib import PurePath
from pathlib import Path
import os
from constants import PROJECTS_DIR, PROJECT_TRANSLATE_DIR, PROJECT_EXTRACT_DIR, CSV_HEADER
import csv
from livemaker.exceptions import BadLsbError, LiveMakerException
from livemaker.lsb import LMScript
from livemaker.project import PylmProject


def _extractcsv(lsb_file, csv_file, encoding='utf-8', overwrite=True, append=False):
    """Extract text from the given LSB file to a CSV file.

    You can open this CSV file for translation in most spreadsheet programs (Excel, Open/Libre Office Calc, etc).
    Just remember to choose comma as delimiter and " as quotechar.

    NOTE: If you are using Excel and UTF-8 text, you must also specify --encoding=utf-8-sig, since Excel requires
    UTF-8 with BOM to handle UTF-8 properly.

    You can use the --append option to add the text data from this lsb file to a existing csv.
    With the --overwrite option an existing csv will be overwritten without warning.

    NOTE: Formatting tags will be lost when using this command in conjunction with insertcsv.
    For translating games which use formatting tags, you may need to work directly with LNS scripts
    using the extract and insert/batchinsert commands.
    """
    lsb_file = Path(lsb_file)
    print(f"Extracting {lsb_file} ...")

    try:
        pylm = PylmProject(lsb_file)
        call_name = pylm.call_name(lsb_file)
    except LiveMakerException:
        pylm = None
        call_name = None

    try:
        with open(lsb_file, "rb") as f:
            lsb = LMScript.from_file(f, call_name=call_name, pylm=pylm)
    except BadLsbError as e:
        raise Exception(f"Failed to parse file: {e}")

    csv_data = []
    for id_, block in lsb.get_text_blocks():
        csv_data.append([str(id_), id_.name, block.name_label, block.text, None])

    if len(csv_data) == 0:
        raise Exception("No text data found.")

    if Path(csv_file).exists():
        if not overwrite and not append:
            raise Exception(f"File {csv_file} already exists. Please use --overwrite or --append option.")

    elif append:
        print(f"File {csv_file} does not exist, but --append specified. A new file will be created.")
        append = False

    with open(csv_file, ("a" if append else "w"), newline="\n", encoding=encoding) as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not append:
            csv_writer.writerow(CSV_HEADER)
        for row in csv_data:
            csv_writer.writerow(row)

    print(f"Extracted {len(csv_data)} text blocks.")


def _extract_strings(extract_path, lsb_file, csv_file, encoding='utf-8', overwrite=False, append=True):
    """Extract strings from the given LSB file to a CSV file.

    You can open this CSV file for translation in most spreadsheet programs (Excel, Open/Libre Office Calc, etc).
    Just remember to choose comma as delimiter and " as quotechar.

    NOTE: If you are using Excel and UTF-8 text, you must also specify --encoding=utf-8-sig, since Excel requires
    UTF-8 with BOM to handle UTF-8 properly.

    You can use the --append option to add the text data from this lsb file to a existing csv.
    With the --overwrite option an existing csv will be overwritten without warning.

    NOTE: this program also extracts strings used in menu functions. DO NOT USE this function for translating menu items.
    The menu will not work!

    NOTE: be very careful with translating strings. Changing the wrong text can break game functionality!
    Lines you would not translate have to be left blank.
    """

    relative_path = Path(lsb_file).relative_to(extract_path)

    with open(lsb_file, "rb") as f:
        try:
            lsb:LMScript = LMScript.from_file(f)
        except LiveMakerException as e:
            raise Exception("Could not open LSB file: {}".format(e))

    csv_data = []

    for c in lsb.commands:
        calc = c.get("Calc")
        if calc:
            for s in calc["entries"]:
                op = s["operands"][0]
                if op["type"] == "Str":
                    csv_data.append(["pylm:string:{}:{}:{}".format(relative_path, c.LineNo, s["name"]), None, c, op["value"]])

    if len(csv_data) == 0:
        raise Exception("No strings found.")

    if Path(csv_file).exists():
        if not overwrite and not append:
            raise Exception("File {} already exists. Please use --overwrite or --append option.".format(csv_file))
    elif append:
        print("File {} does not exist, but --append specified. A new file will be created.".format(csv_file))
        append = False

    with open(csv_file, ("a" if append else "w"), newline="\n", encoding=encoding) as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not append:
            csv_writer.writerow(CSV_HEADER)
        for row in csv_data:
            csv_writer.writerow(row)

    print(f"Extracted {len(csv_data)} strings.")


def lsb_to_csv(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    extract_dir = PurePath(project_dir, PROJECT_EXTRACT_DIR)
    translate_dir = PurePath(project_dir, PROJECT_TRANSLATE_DIR)

    try:
        Path(extract_dir).exists()
    except OSError:
        print("Error: Extract directory %s not found." % extract_dir)
        return

    try:
        if not os.path.exists(translate_dir):
            os.mkdir(translate_dir)
    except OSError:
        print("Error: Creation of the directory %s failed." % translate_dir)

    path = Path(extract_dir)
    for subpath in path.rglob('0*.lsb'):
        translate_path = PurePath(str(translate_dir), str(subpath).replace(str(extract_dir), '.').replace('.lsb', '.csv'))
        try:
            _extractcsv(subpath, translate_path)
            # _extract_strings(extract_dir, subpath, translate_path)
        except Exception as e:
            print("Warn: %s" % e)
