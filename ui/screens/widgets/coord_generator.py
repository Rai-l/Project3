import networkx as nx
from fa2 import ForceAtlas2
import numpy as np


class CoordGenerator:
        def __init__(self):
            self.sampleData={
                        "N0": {"N1": 12, "N3": 5},
                        "N1": {"N2": 3, "N4": 8},
                        "N2": {"N0": 9},
                        "N3": {"N2": 4, "N5": 7},
                        "N4": {"N3": 6},
                        "N5": {}
                    }
            self.coord={}

        def generateSample(self):
            self.generateCoords(self.sampleData)

        def generateCoords(self, adjList):
            graph=nx.Graph()
            for key,val in adjList.items():
                for k, v in val.items():
                    graph.add_edge(key,k,weight=v)
            forceatlas2=ForceAtlas2(
                outboundAttractionDistribution=True,
                barnesHutOptimize=True,
                barnesHutTheta=1.2
            )
            pos=forceatlas2.forceatlas2_networkx_layout(graph, iterations=200)
            self.calcDimensions(pos)
            self.coord=pos

        def offset(self, xoff, yoff, center=True):
            center_f=(xoff/2,yoff/2) if center else (0,0)
            for key,val in self.coord.items():
                for k,v in val.items():
                    v[0]=v[0]+xoff+center_f[0]
                    v[1]=v[1]+yoff+center_f[1]


        def getDimensions(self):
            x=[p[0] for p in self.coord.values()]
            y=[p[1] for p in self.coord.values()]
            min_x, max_x=min(x), max(x)
            min_y, max_y=min(y), max(y)
            width=max_x-min_x
            height=max_y-min_y
            return (width,height)