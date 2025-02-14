import datetime
import logging
import os
import subprocess


def asking_new_date():
    logger = logging.getLogger("my_app")
    new_date_year = int(input("Give the YEAR of the new date: "))
    new_date_month = int(input("Give the MONTH of the new date: "))
    new_date_day = int(input("Give the DAY of the new date: "))
    time_YesNo = input("Do you want to specify the time? Else, time will be set to 00:00:00. (yes or no): ")
    if time_YesNo.lower() == "yes" or time_YesNo.lower() == "y":
        new_date_hour = int(input("Give the HOUR of the new time: "))
        new_date_minute = int(input("give the MINUTES of the new time: "))
        new_date_second = int(input("Give the SECONDS of the new time: "))
    else:
        new_date_hour = 0
        new_date_minute = 0
        new_date_second = 0
    new_date = datetime.datetime(new_date_year, new_date_month, new_date_day, new_date_hour, new_date_minute, new_date_second)
    print("Is this correct?", new_date)
    correct = input("yes or no?: ")
    if correct.lower() == "no" or correct.lower() == "n":
        new_date = asking_new_date()
    logger.info("new date is:", new_date)
    return new_date


def change_date_from_EXIF(path, file_name, new_date, preserve_original):
    logger = logging.getLogger("my_app")
    file_path = os.path.join(path, file_name)
    try:
        # print(file_path)
        # print(new_date.strftime("%Y:%m:%d %H:%M:%S"))
        if preserve_original:
            status, result = subprocess.getstatusoutput(
                [
                    f'exiftool "-AllDates={new_date} -preserve" {path}/{file_name}',
                    new_date.strftime("%Y:%m:%d %H:%M:%S"),
                    path,
                    file_name,
                ]
            )
        else:
            status, result = subprocess.getstatusoutput(
                [
                    f'exiftool "-AllDates={new_date}" -preserve -overwrite_original {path}/{file_name}',
                    new_date.strftime("%Y:%m:%d %H:%M:%S"),
                    path,
                    file_name,
                ]
            )
        if status != 0:
            logger.error("exiftool has trown an error, full exiftool output:\n" + result)
        if "1 image files updated" not in result:
            logger.warning(result)
        logger.info(f"Date changed for {file_path} to new date, {new_date}")
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {e}")
