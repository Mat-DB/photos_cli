import datetime
import logging
import os

from tqdm import tqdm

from functions import adjust_time, generalFunctions


def time(args):
    logger = logging.getLogger("my_app")
    old_date = generalFunctions.get_date_from_EXIF("/home/matthias/Desktop", "test.JPG")
    new_date = adjust_time.asking_new_date if args.fullTime else old_date + datetime.timedelta(hours=args.time_adj)
    logger.info("old time:", old_date, ", new time:", new_date)

    # # The beginning of the whole process
    # Init variables
    folder_path = args.path
    progressCounter = 0
    numSubdirs = 0
    # # Print the amount a directories there are, this is also the amount of progress bars
    if args.progress:
        progressCounter = 1
        numSubdirs = generalFunctions.get_num_dirs(folder_path)
        print("\033[94m There are", numSubdirs, "progressbars to complete! \x1b[0m")
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
            ...
