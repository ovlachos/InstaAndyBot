from itertools import count
import AnyBotLog as logg


class HashTagUsageRecorder:
    _logID = count(0)

    def __init__(self):
        a = 0
        self.id = next(self._logID)

    def __enter__(self):
        return self

    def recordTags(self, commentText):
        logg.logSmth(f"I just recorded a comment:\n {commentText}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("\nTraceback:", exc_tb)
        # print(self.id)


def recordTags(comment_as_txt):
    with HashTagUsageRecorder() as hsr:
        hsr.recordTags(comment_as_txt)
    return 'OK'
