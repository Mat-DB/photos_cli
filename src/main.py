#!/usr/bin/env python
"""Entry point of the cli tool.

Convention:
 # means commended code
 # # means a comment to understand the code
"""

import argparse
import logging
import os

import ColorLoggingFormatter
import rename_functions
from tqdm import tqdm

"""
Something to have a look at,
https://stackoverflow.com/questions/14597466/custom-tab-completion-in-python-argparse
"""


def setup_argparse():
    """Setup of argparse. All needed arguments are defined.

    Returns:
        the retrieved arguments are returned
    """
    parser = argparse.ArgumentParser(description="Rename all photos in a directory and it subdirectories.")
    parser.add_argument("path", help="the path where the photos are located")
    # # A group makes sure only -s or -a can be defined and not both
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--suffix", help="specify a suffix for all photos", dest="suffix")
    group.add_argument(
        "-a",
        "--autosuffix",
        help="take the device from the exif data as the suffix",
        action="store_true",
        dest="autosuffix",
    )
    parser.add_argument(
        "-p",
        "--progress",
        help="display a progressbar at the bottom of the screen. WARNING does not " "work wel with all verbosity levels!!",
        action="store_true",
        dest="progress",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        help="increase output verbosity, default=WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        dest="verbosity",
        default="WARNING",
    )
    arguments = parser.parse_args()
    return arguments


def setup_logging(logLevel):
    """Setup of the application logger.

    Args:
        logLevel: level to set the logger
    """
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(ColorLoggingFormatter.ColorLoggingFormatter())
    myLogger = logging.getLogger("my_app")
    myLogger.setLevel(logLevel)
    myLogger.addHandler(logHandler)


def check_extension(extension):
    return extension.upper() in ["TIFF", "TIF", "JPEG", "JPG", "PNG", "WEBP", "HEIC"]


if __name__ == "__main__":
    # # Setup of the application
    args = setup_argparse()
    setup_logging(args.verbosity)
    logger = logging.getLogger("my_app")

    # # For testing purposes
    # logger.debug("test message debug")
    # logger.info("This is just info")
    # logger.warning("This is a WARNING")
    # logger.error("ERROR, watch out")
    # logger.critical("RUN!!")

    # # Output basic information
    logger.info("Path: " + args.path)
    if args.suffix is not None:
        logger.info("Suffix: " + args.suffix)
    elif args.autosuffix:
        logger.info("Suffix: auto")
    else:
        logger.info("Suffix: no suffix")

    # # The beginning of the whole process
    # Init variables
    folder_path = args.path
    filenames_dict = {}
    progressCounter = 0
    numSubdirs = 0
    # # Print the amount a directories there are, this is also the amount of progress bars
    if args.progress:
        progressCounter = 1
        numSubdirs = rename_functions.get_num_dirs(folder_path)
        print("\033[94m There are", numSubdirs, "progressbars to complete! \x1b[0m")
    # # Walking over every file and directory in the given directory
    for dirPath, _dirNames, filenames in os.walk(folder_path):
        # # Sort the files
        sorted_files = sorted(filenames)
        # # Start a progress bar if enabled with the argument
        if args.progress:
            files = tqdm(sorted_files)
            files.set_description("Progressbar " + str(progressCounter) + "/" + str(numSubdirs))
            progressCounter += 1
        else:
            files = sorted_files
        # # Walk over the files
        for file in files:
            logger.debug("NEXT FILE")
            filePath = os.path.join(dirPath, file)
            extension = str(file).split(".")[-1]
            if not check_extension(extension):
                logger.warning("The following file type is not supported, " + extension)
                logger.warning("Skipping file, " + str(filePath))
                continue
            date_taken = rename_functions.gets_date_taken(filePath)
            # # When there is no date taken the file will not be renamed
            # # Also check if any suffix is needed
            if date_taken == "0000:00 0000:0000":
                logger.warning("No file name change fore file with name " + file + " in folder" + dirPath)
                logger.warning("ERROR NO DATE TAKEN IN EXIF DATA (file=" + file + ")")
                continue
            elif args.autosuffix:
                device = rename_functions.get_device_from_exif(filePath)
                if device is not None:
                    new_name = rename_functions.date_taken_new_name(date_taken) + "--" + device.replace(" ", "_")
                else:
                    logger.error("No device name found for file: " + str(os.path.join(dirPath, file)))
                    logger.error("This file is NOT renamed.")
                    continue
            elif args.suffix is not None:
                new_name = rename_functions.date_taken_new_name(date_taken) + "--" + args.suffix.replace(" ", "_")
            else:
                new_name = rename_functions.date_taken_new_name(date_taken)
            logger.debug(new_name)
            # # Check if the file f is in the dict.
            # # If yes then the file already has been renamed and the script can go to the next file
            if file in filenames_dict:
                continue
            # # If the file name is equal to the new name than renaming is not needed
            if str(file).split(".")[0] == new_name:
                logger.info("File already has the correct name, " + str(filePath))
                continue
            # # Check if there are one or more photos made on the same second and rename correctly
            if new_name not in filenames_dict:
                rename_functions.change_name(dirPath, file, new_name)
                # # Ad the file to the dict
                filenames_dict[new_name] = 1
            elif filenames_dict.get(new_name) == 1:
                logger.error("On " + new_name + " there have been at least 2 photos been made")
                logger.warning("Trying to add (1) and (2) to the the end of the photos name")
                # # Rename the current photo to the new name with (2) behind it
                # # Check if the file already has the correct name
                new_name2 = new_name + "(2)"
                if str(file).split(".")[0] == new_name2:
                    logger.info("File already has the correct name, " + str(filePath))
                else:
                    rename_functions.change_name(dirPath, file, new_name2)
                # # Rename the already existing photo to the new name with (1) behind it
                sameFile_newName = new_name + "(1)"
                rename_functions.change_name(dirPath, (new_name + "." + extension), sameFile_newName)
                # # Update the amount of photos made on that moment
                filenames_dict[new_name] = filenames_dict[new_name] + 1
            else:
                logger.warning("On " + new_name + " there have been more than 2 photos been made")
                logger.warning("Trying to add (" + str(filenames_dict.get(new_name)) + ") to the photo name")
                # # More than 2 photos have been on the same second
                new_name2 = new_name + "(" + str(filenames_dict[new_name] + 1) + ")"
                if str(file).split(".")[0] == new_name2:
                    logger.info("File already has the correct name, " + str(filePath))
                else:
                    rename_functions.change_name(dirPath, file, new_name2)
                # # Update the amount of photos made on that moment
                filenames_dict[new_name] = filenames_dict[new_name] + 1
