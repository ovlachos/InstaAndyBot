from BotMemory import FileHandlerBot as fh


class StatsRecorder:
    def __init__(self):
        self.f_h = fh.FileHandlerBot()

    def __enter__(self):
        return self

    def recordMyStats(self, dataPoint):
        self.f_h.CSV_addNewRowToCSV("myStats", dataPoint)

    def recordHashTagStats(self, dataPoint):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("\nTraceback:", exc_tb)


def createStatsRecorder():
    return StatsRecorder()


def record_new_point(dataPoint, fileName):
    with createStatsRecorder() as statRec:
        if "my" in fileName:
            statRec.recordMyStats(dataPoint)

        if "hash" in fileName:
            statRec.recordHashTagStats(dataPoint)
