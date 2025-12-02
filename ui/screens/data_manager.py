import os
from backend.Algorithims.adjacency_list import AdjacencyList
from backend.Algorithims.adapters import adjlist_to_bfs, reconstruct_from_dijkstra, bfs_path

class DataManager:
    '''Manages graph data, including loading, parsing, and path generation.
    
    Attributes:
        data (dict): Adjacency list representing the graph (for UI consumption).
        adj (AdjacencyList): algorithm-friendly adjacency list used to run algorithms.
        num_nodes (int): Number of nodes in the graph.
        source (str): The source node for pathfinding.
        end (str): Target node for pathfinding.
        path (list|dict): Computed path (list of node ids) or empty dict when none.
        mode (str): Pathfinding algorithm mode ("dijkstra" or "BFS").
    '''
    def __init__(self):
        '''Initializes the DataManager with default graph data.'''
        self.data= {
            "N0": {"N1": [12, 1], "N3": [5, 2]},
            "N1": {"N2": [3, 4], "N4": [8,2]},
            "N2": {"N0": [9, 4]},
            "N3": {"N2": [4,2], "N5": [7,1]},
            "N4": {"N3": [1,6]},
            "N5": {}
        }
        self.adj = AdjacencyList()
        self.sync_adj_list()
        self.num_nodes=len(self.data)
        self.source=None
        self.end=None
        # path: dict mapping node id -> [time, resource] (cumulative) for nodes on path
        self.path = {}
        # path_list: ordered list of node ids in path
        self.path_list = []
        # path_info: dict mapping node id -> {time, resource, cost} for nodes on computed path
        self.path_info = {}
        self.mode="dijkstra"
        # Optional callback that UI can set to receive path updates.
        # Signature: fn(path_list, path_info, path_dict)
        self.on_path_update = None

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
        print("switched mode "+mode)
        self.mode=mode
        self.generatePath()

    def setSource(self, node):
        self.source = node
        if self.end:
            self.generatePath()
        else:
            self.path = {}
            self.path_list = []
            self.path_info = {}
        pass

    def setEnd(self, node):
        self.end=node
        self.generatePath()

    def runBFS(self):
        """Run an unweighted BFS between self.source and self.end.
        Build cumulative time/resource totals along the returned path and
        populate self.path (node -> [cum_time,cum_resource]), self.path_list
        (ordered nodes) and self.path_info (node -> {time,resource,cost}).
        """
        # keep default weights for cost calculation; generatePath will pass real weights
        return self.runBFS_with_weights(1.0, 1.0)

    def runBFS_with_weights(self, weight1=1.0, weight2=1.0):
        try:
            path = bfs_path(self.data, self.source, self.end)
            if path:
                self.path_list = path
                self.path = {}
                self.path_info = {}
                cum_t = 0
                cum_r = 0
                for idx, node_id in enumerate(path):
                    if idx == 0:
                        # start node cumulative totals are zero
                        cum_t = 0
                        cum_r = 0
                        cost = 0
                        self.path[node_id] = [0, 0]
                        self.path_info[node_id] = {'time': 0, 'resource': 0, 'cost': 0}
                    else:
                        prev = path[idx - 1]
                        w = self.data.get(prev, {}).get(node_id, [0, 0])
                        t = w[0] if (isinstance(w, (list, tuple)) and len(w) > 0 and w[0] is not None) else 0
                        r = w[1] if (isinstance(w, (list, tuple)) and len(w) > 1 and w[1] is not None) else 0
                        cum_t += t
                        cum_r += r
                        cost = cum_t * weight1 + cum_r * weight2
                        self.path[node_id] = [cum_t, cum_r]
                        self.path_info[node_id] = {'time': cum_t, 'resource': cum_r, 'cost': cost}
            else:
                self.path = {}
                self.path_list = []
                self.path_info = {}
        except Exception as e:
            print("bfs error:", e)
            self.path = {}
            self.path_list = []
            self.path_info = {}
        return

    def generatePath(self, weight1=1.0, weight2=1.0):
        """Compute path between self.source and self.end using selected mode.
        Defaults weights to 1.0 each for dijkstra scalarization.
        Sets self.path to a list of node ids (empty list if none).
        """
        # make sure data is present
        if not self.source or not self.end:
            return
        if self.source == self.end:
            # single-node path
            self.path_list = [self.source]
            self.path = {self.source: [0, 0]}
            self.path_info = {self.source: {'time': 0, 'resource': 0, 'cost': 0}}
            # notify UI subscribers
            self._maybe_notify_path_update()
            return

        # ensure adjacency list is synced
        self.sync_adj_list()

        if self.mode.lower().startswith("dij"):
            # run dijkstra on adjacency list using both weights. If signature changed, report and abort.
            try:
                result = self.adj.dijkstra(self.source, self.end, weight1, weight2)
            except TypeError as e:
                # adjacency list API changed; require teammate to update caller or adjust here
                print("dijkstra error: incompatible dijkstra signature:", e)
                self.path = {}
                self.path_list = []
                self.path_info = {}
                result = None
            except Exception as e:
                print("dijkstra error:", e)
                self.path = {}
                self.path_list = []
                self.path_info = {}
                result = None

            if not result:
                # no path or unexpected return
                self.path = {}
                self.path_list = []
                self.path_info = {}
            elif isinstance(result, (list, tuple)) and len(result) == 5:
                # old-style detailed return
                nodes, times, resources, weighted_distance, previous = result
                path = reconstruct_from_dijkstra(nodes, previous, self.source, self.end)
                if path:
                    self.path_list = path
                    self.path_info = {}
                    idx_map = {n: i for i, n in enumerate(nodes)}
                    self.path = {}
                    for node_id in path:
                        i = idx_map.get(node_id)
                        if i is None:
                            continue
                        self.path_info[node_id] = {
                            'time': times[i],
                            'resource': resources[i],
                            'cost': weighted_distance[i]
                        }
                        self.path[node_id] = [times[i], resources[i]]
                else:
                    self.path = {}
                    self.path_list = []
                    self.path_info = {}
            elif isinstance(result, (list, tuple)):
                # assume result is an ordered path list
                path = list(result)
                if path:
                    self.path_list = path
                    # reconstruct cumulative time/resource from UI data
                    self.path = {}
                    self.path_info = {}
                    cum_t = 0
                    cum_r = 0
                    for idx, node_id in enumerate(path):
                        if idx == 0:
                            self.path[node_id] = [0, 0]
                            self.path_info[node_id] = {'time': 0, 'resource': 0, 'cost': 0}
                        else:
                            prev = path[idx - 1]
                            w = self.data.get(prev, {}).get(node_id, [0, 0])
                            t = w[0] if (isinstance(w, (list, tuple)) and len(w) > 0 and w[0] is not None) else 0
                            r = w[1] if (isinstance(w, (list, tuple)) and len(w) > 1 and w[1] is not None) else 0
                            cum_t += t
                            cum_r += r
                            cost = cum_t * weight1 + cum_r * weight2
                            self.path[node_id] = [cum_t, cum_r]
                            self.path_info[node_id] = {'time': cum_t, 'resource': cum_r, 'cost': cost}
                else:
                    self.path = {}
                    self.path_list = []
                    self.path_info = {}
            elif isinstance(result, dict):
                # try common dict shapes
                path = result.get('path') or result.get('nodes') or result.get('route')
                if path:
                    path = list(path)
                    self.path_list = path
                    # reconstruct similar to above
                    self.path = {}
                    self.path_info = {}
                    cum_t = 0
                    cum_r = 0
                    for idx, node_id in enumerate(path):
                        if idx == 0:
                            self.path[node_id] = [0, 0]
                            self.path_info[node_id] = {'time': 0, 'resource': 0, 'cost': 0}
                        else:
                            prev = path[idx - 1]
                            w = self.data.get(prev, {}).get(node_id, [0, 0])
                            t = w[0] if (isinstance(w, (list, tuple)) and len(w) > 0 and w[0] is not None) else 0
                            r = w[1] if (isinstance(w, (list, tuple)) and len(w) > 1 and w[1] is not None) else 0
                            cum_t += t
                            cum_r += r
                            cost = cum_t * weight1 + cum_r * weight2
                            self.path[node_id] = [cum_t, cum_r]
                            self.path_info[node_id] = {'time': cum_t, 'resource': cum_r, 'cost': cost}
                else:
                    self.path = {}
                    self.path_list = []
                    self.path_info = {}
            else:
                # unknown return type
                self.path = {}
                self.path_list = []
                self.path_info = {}
        elif self.mode.lower() == "bfs":
             # compute BFS path and cumulative weights using provided scalarization
             self.runBFS_with_weights(weight1, weight2)

        # notify any UI subscriber that a new path (or empty result) is available
        self._maybe_notify_path_update()

    def getPath(self):
        # If path is dict mapping node->[t,r], stringify in same format as earlier code
        if isinstance(self.path, dict) and len(self.path) > 0:
            pairs = []
            for k, v in self.path.items():
                pairs.append(f"{k} : [{v[0]},{v[1]}]")
            return "{" + ", ".join(pairs) + "}"
        # fallback: use path_list
        if isinstance(self.path_list, list) and len(self.path_list) > 0:
            return " -> ".join(self.path_list)
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
        # string data -> adj list, expecting lines: from to weight1 weight2
        print("parsing data...")
        try:
            strData = data if data is not None else "N0 N1 12 11\nN0 N3 5 1\n"
            # reset data
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
        except Exception as e:
            print("invalid data", e)
            return
        pass

    def setData(self):
        self.num_nodes=len(self.data)
        # sync algorithm adjacency after data changes
        try:
            self.sync_adj_list()
        except Exception:
            pass
        self.source=None
        # reset path-related structures to the new formats
        self.path = {}
        self.path_list = []
        self.path_info = {}

    def getGenerated(self, num_nodes=6, max_time=10, max_resource=5):
        # generate a random algorithm adjacency and convert to self.data format
        self.adj = AdjacencyList()
        self.adj.randomly_generate(num_nodes, max_time, max_resource)
        # build self.data from self.adj.graph where edges are [node, time, resource]
        new_data = {}
        for u, neighs in self.adj.get_graph().items():
            new_data[u] = {}
        for u, neighs in self.adj.get_graph().items():
            for entry in neighs:
                # edge entries are [v, time, resource]
                if entry and len(entry) >= 3:
                    v = entry[0]
                    t = entry[1] if entry[1] is not None else 0
                    r = entry[2] if entry[2] is not None else 0
                    new_data[u][v] = [t, r]
        self.data = new_data
        self.setData()

    def loadData(self, input, type):
        if type=="file":
            self.parseFile(input)
        elif type=="text":
            self.parseData(input)
        elif type=="random":
            self.getGenerated()
        pass

    def _maybe_notify_path_update(self):
        """Call the on_path_update callback if provided."""
        try:
            if callable(self.on_path_update):
                self.on_path_update(self.path_list, self.path_info, self.path)
        except Exception as e:
            # don't raise to avoid breaking path generation
            print("on_path_update error:", e)
