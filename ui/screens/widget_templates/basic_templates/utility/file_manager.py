import json

class FileManager:
    '''
    File Manager for opening json files related to ui specific color schemes, size, and other characteristics.

    Attributes:
            pathData(dictionary): opens path_ref.json relative to root directory as an easy way to access files by reading corresponding key to given filename.
            currData(dictionary): opens specific file given that exists as a key in pathData
    '''

    def __init__(self, fileName):
        '''
        Initiates FileManager instance
        :param fileName(string): the name of the file to be parsed that exists as a key in path_ref.json
        '''
        self.pathData = self.parsefile("ui/screens/assets/path_ref.json")
        self.currData = self.parsefile(self.pathData[fileName])
        pass

    def parsefile(self, filePath):
        '''
        Parses given json file
        :param filePath(string): the relative path of the file to be parsed
        :return: returns the parsed file in dictionary
        '''
        with open(filePath) as f:
            return json.load(f)

    def updateData(self, fileName):
        '''
        updates current file attribute with given filename
        :param fileName(string): a file name expected to exist as a key in path_ref.json
        :return: None
        '''
        with open(self.pathData[fileName]) as f:
            self.currData= json.load(f)