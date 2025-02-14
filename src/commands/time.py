import datetime
import logging
import os
import subprocess
import sys

from tqdm import tqdm

from ColorLoggingFormatter import Colors
from functions import generalFunctions, timeFunctions


def time(args):
    logger = logging.getLogger("my_app")

    # Check if exiftool is available, if not -> abort.
    status, result = subprocess.getstatusoutput("exiftool -h")
    if status != 0:
        logger.ERROR("Command 'exiftool' not found!")
        sys.exit(-1)

    # # The beginning of the whole process
    # Init variables
    folder_path = args.path
    progressCounter = 0
    numSubdirs = 0
    # # Print the amount a directories there are, this is also the amount of progress bars
    if args.progress:
        progressCounter = 1
        numSubdirs = generalFunctions.get_num_dirs(folder_path)
        if numSubdirs == 1:
            print(Colors.LIGHT_BLUE.value + "There is 1 progressbar to complete!" + Colors.RESET.value)
        else:
            print(Colors.LIGHT_BLUE.value + "There are", numSubdirs, "progressbars to complete!" + Colors.RESET.value)

    # Execute loop over photos
    for dirPath, _dirNames, filenames in os.walk(args.path):
        # # Sort the files
        sorted_files = sorted(filenames)
        # # Start a progress bar if enabled with the argument
        if args.progress:
            files = tqdm(sorted_files)
            files.set_description("Progressbar " + str(progressCounter) + "/" + str(numSubdirs))
            progressCounter += 1
        else:
            files = sorted_files
        for file in files:
            logger.debug("NEXT FILE")
            old_date = generalFunctions.get_date_from_EXIF(dirPath, file)
            if old_date == -1:
                continue
            new_date = timeFunctions.asking_new_date if args.fullTime else old_date + datetime.timedelta(hours=args.time_adj)
            timeFunctions.change_date_from_EXIF(dirPath, file, new_date, args.overwrite_original)
