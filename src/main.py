"""
Entry point of the cli tool.
"""

"""
Something to have a look at,
https://stackoverflow.com/questions/14597466/custom-tab-completion-in-python-argparse
"""

import argparse
import logging
import os

import ColorLoggingFormatter
import rename_functions
from tqdm import tqdm


def setup_argparse():
    """
    Setup of argparse. All needed arguments are defined.
    :return: the retrieved arguments are returned
    """
    parser = argparse.ArgumentParser(description="Rename all photos in a directory and it subdirectories.")
    parser.add_argument("path", help="the path where the photos are located")
    # This way only -s or -a can be defined and not both
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--suffix", help="specify a suffix for all photos", dest="suffix")
    group.add_argument("-a", "--autosuffix", help="take the device from the exif data as the suffix",
                       action="store_true", dest="autosuffix")
    parser.add_argument("-p", "--progress", help="display a progressbar at the bottom of the screen. WARNING does not "
                                                 "work wel with all verbosity levels!!", action="store_true",
                        dest="progress")
    parser.add_argument("-v", "--verbosity", help="increase output verbosity, default=WARNING",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], dest="verbosity", default="WARNING")
    arguments = parser.parse_args()
    return arguments


def setup_logging(logLevel):
    """
    Setup of the application logger.
    :param logLevel: level to set the logger
    """
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(ColorLoggingFormatter.ColorLoggingFormatter())
    myLogger = logging.getLogger("my_app")
    myLogger.setLevel(logLevel)
    myLogger.addHandler(logHandler)


if __name__ == '__main__':
    args = setup_argparse()
    setup_logging(args.verbosity)
    logger = logging.getLogger("my_app")

    # For testing purposes
    # logger.debug("test message debug")
    # logger.info("This is just info")
    # logger.warning("This is a WARNING")
    # logger.error("ERROR, watch out")
    # logger.critical("RUN!!")

    # Output basic information
    logger.info("Path: " + args.path)
    if args.suffix is not None:
        logger.info("Suffix: " + args.suffix)
    elif args.autosuffix:
        logger.info("Suffix: auto")
    else:
        logger.info("Suffix: none")

    # The beginning of the whole process
    folder_path = args.path
    if args.progress:
        numSubdirs = rename_functions.get_num_dirs(folder_path)
        print("\033[94m There are", numSubdirs, "progressbars to complete! \x1b[0m")
    for dirPath, dirNames, filenames in os.walk(folder_path):
        if args.progress:
            files = tqdm(filenames)
            files.set_description("Files")
        else:
            files = filenames
        for f in files:
            filePath = os.path.join(dirPath, f)
            date_taken = rename_functions.gets_date_taken(filePath)
            if date_taken == "0000:00 0000:0000":
                logger.warning("No file name change fore file with name", f, "in folder", dirPath,
                               "\n ERROR NO DATE TAKEN IN EXIF DATA (' + f + ')")
                continue
            elif args.autosuffix:
                device = rename_functions.get_device_from_exif(filePath)
                if device is not None:
                    new_name = rename_functions.date_taken_new_name(date_taken) + "--" + device.replace(' ', '_')
            elif args.suffix is not None:
                new_name = rename_functions.date_taken_new_name(date_taken) + "--" + args.suffix.replace(' ', '_')
            else:
                new_name = rename_functions.date_taken_new_name(date_taken)
            logger.debug(new_name)
            rename_functions.change_name(dirPath, f, new_name)
