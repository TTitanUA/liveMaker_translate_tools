from scripts.extract import extract_game_data
from scripts.lsbtocsv import lsb_to_csv
from scripts.csvtojson import csv_to_json
from scripts.translate import translate
from scripts.inserttranslateincsv import insert_translate_to_csv
from scripts.patchlsb import patch_lsb_files
from scripts.patchgame import patch_game

project_name = "my_project"
main_file = "game.exe"

stage = "none"

if stage == "extract":
    extract_game_data(project_name, main_file)
    lsb_to_csv(project_name)
    csv_to_json(project_name)

if stage == "translate":
    translate(project_name)

if stage == "insert":
    insert_translate_to_csv(project_name)

if stage == "patch":
    patch_lsb_files(project_name)
    patch_game(project_name, main_file)

