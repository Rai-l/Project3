# bfs.py

from collections import deque
from typing import Any, Dict, List, Optional


class Graph:
    """Represents an undirected graph and provides BFS functionality.

    The graph is stored as an adjacency list where keys are nodes and values are
    lists of neighboring nodes. Nodes can be of any hashable type.

    Attributes:
        adjacency_list (Dict[Any, List[Any]]): Mapping of nodes to their neighbors.
    """

    def __init__(self) -> None:
        """Initializes an empty graph.

        This constructor sets up an empty adjacency list, ready to add nodes and edges.
        """
        self.adjacency_list: Dict[Any, List[Any]] = {}

    def add_node(self, node: Any) -> None:
        """Adds a node to the graph if it doesn't already exist.

        This method ensures that the node is present in the adjacency list without
        duplicating entries. It's called automatically when adding edges if needed.

        Args:
            node (Any): The node to add; it must be hashable.
        """
        if node not in self.adjacency_list:
            # Initialize an empty list for neighbors if the node is new
            self.adjacency_list[node] = []

    def add_edge(self, node1: Any, node2: Any) -> None:
        """Adds an undirected edge between two nodes.

        If the nodes do not exist, they are added to the graph automatically.
        This method ensures no duplicate edges are added between the same pair of nodes.

        Args:
            node1 (Any): The first node. Must be hashable.
            node2 (Any): The second node. Must be hashable.
        """
        # Ensure both nodes are in the graph
        self.add_node(node1)
        self.add_node(node2)
        
        # Add node2 to node1's neighbors if not already present
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        
        # Add node1 to node2's neighbors if not already present (undirected)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)

    def bfs_shortest_path(self, start_node: Any, end_node: Any) -> Optional[List[Any]]:
        """Performs BFS to find the shortest path from start_node to end_node.

        Uses a queue for BFS traversal and tracks parent nodes to reconstruct the
        path. This is suitable for unweighted graphs where the shortest path is
        defined by the fewest edges. The algorithm explores level by level.

        Args:
            start_node (Any): The starting node for the search. Must exist in the graph.
            end_node (Any): The target node to find the path to. Must exist in the graph.

        Returns:
            Optional[List[Any]]: The shortest path as a list of nodes from start_node
                to end_node, or None if no path exists.

        Note:
            This method uses an iterative approach with a queue to avoid recursion
            depth issues for large graphs, adhering to better performance for large
            inputs as per guidelines. Time complexity is O(V + E), where V is vertices
            and E is edges.
        """
        # Early exit if start or end node is not in the graph
        if start_node not in self.adjacency_list or end_node not in self.adjacency_list:
            return None

        # Set to keep track of visited nodes to avoid revisiting
        visited: set[Any] = set()
        
        # Dictionary to track parent of each node for path reconstruction
        parent: Dict[Any, Any] = {}
        
        # Queue for BFS, using deque for efficient pops from left
        queue: deque[Any] = deque()

        # Enqueue start node and mark as visited
        queue.append(start_node)
        visited.add(start_node)
        parent[start_node] = None  # Start node has no parent

        # Flag to indicate if the end node is found
        found: bool = False
        
        # Main BFS loop
        while queue:
            # Dequeue the current node
            current_node = queue.popleft()
            
            # Check if we've reached the end node
            if current_node == end_node:
                found = True
                break

            # Explore neighbors
            for neighbor in self.adjacency_list[current_node]:
                if neighbor not in visited:
                    # Mark neighbor as visited to prevent re-processing
                    visited.add(neighbor)
                    
                    # Set parent for path tracing
                    parent[neighbor] = current_node
                    
                    # Enqueue neighbor for further exploration
                    queue.append(neighbor)

        # If end node not found, return None
        if not found:
            return None

        # Reconstruct the path by backtracking from end to start using parents
        path: List[Any] = []
        current: Any = end_node
        while current is not None:
            path.append(current)
            current = parent[current]
        
        # Reverse the path to get start to end order
        path.reverse()
        return path
