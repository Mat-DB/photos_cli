import os
from datetime import datetime

import piexif


def asking_new_date():
    new_date_year = int(input("Geef het JAAR van de nieuwe datum: "))
    new_date_month = int(input("Geef de Maand van de nieuwe datum: "))
    new_date_day = int(input("Geef de DAG van de nieuwe datum: "))
    tijd_ja_nee = input("Wilt u ook een uur? Indien nee 00:00:00. (ja of nee): ")
    if tijd_ja_nee == "ja":
        new_date_hour = int(input("Geef het UUR van de nieuwe datum: "))
        new_date_minute = int(input("Geef het MINUTEN van de nieuwe datum: "))
        new_date_second = int(input("Geef het SECONDE van de nieuwe datum: "))
    else:
        new_date_hour = 0
        new_date_minute = 0
        new_date_second = 0
    new_date = datetime(new_date_year, new_date_month, new_date_day, new_date_hour, new_date_minute, new_date_second)
    print("Dit klopt?", new_date)
    correct = input("ja of nee?: ")
    if correct == "nee":
        new_date = asking_new_date()
    return new_date


def change_date_in_EXIF(path, file_name, new_date):
    file_path = os.path.join(path, file_name)
    exif_dict = piexif.load(file_path)
    exif_dict["Exif"] = {piexif.ExifIFD.DateTimeOriginal: new_date.strftime("%Y:%m:%d %H:%M:%S")}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path)
    print("Change date of", path / file_name)
