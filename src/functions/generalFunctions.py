import datetime
import logging
import os
import pathlib

import piexif


def check_extension(extension):
    return extension.upper() in ["TIFF", "TIF", "JPEG", "JPG", "PNG", "WEBP", "HEIC"]


def get_num_dirs(dir):
    """_summary_.

    Args:
        dir: _description_

    Returns:
        _description_
    """
    count = 0
    path = pathlib.Path(dir)
    for subdir in path.glob("**/"):
        if subdir.is_dir():
            count += 1
    return count


def get_date_from_EXIF(path, file_name):
    logger = logging.getLogger("my_app")
    file_path = os.path.join(path, file_name)
    try:
        exif_dict = piexif.load(file_path)
        dateTime = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
        if not dateTime:
            logger.error(f"No 'DateTimeOriginal' field found in {path / file_name}")
            return -1
        dateTime = dateTime.decode("utf-8")
        dateTimeObj = datetime.datetime.strptime(dateTime, "%Y:%m:%d %H:%M:%S")
        return dateTimeObj
    except Exception as e:
        logger.error(f"Failed to process {path / file_name}: {e}")
