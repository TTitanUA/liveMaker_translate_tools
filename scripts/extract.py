from pathlib import PurePath
from pathlib import Path
import os
from io import BytesIO
from PIL import Image
from livemaker import GalImagePlugin
from livemaker.archive import LMArchive
from livemaker.exceptions import BadLiveMakerArchive, LiveMakerException
from constants import PROJECTS_DIR, PROJECT_GAME_DIR, PROJECT_EXTRACT_DIR


def _extract_as_png(lm, info, output_dir, image_format, dry_run, verbose):
    try:
        png_path = info.path.parent.joinpath(f"{info.path.stem}.png")
        if not dry_run:
            data = lm.read(info)
            path = output_dir.joinpath(png_path).expanduser().resolve()
            im = Image.open(BytesIO(data))
            path.parent.mkdir(parents=True, exist_ok=True)
            im.save(path)
        if verbose or dry_run:
            print(png_path)
    except LiveMakerException as e:
        print(f"Error converting {info.path} to PNG: {e}")
        if image_format == "png":
            print("  Original GAL image will be used as fallback.")
            if not dry_run:
                lm.extract(info, output_dir)
            if verbose or dry_run:
                print(info.path)


def _lmar_x(dry_run, image_format, output_dir, verbose, input_file):
    """Extract the specified archive."""
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = Path.cwd()
    try:
        with LMArchive(input_file) as lm:
            for info in lm.infolist():
                try:
                    if info.path.suffix.lower() == ".gal":
                        if image_format in ("gal", "both"):
                            if not dry_run:
                                lm.extract(info, output_dir)
                            if verbose or dry_run:
                                print(info.path)
                        if image_format in ("png", "both"):
                            _extract_as_png(lm, info, output_dir, image_format, dry_run, verbose)
                    else:
                        if not dry_run:
                            lm.extract(info, output_dir)
                        if verbose or dry_run:
                            print(info.path)
                except LiveMakerException as e:
                    print(f"  Error extracting {info.path}: {e}")
    except BadLiveMakerArchive as e:
        print(f"Could not read LiveMaker archive {input_file}: {e}")


def extract_game_data(project_name, main_file):
    project_dir = PurePath(PROJECTS_DIR, project_name)
    main_file = PurePath(project_dir, PROJECT_GAME_DIR, main_file)
    extract_dir = PurePath(project_dir, PROJECT_EXTRACT_DIR)

    try:
        Path(main_file).exists()
    except:
        print("Error: Main file not found.")
        return

    try:
        os.mkdir(extract_dir)
    except OSError:
        print("Error: Creation of the directory %s failed." % extract_dir)

    _lmar_x(False, "gal", extract_dir, False, main_file)
    print("Extraction completed.")
