import datetime
import logging
import os

import piexif


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


def change_date_from_EXIF(path, file_name, new_date):
    logger = logging.getLogger("my_app")
    file_path = os.path.join(path, file_name)
    exif_dict = piexif.load(file_path)
    exif_dict["Exif"] = {piexif.ExifIFD.DateTimeOriginal: new_date.strftime("%Y:%m:%d %H:%M:%S")}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path)
    logger.info("Date changed for", path / file_name, ", to new date,", new_date)


def adjust_time(image_path, adjustment):
    """Adjust the DateTimeOriginal field of the JPEG image metadata.

    :param image_path: Path to the JPEG image
    :param adjustment: Time adjustment in hours (positive or negative)
    """
    logger = logging.getLogger("my_app")
    try:
        # Load EXIF data
        exif_data = piexif.load(image_path)
        datetime_original = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal)

        if not datetime_original:
            logger.error(f"No 'DateTimeOriginal' field found in {image_path}")
            return

        # Decode the datetime string
        datetime_original_str = datetime_original.decode("utf-8")
        original_time = datetime.datetime.strptime(datetime_original_str, "%Y:%m:%d %H:%M:%S")

        # Adjust the time
        adjusted_time = original_time + datetime.timedelta(hours=adjustment)

        # Format back to EXIF format
        adjusted_time_str = adjusted_time.strftime("%Y:%m:%d %H:%M:%S")
        exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = adjusted_time_str.encode("utf-8")

        # Save the modified EXIF data
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, image_path)
        logger.info(f"Adjusted time for {image_path}: {datetime_original_str} -> {adjusted_time_str}")

    except Exception as e:
        logger.error(f"Failed to process {image_path}: {e}")
