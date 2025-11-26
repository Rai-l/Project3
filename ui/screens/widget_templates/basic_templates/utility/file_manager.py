import json

class FileManager:

    def __init__(self, fileName):
        # paths
        self.pathData = self.parsefile("ui/screens/assets/path_ref.json")
        self.currData = self.parsefile(self.pathData[fileName])
        pass

    def parsefile(self, filePath):
        with open(filePath) as f:
            return json.load(f)

    def updateData(self, fileName):
        with open(self.pathData[fileName]) as f:
            self.currData= json.load(f)