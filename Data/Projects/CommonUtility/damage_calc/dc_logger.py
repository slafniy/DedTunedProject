import logging
import sys
from pathlib import Path

_path_to_log = Path(__file__).resolve().parent / 'damage_calculator.log'


def _get_logger_gen():
    logger = logging.Logger(">>")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(_path_to_log, mode='w')
    logger.addHandler(file_handler)

    while True:
        yield logger


_logger_gen = _get_logger_gen()

dc_logger = next(_logger_gen)
