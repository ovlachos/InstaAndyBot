import logging
from itertools import count


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
        # print(self._logID)


def createLogger():
    screenLogger = logging.getLogger('The_Logger')
    screenFormat = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    screenHandler = logging.FileHandler('../InstaBot.log')
    screenHandler.setFormatter(screenFormat)
    screenHandler.setLevel(logging.DEBUG)

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
