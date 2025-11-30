import random
import string
import sys
import backend.Algorithims.priority_queue as pq

class AdjacencyList:
    def __init__(self):
        self.graph = {}

    def insert(self, point_A, point_B, time_taken, resource_needed):
        if len(self.graph) == 1:
            self.graph.clear()
        val1 = [point_B, time_taken, resource_needed]
        val2 = [point_A, time_taken, resource_needed]
        if point_A not in self.graph.keys():
            self.graph.update({point_A : []})
        if point_B not in self.graph.keys() and point_B is not None:
            self.graph.update({point_B : []})
        self.graph[point_A].append(val1)
        if point_B is not None:
            self.graph[point_B].append(val2)

    def get_adjacent(self, node):
        return self.graph.get(node)

    def get_graph(self):
        return self.graph

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

    def dijkstra(self, nodeA, weight1, weight2):
        q = pq.PriorityQueue(weight1, weight2)
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
            index_n = nodes.index(n)
            if q.priority([n, t, r]) > weighted_distance[index_n]:
                continue
            adjacent_nodes = self.get_adjacent(n)
            for i in range(0, len(adjacent_nodes)):
                n1 = adjacent_nodes[i][0]
                t1 = adjacent_nodes[i][1]
                r1 = adjacent_nodes[i][2]
                p1 = q.priority([n1, t1, r1])
                index_n1 = nodes.index(n1)
                if (weighted_distance[index_n] + p1) < weighted_distance[index_n1]:
                    weighted_distance[index_n1] = weighted_distance[index_n] + p1
                    time_taken[index_n1] = time_taken[index_n] + t1
                    resources_needed[index_n1] = resources_needed[index_n] + r1
                    previous_node[index_n1] = n
                    q.insert([n1, time_taken[index_n1], resources_needed[index_n1]])
        return nodes, time_taken, resources_needed, weighted_distance, previous_node

