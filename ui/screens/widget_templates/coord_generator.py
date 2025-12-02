import networkx as nx
from fa2 import ForceAtlas2


class CoordGenerator:
    '''
    Help generate xy coords for given adjacent list, using offset is not reccomended when using generated coords for ui positions unless needed

    Attributes:
        data(dictionary): stores current adjacent list data
        coord(dictionary): contains dictionary containing nodes as key and their respected xy coords
    '''
    def __init__(self, data=None, xoff=0, yoff=0, woff=0, hoff=0):
        self.data=data
        self.coord={}
        self.generateCoords(data)
        self.offset(xoff, yoff, woff, hoff)

    def generateCoords(self, adjList=None):
        if(adjList):
            self.data=adjList
        else:
            self.data={
                "N0": {"N1": 12, "N3": 5},
                "N1": {"N2": 3, "N4": 8},
                "N2": {"N0": 9},
                "N3": {"N2": 4, "N5": 7},
                "N4": {"N3": 6},
                "N5": {}
            }
        graph=nx.Graph()
        for key, val in self.data.items():
            if not val:
                continue
            for k, v in val.items():
                if isinstance(v, (list, tuple)) and len(v) >= 2:
                    t = 0 if v[0] is None else v[0]
                    r = 0 if v[1] is None else v[1]
                    try:
                        scalar = float(t) + float(r)
                    except Exception:
                        scalar = 1.0
                else:
                    try:
                        scalar = float(v)
                    except Exception:
                        scalar = 1.0

                if scalar is None or scalar <= 0:
                    scalar = 1.0

                graph.add_edge(key, k, weight=scalar)
        forceatlas2=ForceAtlas2(
            outboundAttractionDistribution=True,
            barnesHutOptimize=True,
            barnesHutTheta=1.2
        )
        pos=forceatlas2.forceatlas2_networkx_layout(graph, iterations=200)
        self.coord=pos


    def offset(self, xoff, yoff, width=0, height=0):
        center_f=(width/2,height/2)
        for key,val in self.coord.items():
            self.coord[key]=(val[0]+xoff+center_f[0],val[1]+yoff+center_f[1])


    def getDimensions(self):
        x=[p[0] for p in self.coord.values()]
        y=[p[1] for p in self.coord.values()]
        min_x, max_x=min(x), max(x)
        min_y, max_y=min(y), max(y)
        width=max_x-min_x
        height=max_y-min_y
        return (width,height)

    def getCoords(self):
        return self.coord