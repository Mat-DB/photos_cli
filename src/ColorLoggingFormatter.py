import logging


class ColorLoggingFormatter(logging.Formatter):
    """
    For the color codes have a look at the following URL.
    https://talyian.github.io/ansicolors/
    """
    # Colors
    grey = "\x1b[38;20m"
    green = "\033[1;32m"
    yellow = "\x1b[38;5;184m"
    orange = "\x1b[38;5;208m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Needed formats
    messageFormatPart1 = "%(asctime)s | %(levelname)-9s: "
    messageFormatPart2 = "%(message)s"
    messageFormatPart2LineNumber = "%(message)s - (%(filename)s:%(lineno)d)"
    dateFormat = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: reset + messageFormatPart1 + grey + messageFormatPart2LineNumber + reset,
        logging.INFO: reset + messageFormatPart1 + green + messageFormatPart2 + reset,
        logging.WARNING: reset + messageFormatPart1 + yellow + messageFormatPart2LineNumber + reset,
        logging.ERROR: reset + messageFormatPart1 + orange + messageFormatPart2LineNumber + reset,
        logging.CRITICAL: reset + messageFormatPart1 + red + messageFormatPart2LineNumber + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.dateFormat)
        return formatter.format(record)
