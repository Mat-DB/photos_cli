"""This file holds all functions regarding renaming photos."""

import logging
import os

import exifread


def change_name(path, old_name, new_name, dry_run):
    """Change the name of a file and appends a number if the file exists.

    Args:
        path: path of the file
        old_name: old name of the file with extension
        new_name: new name of the file WITHOUT extension
    """
    logger = logging.getLogger("my_app")
    old = os.path.join(path, old_name)
    file_split = old_name.split(".")
    logger.debug("Splitted file: " + str(file_split))
    logger.debug("Extension: " + str(file_split[-1]))
    extension = file_split[-1]
    if new_name == "" or new_name is None:
        logger.critical("The new filename cannot be nothing!")
        return
    new = os.path.join(path, (new_name + "." + extension))
    if os.path.isfile(new):
        logger.error("File: " + str(old) + " already exists, not changed!")
        logger.critical("On unix machines " + str(new) + " would be overwritten!!")
        return
    try:
        if not dry_run:
            os.rename(old, new)
        logger.info("Name changed from " + old_name + " to " + new_name + "." + extension + " in folder " + path)
    except FileExistsError as existsError:
        logger.debug(str(existsError))
        logger.error("File:" + str(old) + " already exists, not changed!")
    except FileNotFoundError as notFoundError:
        logger.debug(str(notFoundError))
        logger.error("File:" + str(old) + " not found!")


def date_taken_new_name(date_taken):
    """Creates a new from the date taken in the default datetime format YYMMDD_hhmmss.

    Args:
        date_taken: date taken from exif data

    Returns:
        new file name in default datetime format (without extension)
    """
    dateArray = date_taken.split(" ")
    date = dateArray[0].split(":")
    time = dateArray[1].split(":")
    # YearMonthDay_HourMinutesSeconds
    new_name = date[0] + date[1] + date[2] + "_" + time[0] + time[1] + time[2]
    return new_name


def gets_date_taken(file_path):
    """Get the date taken from a picture.

    Args:
        file_path: path to picture

    Returns:
        date taken from exif
    """
    with open(file_path, "rb") as currentFile:
        tags = exifread.process_file(currentFile)  # type: ignore  # This is correct following the documentation https://pypi.org/project/ExifRead/
        shootTimeTag = "EXIF DateTimeOriginal"
        if shootTimeTag in tags:
            shootTime = str(tags[shootTimeTag])
            if not shootTime:
                shootTime = "0000:00 0000:0000"
        else:
            shootTime = "0000:00 0000:0000"
        return shootTime


def get_device_from_exif(filePath):
    """_summary_.

    Args:
        filePath: _description_

    Returns:
        _description_
    """
    logger = logging.getLogger("my_app")
    with open(filePath, "rb") as currentFile:
        tags = exifread.process_file(currentFile)  # type: ignore  # This is correct following the documentation https://pypi.org/project/ExifRead/
        # logger.debug(tags.keys())
        # logger.debug("END FILE")
        deviceTag = "Image Model"
        if deviceTag in tags:
            logger.debug("Tag Image Model: " + str(tags["Image Model"]))
            deviceName = str(tags[deviceTag])
            if not deviceName:
                deviceName = None
        else:
            logger.debug("Tag Image Model does not exist")
            deviceName = None
        return deviceName
