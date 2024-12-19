import json
import os
import pickle
import pandas as pd
import AnyBotLog as logg

from BotMemory import BotMemoryFilesFactory as BF


def initializeFolder(targetPath):
    from os import path

    try:
        if not path.exists(targetPath):
            os.makedirs(targetPath)
    except Exception as e:
        print(e)


class MemoryFile():
    """
    Represents a file in memory with specific attributes.

    This class is designed to store and manage basic file information including the
    file name, file path, extension, and column structure. Additionally, it provides
    functionality to initialize the file with the help of an external creator
    object that supplies details about the file.

    Attributes:
    fileName (str): The name of the file.
    filepath (str): The path where the file is located.
    extension (str): The type or format of the file extension.
    columns (list): A list of column names or specifications associated with the file.

    Methods:
    initialize(creator): Uses the provided creator object to retrieve and set
    details about the file.
    """
    def __init__(self, fileName, filepath, extension, columns):
        self.fileName = fileName
        self.filepath = filepath
        self.extension = extension
        self.columns = columns

    def initialize(self, creator):
        creator.getDetails(self.filepath, self.columns)


class FileHandlerBot:
    """
    The FileHandlerBot class provides functionality for managing files and directories configured in JSON files.
    It includes methods to read and write JSON configurations, manage CSV files, handle operations like adding
    or removing rows, and support user memory serialization via JSON or pickle formats. The class ensures the
    existence of directories and files during initialization and provides utility methods for data manipulation.

    Attributes:
        thisFile (str): Directory path of the current file.
        py_files (str): Path to the directory one level above the file's directory.
        projectFolder (str): Path to the root project folder.

    Methods:
        __init__():
            Initializes the FileHandlerBot instance by validating and setting up directories and files.
        getConfig_JSON_paths(kindOfJSON: str) -> dict:
            Reads and returns configuration details from JSON files.
        getFileFromFilename(filename: str) -> Optional[dict]:
            Retrieves configuration details for a specific file by its name.
        CSV_getFrameFromCSVfile(filename: str) -> pd.DataFrame:
            Reads and returns the content of a CSV file as a pandas DataFrame.
        listToFrame(inputList: list) -> pd.DataFrame:
            Converts a list into a pandas DataFrame.
        CSV_saveFrametoCSVfile(filename: str, frame: pd.DataFrame):
            Saves a pandas DataFrame to a CSV file.
        CSV_removeRowFromCSV(filename: str, row_index: int):
            Removes a specific row from a CSV file by index.
        CSV_addNewRowToCSV(filename: str, row: list):
            Adds a new row to the specified CSV file.
        addUserto_the_Love(user: str, kindOfLove: str):
            Adds a user to a specified "love" CSV file, ensuring no duplicates.
        removeUserfrom_the_Love(user: str, kindOfLove: str):
            Removes a user from a specified "love" CSV file.
        readSimpleJSONfiles(fileName: str) -> Optional[dict]:
            Reads and returns the contents of a simple JSON file.
        writeSimpleJSONfiles(fileName: str, fileObj: dict):
            Writes an object to a specified JSON file.
        readMemoryFile(JSONdecoder: Callable) -> list:
            Reads a user memory file and decodes it using the provided JSON decoder function.
        readMemoryFiles(JSONdecoder: Callable) -> list:
            Reads all user memory JSON files in a directory and decodes them.
        writeToUserMemory(userMemory: list, JSONencoder: Callable, file: Optional[str] = None):
            Writes a list of user memory information to a JSON file using a JSON encoder.
        pickleUserMemory(userMemory: any):
            Serializes and saves user memory to a pickle file.
        unPickleMemory() -> any:
            Reads and deserializes user memory from a pickle file.
    """
    # Main Directories
    thisFile = os.path.dirname(__file__)
    py_files = os.path.join(thisFile, '../')
    projectFolder = os.path.join(py_files, '../')

    def __init__(self):
        from pathlib import Path

        self.paths = self.getConfig_JSON_paths('paths')
        self.files = self.getConfig_JSON_paths('files')
        self.fileFactoryCreator = BF.fileCreator()

        # Make sure the files and folders mentioned
        # in the JSON configs are in existence
        for val in self.paths.values():
            initializeFolder(Path(self.projectFolder + val))

        for file in self.files:
            if not Path(file['filepath']).is_file():
                mFile = MemoryFile(file['filename'], file['filepath'], file['extension'], file['columns'])
                self.fileFactoryCreator.create(mFile, file['extension'])

    def getConfig_JSON_paths(self, kindOfJSON='paths'):

        os.chdir(self.projectFolder)
        if kindOfJSON == 'paths':
            fileName = "paths_config.json"
        else:
            fileName = "files_config.json"

        with open(fileName) as json_conf:
            CONF = json.load(json_conf)

        return CONF

    def getFileFromFilename(self, filename):
        for file in self.files:
            if filename == file['filename']:
                return file

    def CSV_getFrameFromCSVfile(self, filename):
        frame = pd.DataFrame([])
        file = self.getFileFromFilename(filename)
        if file:
            try:
                frame = pd.read_csv(file['filepath'], sep=',')
            except Exception as e:
                print(e)

        return frame

    def listToFrame(self, inputList):
        return pd.DataFrame(data=inputList)

    def CSV_saveFrametoCSVfile(self, filename, frame):
        file = self.getFileFromFilename(filename)
        frame.to_csv(file['filepath'], index=False, encoding='utf-8')

    def CSV_removeRowFromCSV(self, filename, row_index):
        file = self.getFileFromFilename(filename)
        if file:
            oldframe = self.CSV_getFrameFromCSVfile(filename)
            oldframe = oldframe.drop(oldframe.index[row_index])
            oldframe.to_csv(file['filepath'], index=False, encoding='utf-8')

    def CSV_addNewRowToCSV(self, filename, row):  # 'row' is a list type
        file = self.getFileFromFilename(filename)
        if file:
            oldFrame = pd.read_csv(file['filepath'])

            if len(file['columns']) == len(row):
                new_row = pd.Series(row)
                row_df = pd.DataFrame([new_row])
                row_df.columns = file['columns']

                frame_new = pd.concat([row_df, oldFrame], ignore_index=True)
                frame_new.to_csv(file['filepath'], index=False, encoding='utf-8')

    def addUserto_the_Love(self, user, kindOfLove):

        file = self.getFileFromFilename(kindOfLove)  # e.g. 'dailyLoveCSV'
        if file:
            oldFrame = pd.read_csv(file['filepath'])

            if not user in oldFrame[file['columns'][0]].tolist():
                self.CSV_addNewRowToCSV(kindOfLove, [user])

    def removeUserfrom_the_Love(self, user, kindOfLove):
        file = self.getFileFromFilename(kindOfLove)
        if file:
            oldFrame = pd.read_csv(file['filepath'])
            try:
                rowIndexOfUser = oldFrame[oldFrame[file['columns'][0]] == user].index.values[0]
                self.CSV_removeRowFromCSV(kindOfLove, rowIndexOfUser)
            except Exception as e:
                logg.logSmth("{0}, {1}".format(e, user))

    def readSimpleJSONfiles(self, fileName):

        memoryfile = None
        file = self.getFileFromFilename(fileName)

        if file:
            try:
                with open(file['filepath']) as jUM:
                    memoryfile = json.load(jUM)
            except Exception as e:
                logg.logSmth(f'WARNING: fail in reading {fileName}. Falling back to defaults. {e}')

            return memoryfile

    def writeSimpleJSONfiles(self, fileName, fileObj):

        file = self.getFileFromFilename(fileName)['filepath']

        if file:
            with open(file, 'w') as jUM:
                json.dump(fileObj, jUM, sort_keys=True, indent=4)

    def readMemoryFile(self, JSONdecoder):  # JSONdecoder is a function that translates JSON to User_M objects

        file = self.getFileFromFilename('User_Memory')

        if file:
            try:
                with open(file['filepath']) as jUM:
                    memoryfile = json.load(jUM, object_hook=JSONdecoder)
            except Exception as e:
                memoryfile = []
                logg.logSmth('WARNING: Could not read memory file! No love can be given.')
                logg.logSmth(f"Error: {e}")

            return memoryfile

    def readMemoryFiles(self, JSONdecoder):
        import glob

        directory = self.paths['User_Memory']
        all_files = glob.glob(directory + "/*.json")

        memoryfile = []
        memoryfile1 = []
        for file in all_files:
            with open(file) as jUM:
                memoryfile1.append(json.load(jUM, object_hook=JSONdecoder))

        for item in memoryfile1:
            memoryfile.append(item[0])

        return memoryfile

    def writeToUserMemory(self, userMemory, JSONencoder, file=None):
        # userMemory is a list of python dictionaries each containing a single user's info

        if not file:
            file = self.getFileFromFilename('User_Memory')['filepath']

        if file:
            with open(file, 'w') as jUM:
                json.dump(userMemory, jUM, cls=JSONencoder, sort_keys=True, indent=4)

    def pickleUserMemory(self, userMemory):  # TODO: use "with" context manager instead
        fileName = self.getFileFromFilename('User_Memory_pickle')['filepath']
        if fileName:
            outfile = open(fileName, 'wb')
            pickle.dump(userMemory, outfile, fix_imports=True, buffer_callback=None)
            outfile.close()

    def unPickleMemory(self):
        filename = self.getFileFromFilename('User_Memory_pickle')['filepath']
        if filename:
            infile = open(filename, 'rb')
            memoryPickle = pickle.load(infile)
            infile.close()
            return memoryPickle
