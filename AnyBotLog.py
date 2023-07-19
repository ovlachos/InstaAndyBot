import logging
import os
import shutil
from itertools import count


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


class MyLogger:
    _logID = count(0)

    def __init__(self, logger):
        self.logger = logger
        self.id = next(self._logID)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("\nTraceback:", exc_tb)
        # print(self.id)

    def cleanUp(self):
        if not self.logger.hasHandlers():
            return
        logSize = file_size(self.logger.handlers[0].baseFilename)
        # print(logSize)

        if 'ΜB' in logSize:
            numSize = float(logSize.split('Μ')[0])

            if numSize > 7:
                print(f"################################### Log file is {logSize}. Will delete")
                if os.path.exists(self.logger.handlers[0].baseFilename):
                    os.remove(self.logger.handlers[0].baseFilename)

                for hand in self.logger.handlers:
                    self.logger.removeHandler(hand)


def createLogger():
    screenLogger = logging.getLogger('The_Logger')
    screenLogger.propagate = 0
    screenFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    screenHandler = logging.FileHandler('../InstaBot2.log')
    # TimedRotatingFileHandler(filename='../logs/InstaBot2.log', when='D', interval=1, backupCount=14, encoding='utf-8', delay=False)
    screenHandler.setFormatter(screenFormat)
    screenHandler.setLevel(logging.DEBUG)

    if not len(screenLogger.handlers):
        screenLogger.addHandler(screenHandler)

    screenLogger.setLevel(logging.DEBUG)

    return MyLogger(screenLogger)


def logSmth(message, level=None):
    print(message)
    with createLogger() as loggerPack:
        if level:
            if 'DEBUG' in level:
                loggerPack.logger.debug(message)
            if 'INFO' in level:
                loggerPack.logger.info(message)
            if 'WARNING' in level:
                loggerPack.logger.warning(message)
            if 'ERROR' in level:
                loggerPack.logger.error(message, exc_info=True)
        else:
            loggerPack.logger.info(message)

        loggerPack.cleanUp()
