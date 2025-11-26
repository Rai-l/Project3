

class DataManager:
    def __init__(self):
        self.data= {
            "N0": {"N1": 12, "N3": 5},
            "N1": {"N2": 3, "N4": 8},
            "N2": {"N0": 9},
            "N3": {"N2": 4, "N5": 7},
            "N4": {"N3": 6},
            "N5": {}
        }
        self.num_nodes=len(self.data)
        self.source=None
        self.path={}
        self.mode="dijkastra"

    def getAdj(self, item):
        return self.stringifyNodes(self.data[item])

    def stringifyNodes(self, nodes):
        stringified = "{"
        count = 0
        if nodes:
            for key, val in nodes.items():
                count += 1
                if count != 1:
                    stringified += ", " + key + " : " + str(val)
                else:
                    stringified += key + " : " + str(val)

        stringified += "}"
        return stringified

    def setMode(self, mode):
        self.mode=mode
        self.generatePath()

    def setSource(self, node):
        self.source = node
        self.generatePath()
        pass

    def generatePath(self):
        if self.source:
            if self.mode == "dijkastra":
                pass
            elif self.mode == "DFS":
                pass

    def getPath(self):
        if self.source:
            return "a stringified path need impll"
        else:
            return "None"
    def parseFile(self,filepath):
        with open(filepath, "r") as f:
            content=f.read()
        self.parseData(content)
        pass

    def parseData(self, data=None):
        #string data->adj list, expecting strings of from to weight
        strData = data
        if data==None:
            strData="N0 N1 12\nN0 N3 5\n"
        for i in range(strData.count("\n")):
            enterPos=strData.find("\n")
            line=strData[:enterPos]
            strData=strData[enterPos+1:]
            spacePos=line.find(" ")
            while (len(line)>0):
                fromNode=line[:spacePos+1]
                spacePos = line.find(" ")
                line=line[spacePos+1:]
                spacePos = line.find(" ")
                toNode=line[:spacePos+1]
                line = line[spacePos + 1:]
                spacePos = line.find(" ")
                weight = int(line[:spacePos+1]) if spacePos!=-1 else int(line)
                self.data[fromNode] = {toNode: weight}
                line=""
        self.setData()
        pass

    def setData(self):
        self.num_nodes=len(self.data)
        self.source=None
        self.path={}

    def loadData(self, input, type):
        if type=="file":
            self.parseFile(input)
        elif type=="text":
            self.parseData(input)
        pass
