import logging
import sys
from pathlib import Path



class DCLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

        _path_to_log = Path(__file__).resolve().parent / f'{name}.log'

        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(formatter)
        self.addHandler(self.stream_handler)

        self.file_handler = logging.FileHandler(_path_to_log, mode='w')
        self.file_handler.setFormatter(formatter)
        self.addHandler(self.file_handler)


