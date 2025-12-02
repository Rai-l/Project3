from backend.Algorithims.bfs import Graph as BFSGraph
from backend.Algorithims.adjacency_list import AdjacencyList
from typing import Dict, Any, List, Optional

def adjlist_to_bfs(adj: Dict[Any, Any]) -> BFSGraph:
    """Convert adjacency-list-with-weights (dict-of-dicts or dict-of-lists) to an unweighted BFS Graph (neighbors only).
    Ensure any node that appears only as a neighbor is also added to the BFS graph so BFS can find paths to it."""
    g = BFSGraph()
    for u, neighs in adj.items():
        g.add_node(u)
        if not neighs:
            continue
        # If neighbors is a dict (u -> {v: [w1,w2], ...})
        if isinstance(neighs, dict):
            for v in neighs.keys():
                g.add_node(v)
                g.add_edge(u, v)
        else:
            # neighs may be a list of entries like [v, t, r] or simple neighbor ids
            for item in neighs:
                if isinstance(item, (list, tuple)) and len(item) > 0:
                    v = item[0]
                else:
                    v = item
                g.add_node(v)
                g.add_edge(u, v)
    return g


def bfs_path(adj: Dict[Any, Any], start: Any, end: Any) -> Optional[List[Any]]:
    """Build a BFS graph from the given adjacency and return the shortest path from start to end.
    Returns a list of node ids in order, or None if no path exists or nodes are missing."""
    g = adjlist_to_bfs(adj)
    try:
        path = g.bfs_shortest_path(start, end)
        return path
    except Exception:
        return None

def reconstruct_from_dijkstra(nodes: List[Any], previous_node: List[Optional[Any]], start: Any, target: Any) -> Optional[List[Any]]:
    """Rebuild path returned by AdjacencyList.dijkstra (nodes, previous_node)."""
    if target not in nodes or start not in nodes:
        return None
    idx_map = {n: i for i, n in enumerate(nodes)}
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = previous_node[idx_map[cur]]
    path.reverse()
    return path if path and path[0] == start else None