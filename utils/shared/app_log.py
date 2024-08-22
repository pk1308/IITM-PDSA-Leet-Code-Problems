import sys
from datetime import datetime

from loguru import logger


def custom_time_format(record):
    """Custom time format function for logging with hour, minute, and second.

    This function can be potentially extended to extract information from the
    `record` argument for more dynamic formatting in the future.

    Args:
        record (logging.Record): The Loguru record object.

    Returns:
        str: The formatted time string.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Set up the logger with custom format
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> | <blue>{level}</blue> | {message}",
)
