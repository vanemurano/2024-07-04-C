from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.DiGraph() # orientato e pesato
        self._nodes=[]
        self._idMapSightings={}
        for s in DAO.get_all_sightings():
            self._idMapSightings[s.id]=s

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self, year):
        return DAO.getAllShapes(year)

    def buildGraph(self, year, shape):
        self._nodes=[]
        self._graph.clear()
        self._nodes=DAO.getAllNodes(year, shape)
        for s1, s2, peso in DAO.getAllEdges(self._idMapSightings, year, shape):
            if s1 in self._nodes and s2 in self._nodes:
                self._graph.add_edge(s1, s2, weight=peso)

    def archiMax(self):
        archi=list(self._graph.edges(data="weight"))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[0:5]

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)
