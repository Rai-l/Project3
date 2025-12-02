import random
import string
import sys
import backend.Algorithims.priority_queue as pq


class AdjacencyList:
    def __init__(self):
        self.graph = {}
        self.dispay_graph = {}

    #inserts and edge into the adjacency list.
    def insert(self, point_A, point_B, time_taken, resource_needed):
        if len(self.graph) == 1:
            self.graph.clear()
        val1 = [point_B, time_taken, resource_needed]
        val2 = [point_A, time_taken, resource_needed]
        val3 = {point_B : [time_taken, resource_needed]}
        if point_A not in self.graph.keys():
            self.graph.update({point_A : []})
        if point_B not in self.graph.keys() and point_B is not None:
            self.graph.update({point_B : []})
            self.dispay_graph.update({point_B: {}})
        self.graph[point_A].append(val1)
        if point_B is not None:
            self.graph[point_B].append(val2)
        self.dispay_graph.update({point_A : val3})

    def get_adjacent(self, node):
        return self.graph.get(node)

    def get_graph(self):
        return self.graph

# get display graph returns the graph in the format you requested
    def get_display_graph(self):
        return self.dispay_graph

    def randomly_generate(self, number_of_nodes, max_time, max_resource):
        self.graph.clear()
        if number_of_nodes == 1:
            length = random.randint(1, 20)
            name = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))
            self.insert(name, None, None, None)
            return
        nodes = [" " for i in range(0, number_of_nodes)]
        index = 0
        edges = []
        while " " in nodes:
            length = random.randint(1, 20)
            name = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))
            while name in nodes:
                length = random.randint(1, 20)
                name = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))
            nodes[index] = name
            index += 1
        max_edges = len(nodes) - 1
        for i in range(0, len(nodes)):
            adjacent_nodes = self.get_adjacent(nodes[i])
            if adjacent_nodes == None:
                adjacent_nodes = []
            if len(adjacent_nodes) == max_edges:
                continue
            no_of_edges = random.randint(1, max_edges - len(adjacent_nodes))
            index2 = 0
            while index2 < no_of_edges:
                new_node = random.randint(0, len(nodes) - 1)
                if (new_node != i) and ([nodes[new_node], nodes[i]] not in edges) and ([nodes[i], nodes[new_node]] not in edges):
                    edges.append([nodes[new_node], nodes[i]])
                    edges.append([nodes[i], nodes[new_node]])
                    time_taken = random.randint(1, max_time)
                    resource_taken = random.randint(1, max_resource)
                    self.insert(nodes[i], nodes[new_node], time_taken, resource_taken)
                    index2 += 1


    def find(self, node):
        if node in self.graph:
            return True
        return False

    def dijkstra(self, nodeA, nodeB, weight1=1.0, weight2=1.0):
        q = pq.PriorityQueue()
        # ensure priority queue uses the same scalarization
        try:
            q.weight1 = weight1
            q.weight2 = weight2
        except Exception:
            pass
        nodes = list(self.graph.keys())
        time_taken = [sys.maxsize] * len(nodes)
        resources_needed = [sys.maxsize] * len(nodes)
        weighted_distance = [sys.maxsize] * len(nodes)
        previous_node = [None] * len(nodes)
        q.insert([nodeA, 0, 0])
        time_taken[nodes.index(nodeA)] = 0
        resources_needed[nodes.index(nodeA)] = 0
        weighted_distance[nodes.index(nodeA)] = 0
        while not q.empty() and len(self.graph.keys()) != 1:
            node = q.pop()
            n = node[0]
            t = node[1]
            r = node[2]
            try:
                index_n = nodes.index(n)
            except ValueError:
                # node not known in list
                continue
            # If the priority of this popped state is worse than the best known, skip
            if q.priority([n, t, r]) > weighted_distance[index_n]:
                continue
            adjacent_nodes = self.get_adjacent(n) or []
            for entry in adjacent_nodes:
                # entry format: [neighbor, time, resource]
                if not entry or len(entry) < 1:
                    continue
                n1 = entry[0]
                t1 = entry[1] if len(entry) > 1 else 0
                r1 = entry[2] if len(entry) > 2 else 0
                try:
                    index_n1 = nodes.index(n1)
                except ValueError:
                    # unknown neighbor
                    continue

                # compute candidate cumulative totals
                cand_time = time_taken[index_n] + (t1 if t1 is not None else 0)
                cand_res = resources_needed[index_n] + (r1 if r1 is not None else 0)
                # scalarize cumulative to compare
                p1 = q.priority([n1, cand_time, cand_res])

                if (weighted_distance[index_n] + p1) < weighted_distance[index_n1]:
                    weighted_distance[index_n1] = weighted_distance[index_n] + p1
                    time_taken[index_n1] = cand_time
                    resources_needed[index_n1] = cand_res
                    previous_node[index_n1] = n
                    q.insert([n1, time_taken[index_n1], resources_needed[index_n1]])

        # reconstruct path safely
        if nodeB not in nodes or nodeA not in nodes:
            return None
        reverse_path = []
        try:
            index_path = nodes.index(nodeB)
        except ValueError:
            return None
        cur = nodeB
        while cur is not None:
            reverse_path.append(cur)
            prev = previous_node[nodes.index(cur)]
            cur = prev
        reverse_path.reverse()
        # verify path starts with nodeA
        if len(reverse_path) == 0 or reverse_path[0] != nodeA:
            return None
        return reverse_path
