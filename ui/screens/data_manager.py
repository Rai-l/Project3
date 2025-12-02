import os

class DataManager:
    '''Manages graph data, including loading, parsing, and path generation.
    
    Attributes:
        data (dict): Adjacency list representing the graph.
        num_nodes (int): Number of nodes in the graph.
        source (str): The source node for pathfinding.
        path (dict): Computed paths from the source node containing string key and int weight.
        mode (str): Pathfinding algorithm mode ("dijkstra" or "BFS").
    '''
    def __init__(self):
        '''Initializes the DataManager with default graph data.
        '''
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
        self.end=None
        self.path={}
        self.mode="dijkstra"

    def getAdj(self, item):
        '''Returns the adjacency list of the specified node as a string.
        Parameters:
            item (str): The node identifier.
        Returns:
            str: Stringified adjacency list of the node.
        '''
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
        if self.end:
            self.generatePath()
        else:
            self.path={}
        pass

    def setEnd(self, node):
        self.end=node
        self.generatePath()

    def generatePath(self):
        if self.source and self.end:
            if self.source==self.end:
                self.path={}
            if self.mode == "dijkstra":
                pass
            elif self.mode == "BFS":
                pass

    def getPath(self):
        if len(self.path)>0:
            return "a stringified path need impll"
        else:
            return "None"
    def parseFile(self,filepath):
        if not os.path.exists(filepath):
            print("invalid path")
            return
        with open(filepath, "r") as f:
            content=f.read()
        self.parseData(content)
        pass

    def parseData(self, data=None):
        #string data->adj list, expecting strings of: from to weight
        print("parsing data...")
        try:
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
        except Exception:
            print("invalid data")
            return
        pass

    def setData(self):
        self.num_nodes=len(self.data)
        self.source=None
        self.path={}
    def getGenerated(self):
        data=None
        if data==None:
            self.data={
            "N0": {"N1": 12, "N3": 5},
            "N1": {"N2": 3, "N4": 8},
            "N2": {"N0": 9},
            "N3": {"N2": 4, "N5": 7},
            "N4": {"N3": 6},
            "N5": {}
        }
        self.setData()

    def loadData(self, input, type):
        if type=="file":
            self.parseFile(input)
        elif type=="text":
            self.parseData(input)
        elif type=="random":
            self.getGenerated()
        pass
