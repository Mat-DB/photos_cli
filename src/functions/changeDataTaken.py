from datetime import datetime, timedelta

import piexif


def adjust_time(image_path, adjustment):
    """Adjust the DateTimeOriginal field of the JPEG image metadata.

    :param image_path: Path to the JPEG image
    :param adjustment: Time adjustment in hours (positive or negative)
    """
    try:
        # Load EXIF data
        exif_data = piexif.load(image_path)
        datetime_original = exif_data["Exif"].get(piexif.ExifIFD.DateTimeOriginal)

        if not datetime_original:
            print(f"No 'DateTimeOriginal' field found in {image_path}")
            return

        # Decode the datetime string
        datetime_original_str = datetime_original.decode("utf-8")
        original_time = datetime.strptime(datetime_original_str, "%Y:%m:%d %H:%M:%S")

        # Adjust the time
        adjusted_time = original_time + timedelta(hours=adjustment)

        # Format back to EXIF format
        adjusted_time_str = adjusted_time.strftime("%Y:%m:%d %H:%M:%S")
        exif_data["Exif"][piexif.ExifIFD.DateTimeOriginal] = adjusted_time_str.encode("utf-8")

        # Save the modified EXIF data
        exif_bytes = piexif.dump(exif_data)
        piexif.insert(exif_bytes, image_path)
        print(f"Adjusted time for {image_path}: {datetime_original_str} -> {adjusted_time_str}")

    except Exception as e:
        print(f"Failed to process {image_path}: {e}")
