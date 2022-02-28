from itertools import count
from datetime import datetime
import AnyBotLog as logg
from BotMemory import FileHandlerBot as fh

timeStampFormat = "%m/%d/%Y-%H:%M"


class HashTagUsageRecorder:
    _logID = count(0)

    def __init__(self):
        a = 0
        self.id = next(self._logID)
        self.filehandler = fh.FileHandlerBot()

    def __enter__(self):
        return self

    def recordTags(self, commentText):
        # logg.logSmth(f"I just recorded a comment:\n {commentText}")
        timeStamp = datetime.now().strftime(timeStampFormat)
        self.filehandler.CSV_addNewRowToCSV('hashtagUsageCSV', [timeStamp, commentText])

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("\nTraceback:", exc_tb)
        # print(self.id)


def recordTags(comment_as_txt):
    with HashTagUsageRecorder() as hsr:
        hsr.recordTags(comment_as_txt)
        return 'OK'
