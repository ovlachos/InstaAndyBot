from BotMemory import FileHandlerBot as fh


class BotParams:
    def __init__(self):
        self.fileName = 'BotParams'
        self.paramsFileHandler = fh.FileHandlerBot()
        self.paramsDict = None

        self.readBotParams()

    def readBotParams(self):
        if inputFile := self.paramsFileHandler.readSimpleJSONfiles(self.fileName):
            self.paramsDict = inputFile

    def writeBotParams(self):
        if self.paramsDict:
            self.paramsFileHandler.writeSimpleJSONfiles(self.fileName, self.paramsDict)

    def getBotParams(self):
        if self.paramsDict:
            return self.paramsDict

    def getBotParam(self, param):
        if self.paramsDict:
            return self.paramsDict.get(param, None)

    def updateMana(self, newValue, timeStamp=None):
        if newValue:
            self.paramsDict['manaLeft'] = newValue

            if timeStamp:
                self.paramsDict['TimeStamp'] = timeStamp

            self.writeBotParams()

    def updateOwnFollowers(self, newValue):
        if newValue:
            self.paramsDict['OwnFollowers'] = newValue
            self.writeBotParams()
