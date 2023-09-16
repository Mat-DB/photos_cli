"""
This file holds all functions regarding renaming photos.
"""
import logging
import os
import pathlib
import exifread


def change_name(path, old_name, new_name):
    """

    :param path:
    :param old_name:
    :param new_name:
    :return:
    """
    logger = logging.getLogger("my_app")
    old = os.path.join(path, old_name)
    file_split = old_name.split('.')
    logger.debug("Splitted file: " + str(file_split))
    logger.debug("Extension: " + str(file_split[-1]))
    extension = file_split[-1]
    new = os.path.join(path, (new_name + '.' + extension))
    try:
        os.rename(old, new)
        logger.info("Name changed from " + old_name + " to " + new_name + '.' + extension + " in folder " + path)
    except FileExistsError as error:
        logger.error(str(error) + '\n' + old + " changed with (1) behind the name!")
        new2 = os.path.join(path, (new_name + "(1)." + extension))
        try:
            os.rename(old, new2)
            logger.info("Name changed from " + old_name + " to " + new_name + '.' + extension + " in folder " + path)
        except FileExistsError as error:
            logger.error(error, '\n' + str(old), "not changed!")


def date_taken_new_name(date_taken):
    """

    :param date_taken:
    :return:
    """
    dateArray = date_taken.split(" ")
    date = dateArray[0].split(":")
    time = dateArray[1].split(":")
    new_name = date[0] + '-' + date[1] + '-' + date[2] + '--' + time[0] + '-' + time[1] + '-' + time[2]
    return new_name


def gets_date_taken(file_path):
    """

    :param file_path:
    :return:
    """
    currentFile = open(file_path, 'rb')
    tags = exifread.process_file(currentFile)
    shootTimeTag = "EXIF DateTimeOriginal"
    if shootTimeTag in tags:
        shootTime = str(tags[shootTimeTag])
        if not shootTime:
            shootTime = "0000:00 0000:0000"
    else:
        shootTime = "0000:00 0000:0000"
    return shootTime


def get_device_from_exif(filePath):
    logger = logging.getLogger("my_app")
    currentFile = open(filePath, 'rb')
    tags = exifread.process_file(currentFile)
    # logger.debug(tags.keys())
    # logger.debug("END FILE")
    logger.debug("Tag Image Model: " + str(tags["Image Model"]))
    deviceTag = "Image Model"
    if deviceTag in tags:
        deviceName = str(tags[deviceTag])
        if not deviceName:
            deviceName = None
    else:
        deviceName = None
    return deviceName


def get_num_dirs(dir):
    count = 0
    path = pathlib.Path(dir)
    for subdir in path.glob('**/'):
        if subdir.is_dir():
            count += 1
    return count

