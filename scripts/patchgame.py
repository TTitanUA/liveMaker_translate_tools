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
from constants import PROJECTS_DIR, PROJECT_GAME_DIR, PROJECT_RESULT_DIR
import shutil
from livemaker.cli.lmpatch import lmpatch


def _copy_game_files(game_dir, result_dir):
    """Copy game files from project_dir to game_dir and result_dir."""
    print(f"Copying game files from {game_dir} to {result_dir} ...")
    shutil.copytree(game_dir, result_dir, dirs_exist_ok=True)


def patch_game(project_name, main_file):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    game_dir = PurePath(project_dir, PROJECT_GAME_DIR)
    result_dir = PurePath(project_dir, PROJECT_RESULT_DIR)
    main_file = PurePath(project_dir, PROJECT_RESULT_DIR, main_file)

    _copy_game_files(game_dir, result_dir)

    path = Path(result_dir)
    for subpath in path.rglob('0*.lsb'):

        try:
            print(main_file, subpath)
            lmpatch(main_file, subpath)
        except Exception as e:
            print("Warn: %s" % e)
