"""
Entry point of the cli tool.
"""

import argparse
import logging
import ColorLoggingFormatter
import rename_functions


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
    parser.add_argument("-v", "--verbosity", help="increase output verbosity, default=WARNING",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], dest="verbosity", default="WARNING")
    argmunets = parser.parse_args()
    return argmunets


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

    logger.info("Path: " + args.path)
    if args.suffix is not None:
        logger.info("Suffix: " + args.suffix)
    else:
        logger.info("Suffix: auto")
    rename_functions.change_names_in_folder(args)
