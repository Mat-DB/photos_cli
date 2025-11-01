#!/usr/bin/env python
"""Entry point of the cli tool.

Convention:
 # means commended code
 # # means a comment to understand the code
"""

import argparse
import logging
import sys

# import argcomplete
import ColorLoggingFormatter
from commands.rename import rename
from commands.time import time

"""
Something to have a look at,
https://stackoverflow.com/questions/14597466/custom-tab-completion-in-python-argparse

Sources,
https://stackoverflow.com/questions/18668227/argparse-subcommands-with-nested-namespaces
https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu

"""
# CLI tool version
version = "2.0"


def setup_argparse():
    """Setup of argparse. All needed arguments are defined.

    Returns:
        the retrieved arguments are returned
    """
    main_parser = argparse.ArgumentParser(prog="photos_cli", description="CLI tool to batch manipulate photos.")

    # General arguments
    general_args_parser = argparse.ArgumentParser(add_help=False)
    general_args_parser.add_argument(
        "-p",
        "--progress",
        help="display a progressbar at the bottom of the screen. WARNING does not work wel with all verbosity levels!!",
        action="store_true",
        dest="progress",
    )
    general_args_parser.add_argument(
        "-v",
        "--verbosity",
        help="increase output verbosity, default=WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        dest="verbosity",
        default="WARNING",
    )
    general_args_parser.add_argument("-P", "--path", help="the path where the photos are located", required=True)

    # create sub-parser
    sub_parsers = main_parser.add_subparsers(help="available subcommands", dest="command")

    # Create a subparser for the "time" command
    timeParser = sub_parsers.add_parser(
        "time",
        help="adjust the hour in the date taken in EXIF data",
        description="description of the subparser time command",
        parents=[general_args_parser],
    )
    time_adj_group = timeParser.add_mutually_exclusive_group(required=True)
    time_adj_group.add_argument("-t", "--time", type=int, help="in hours the amount to adjust the date taken", dest="time_adj")
    time_adj_group.add_argument("--fullTime", help="specify a full time for ALL pictures", action="store_true", dest="fullTime")
    timeParser.add_argument(
        "-O",
        "--overwrite_original",
        help="CAREFUL, overwrite the original FILE. Instead of preserving it by adding '_original' to the filename",
        action="store_false",  # Default set to False, do not overwrite!
        dest="overwrite_original",
    )

    # Create a subparser for the "rename" command
    renameParser = sub_parsers.add_parser(
        "rename",
        help="rename all photos, according to the options set",
        description="description of the subparser rename command",
        parents=[general_args_parser],
    )

    # A group makes sure only -s or -a can be defined and not both
    suffixGroup = renameParser.add_mutually_exclusive_group()
    suffixGroup.add_argument("-s", "--suffix", help="specify a suffix for all photos", dest="suffix")
    suffixGroup.add_argument(
        "-a",
        "--autosuffix",
        help="take the device from the exif data as the suffix",
        action="store_true",
        dest="autosuffix",
    )
    suffixGroup.add_argument(
        "-d",
        "--add-date",
        help="Special format, add date in front of file name. Eg: YYYYMMDD-<original_name>.<extension>",
        action="store_true",
        dest="date_in_front",
    )

    # An option to do a dry run, do not rename just output
    renameParser.add_argument(
        "-n",
        "--dry-run",
        help="Do a dry run. Do not rename, just output if debug is INFO",
        action="store_true",
        dest="dry_run",
    )

    main_parser.add_argument("--version", help="show version and exit", action="version", version=version)
    # argcomplete.autocomplete(main_parser)
    arguments = main_parser.parse_args()
    if arguments.command is None:
        print(
            ColorLoggingFormatter.Colors.BOLD_RED.value
            + "ERROR: no argument specified.\nHelp is printed instead!!"
            + ColorLoggingFormatter.Colors.RESET.value
        )
        main_parser.print_help()
        print(
            ColorLoggingFormatter.Colors.BOLD_RED.value
            + "ERROR: no argument specified.\nHelp is printed instead!! (see above)"
            + ColorLoggingFormatter.Colors.RESET.value
        )
        sys.exit(-1)
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


if __name__ == "__main__":
    # # Setup of the application
    args = setup_argparse()
    print(args)

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

    if args.command == "time":
        logger.info("time command selected")
        time(args)
    elif args.command == "rename":
        logger.info("rename command selected")
        rename(args)
