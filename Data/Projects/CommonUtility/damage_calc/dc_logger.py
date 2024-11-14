import logging
import sys
from pathlib import Path

_loggers = {}


def get_logger(name):
    if name not in _loggers.keys():
        _loggers[name] = DCLogger(name)
    return _loggers[name]


class DCLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

        _path_to_log = Path(__file__).resolve().parent / f'{name}.log'

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(logging.ERROR)
        self.stream_handler.setFormatter(formatter)
        self.addHandler(self.stream_handler)

        self.file_handler = logging.FileHandler(_path_to_log, mode='w')
        self.file_handler.setFormatter(formatter)
        self.file_handler.setLevel(logging.ERROR)
        self.addHandler(self.file_handler)
