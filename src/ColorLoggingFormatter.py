import logging
from enum import Enum


class Colors(Enum):
    GREY = "\x1b[38;20m"
    GREEN = "\033[1;32m"
    YELLOW = "\x1b[38;5;184m"
    ORANGE = "\x1b[38;5;208m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    LIGHT_BLUE = "\033[94m"


class ColorLoggingFormatter(logging.Formatter):
    """For the color codes have a look at the following URL.

    https://talyian.github.io/ansicolors/
    """

    # Needed formats
    messageFormatPart1 = "%(asctime)s | %(levelname)-9s: "
    messageFormatPart2 = "%(message)s"
    messageFormatPart2LineNumber = "%(message)s - (%(filename)s:%(lineno)d)"
    dateFormat = "%Y-%m-%d %H:%M:%S"

    FORMATS = {
        logging.DEBUG: Colors.RESET.value + messageFormatPart1 + Colors.GREY.value + messageFormatPart2LineNumber + Colors.RESET.value,
        logging.INFO: Colors.RESET.value + messageFormatPart1 + Colors.GREEN.value + messageFormatPart2 + Colors.RESET.value,
        logging.WARNING: Colors.RESET.value + messageFormatPart1 + Colors.YELLOW.value + messageFormatPart2LineNumber + Colors.RESET.value,
        logging.ERROR: Colors.RESET.value + messageFormatPart1 + Colors.ORANGE.value + messageFormatPart2LineNumber + Colors.RESET.value,
        logging.CRITICAL: Colors.RESET.value + messageFormatPart1 + Colors.RED.value + messageFormatPart2LineNumber + Colors.RESET.value,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.dateFormat)
        return formatter.format(record)
