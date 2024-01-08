import json
from pathlib import PurePath
from pathlib import Path
from livemaker.exceptions import BadLsbError, BadTextIdentifierError, LiveMakerException
from livemaker.lsb import LMScript
from livemaker.lsb.command import BaseComponentCommand, Calc, CommandType, Jump, LabelReference
from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType
from livemaker.lsb.menu import LPMSelectionChoice
from livemaker.lsb.novel import LNSCompiler, LNSDecompiler, TWdChar, TWdOpeReturn
from livemaker.lsb.translate import TextBlockIdentifier, TextMenuIdentifier, make_identifier
from livemaker.project import PylmProject
from constants import PROJECTS_DIR, PROJECT_TRANSLATE_DIR, PROJECT_RESULT_DIR, PROJECT_EXTRACT_DIR
import csv
import shutil
import sys

def _patch_csv_text(lsb, lsb_file, csv_data, verbose=False):
    """Patch text lines in the given lsb file using csv_data."""
    text_objects = []
    untranslated = 0

    for row, (id_str, name, context, orig_text, translated_text) in enumerate(csv_data):
        if "pylm:string" in id_str:
            continue

        try:
            id_ = make_identifier(id_str)
        except BadTextIdentifierError as e:
            if row > 0:
                # ignore possible header row
                print(f"Ignoring invalid text ID: {e}")
            continue

        if not isinstance(id_, TextBlockIdentifier):
            continue

        if id_.filename == lsb_file.name:
            if translated_text:
                if verbose:
                    print(f"{id_}: '{orig_text}' -> '{translated_text}'")
                text_objects.append((id_, translated_text))
            else:
                if verbose:
                    print(f"{id_} Ignoring untranslated text '{orig_text}'")
                untranslated += 1

    translated, failed = lsb.replace_text(text_objects)

    return translated, failed, untranslated


def _patch_csv_string(lsb, relative_file_name, csv_data, verbose=False):
    """Patch text lines in the given lsb file using csv_data."""
    string_translated = 0

    for c in lsb.commands:
        calc = c.get("Calc")
        if calc:
            for s in calc["entries"]:
                op = s["operands"][0]
                if op["type"] == "Str":
                    for line in csv_data:
                        if len(line) < 4: continue
                        if line[3] == "": continue
                        if line[4] == "": continue
                        if line[0] == "pylm:string:{}:{}:{}".format(relative_file_name, c.LineNo, s["name"]):
                            op.value = line[4]
                            string_translated += 1

    return string_translated


def _insertcsv(lsb_file, csv_file, encoding, new_lsb_file, extract_path, verbose):
    """Apply translated text lines from the given CSV file to given LSB file.

    CSV_FILE should be a file previously created by the extractcsv command, with added translations.
    --encoding option must match the values were used for extractcsv.

    The original LSB file will be backed up to <lsb_file>.bak unless the --no-backup option is specified.
    """
    lsb_file = Path(lsb_file)
    relative_path = Path(lsb_file).relative_to(extract_path)
    print(f"Patching {lsb_file} ...")

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
        sys.exit(f"Failed to parse file: {e}")

    csv_data = []

    with open(csv_file, newline="\n", encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in csv_reader:
            if (len(row) < 5):
                row.append(row[3])
            csv_data.append(row)

    # string_translated = _patch_csv_string(lsb, relative_path, csv_data, verbose)
    # print(f"  Translated {string_translated} strings")

    translated, failed, untranslated = _patch_csv_text(lsb, lsb_file, csv_data, verbose)

    print(f"  Translated {translated} lines")
    print(f"  Failed to translate {failed} lines")
    print(f"  Ignored {untranslated} untranslated lines")
    if not translated:
        return

    try:
        new_lsb_data = lsb.to_lsb()
        with open(new_lsb_file, "wb") as f:
            f.write(new_lsb_data)
        print("Wrote new LSB.")
    except LiveMakerException as e:
        sys.exit(f"Could not generate new LSB file: {e}")


def _patch_lsb(csv_file, result_dir, translate_dir, extract_dir):
    lsb_file = csv_file.replace('.csv', '.lsb').replace(translate_dir, extract_dir)
    new_lsb_file = lsb_file.replace(extract_dir, result_dir)

    if not Path(lsb_file).exists():
        print("Error: LSB file %s not found." % lsb_file)
        return

    _insertcsv(lsb_file, csv_file, 'utf-8', new_lsb_file, extract_dir, True)


def patch_lsb_files(project_name):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    extract_dir = PurePath(project_dir, PROJECT_EXTRACT_DIR)
    translate_dir = PurePath(project_dir, PROJECT_TRANSLATE_DIR)
    result_dir = PurePath(project_dir, PROJECT_RESULT_DIR)

    if not Path(result_dir).exists():
        Path(result_dir).mkdir(parents=True)

    path = Path(translate_dir)
    for subpath in path.rglob('*.csv'):
        print(subpath)
        _patch_lsb(str(subpath), str(result_dir), str(translate_dir), str(extract_dir))
