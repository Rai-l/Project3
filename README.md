# Project3
Usage of program:
Program start with an initial sample data of adjacent list that generates the visual graph:
{
    "N0": {"N1": [12, 1], "N3": [5, 2]},
    "N1": {"N2": [3, 4], "N4": [8,2]},
    "N2": {"N0": [9, 4]},
    "N3": {"N2": [4,2], "N5": [7,1]},
    "N4": {"N3": [1,6]},
    "N5": {}
}
Graph:
Single-clicking a node sets a new selected node
Double-clicking a node sets a new selected source/start node
Triple-clicking a node sets a new end node 

Clicking on graph deselects selected node

Panel:
Clicking text input shows input box for text based input, format should follow as:
Node1 Node2 weight1 weight2

This format should stay the same for any text file input as a path or dropped into file input as filepath
**note that nodes inserted must be at least 2
ex. 
N1 N2 6 4
N2 N3 1 2

Clicking file input displays file input text box which can take in filepath through typing filepath in or dropping path in

When finished writing a text/filepath submit to generate new graph.

Clicking random automatically generates a new graph.

Clicking Dijkstra generates a highlighted path of nodes corresponding to the shortest path found via the algorithm

Clicking BFS generates a highlighted path of nodes corresponding to the shortest path found via the algorithm

Any paths generated should be shown right of path in display panel as respected node ids and their weight

