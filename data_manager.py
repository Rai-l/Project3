import os
import random
import string
from backend.Algorithims.adjacency_list import AdjacencyList
from backend.Algorithims.adapters import adjlist_to_bfs, reconstruct_from_dijkstra, bfs_path


class DataManager:
    '''
    Helps manage modifying, retrieving, and storing data of an adjacency list and other included attributes.

    Attributes:
        data(dict): dict of node keys and their adjacent vetex as values where its stored as dict of node key and weight, a list of time and resource
        adj(AdjacencyList): an instance of AdjacencyList
        num_nodes(int): length of current data dict
        source(string): start node for computation of shortest path
        end(string): end node for computation of shortest path
        path(list): computed shortest path
        mode(string): string of "dijkstra" or "bfs"

    '''
    def __init__(self):
        self.data = {
            "N0": {"N1": [12, 1], "N3": [5, 2]},
            "N1": {"N2": [3, 4], "N4": [8, 2]},
            "N2": {"N0": [9, 4]},
            "N3": {"N2": [4, 2], "N5": [7, 1]},
            "N4": {"N3": [1, 6]},
            "N5": {}
        }
        self.adj = AdjacencyList()
        self.num_nodes = len(self.data)
        self.source = None
        self.end = None
        self.path = []
        self.mode = "dijkstra"
        self.sync_adj_list()
        self.setData()

    def getAdj(self, item):
        '''Returns the adjacency list of the specified node as a string.'''
        return self.stringifyNodes(self.data.get(item, {}))

    def stringifyNodes(self, nodes):
        stringified = "{"
        if not nodes:
            return "{}"
        pairs = []
        for key, val in nodes.items():
            # val expected to be a list-like [weight1, weight2]
            w1 = val[0] if len(val) > 0 else None
            w2 = val[1] if len(val) > 1 else None
            pairs.append(f"{key} : [{w1},{w2}]")
        stringified += ", ".join(pairs)
        stringified += "}"
        return stringified

    def setMode(self, mode):
        self.mode = mode
        self.path = []
        self.generatePath()

    def setSource(self, node):
        self.source = node

    def setEnd(self, node):
        self.end = node

    def runBFS(self):
        try:
            path = bfs_path(self.data, self.source, self.end)
            if path:
                self.path=path
            else:
                self.path = []
        except Exception:
            print("Invalid input(s)")
            self.path = {}
        return
    def sync_adj_list(self):
        """Populate self.adj (AdjacencyList) from self.data (dict).
        Call after parseData / getGenerated / any external edits to self.data.
        """
        self.adj = AdjacencyList()
        for u, neigh in self.data.items():
            if not neigh:
                # ensure the node exists in adj.graph but do NOT insert None-neighbor entries
                # do this by directly ensuring the key exists with an empty list
                self.adj.graph.setdefault(u, [])
                continue
            for v, vals in neigh.items():
                # vals expected to be [time, resource]
                try:
                    t = vals[0] if vals and len(vals) > 0 else 0
                    r = vals[1] if vals and len(vals) > 1 else 0
                except Exception:
                    t, r = 0, 0
                self.adj.insert(u, v, t, r)

    def generatePath(self, weight1=1.0, weight2=1.0):
        """Compute path between self.source and self.end using selected mode.
        Defaults weights to 1.0 each for dijkstra scalarization.
        Sets self.path to a list of node ids (empty list if none).
        """
        # make sure data is present
        if not self.source or not self.end:
            return
        if self.source == self.end:
            self.path = {self.source: [0, 0]}
            return

        if self.mode.lower().startswith("dij"):
            result = self.adj.dijkstra(self.source, self.end, weight1, weight2)
            if result:
                self.path = result
            else:
                self.path = []

        elif self.mode.lower() == "bfs":
            self.runBFS()

    def getPath(self):
        if self.path and len(self.path) > 0:
            return "{" + ", ".join(self.path) + "}"
        return "No path found"

    def parseFile(self, filepath):
        if not os.path.exists(filepath):
            print("Invalid path")
            return
        with open(filepath, "r") as f:
            content = f.read()
        self.parseData(content)
        pass

    def parseData(self, data=None):
        try:
            strData = data if data is not None else "N0 N1 12 11\nN0 N3 5 1\n"
            self.data = {}
            for raw_line in strData.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 3:
                    # invalid line, skip
                    continue
                fromNode = parts[0].strip()
                toNode = parts[1].strip()
                # parse weights
                try:
                    weight1 = int(parts[2])
                except Exception:
                    weight1 = 0
                weight2 = 0
                if len(parts) >= 4:
                    try:
                        weight2 = int(parts[3])
                    except Exception:
                        weight2 = 0
                # ensure entries exist and preserve multiple neighbors
                if fromNode not in self.data:
                    self.data[fromNode] = {}
                self.data[fromNode][toNode] = [weight1, weight2]
                if toNode not in self.data:
                    self.data[toNode] = {}
            self.setData()
        except Exception:
            print("Invalid input(s)")
            return
        pass

    def setData(self):
        try:
            self.sync_adj_list()
        except Exception:
            pass
        self.num_nodes = len(self.data)
        self.source = None
        self.path = []

    def getGenerated(self, num_nodes=15000, max_time=10, max_resource=50, avg_degree=4):
        nodes = []
        while len(nodes) < num_nodes:
            name = "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))
            if name not in nodes:
                nodes.append(name)
        graph = {node: {} for node in nodes}
        for i in range(num_nodes):
            node = nodes[i]
            degree = random.randint(1, avg_degree)
            possible = list(range(num_nodes))
            possible.remove(i)
            neighbors = random.sample(possible, degree)

            for idx in neighbors:
                neighbor = nodes[idx]
                if neighbor not in graph[node]:
                    t = random.randint(1, max_time)
                    r = random.randint(1, max_resource)

                    graph[node][neighbor] = [t, r]
                    graph[neighbor][node] = [t, r]
        self.data=graph

    def loadData(self, input, type):
        if type == "file":
            self.parseFile(input)
        elif type == "text":
            self.parseData(input)
        elif type == "random":
            self.getGenerated()
        pass