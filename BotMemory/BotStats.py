from BotMemory import FileHandlerBot as fh


class StatsRecorder:
    def __init__(self):
        self.f_h = fh.FileHandlerBot()

    def __enter__(self):
        return self

    def recordMyStats(self, dataPoint):
        self.f_h.CSV_addNewRowToCSV("myStats", dataPoint)

    def recordMyFollowing(self, myFollowing):
        frame = self.f_h.listToFrame(myFollowing)
        self.f_h.CSV_saveFrametoCSVfile('myFollowing', frame)

    def recordHashTagStats(self, dataPoint):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("\nTraceback:", exc_tb)


def createStatsRecorder():
    return StatsRecorder()


def record_new_point(dataPoint, fileName):
    with createStatsRecorder() as statRec:
        if "Stats" in fileName:
            statRec.recordMyStats(dataPoint)

        if "hash" in fileName:
            statRec.recordHashTagStats(dataPoint)

        if "Following" in fileName:
            statRec.recordMyFollowing(dataPoint)
