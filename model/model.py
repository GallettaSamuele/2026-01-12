import copy

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._grafo = nx.Graph()
        self._insieme = []

    def getAllYears(self):
        return DAO.getAllYears()

    def fillMappaConstructoraxEta(self):
        self._mappaConstructorEta = {}
        constr_maxEta = DAO.getMaxAgeConstructor()
        for constr in constr_maxEta:
            self._mappaConstructorEta[constr[0]] = constr[1]

    def fillMappaConstructor(self):
        self._mappaConstructor = {}
        constr = DAO.getAllConstructor()
        for con in constr:
            if con.constructorId in self._mappaConstructorEta.keys():
                con.oldest_driver_dob = self._mappaConstructorEta[con.constructorId]
            self._mappaConstructor[con.constructorId] = con

    def creaNdoiGrafo(self, anno1, anno2):
        nodi = DAO.getNodiGrafo(anno1, anno2)
        for nodo in nodi:
            self._grafo.add_node(self._mappaConstructor[nodo])

    def creaArchiGrafo(self, anno1, anno2):
        archi = DAO.getArchiGrafo(anno1, anno2)
        for arco in archi:
            self._grafo.add_edge(self._mappaConstructor[arco[0]], self._mappaConstructor[arco[1]], weight=arco[2])

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self.fillMappaConstructoraxEta()
        self.fillMappaConstructor()
        self.creaNdoiGrafo(anno1, anno2)
        self.creaArchiGrafo(anno1, anno2)

    def ricorsione(self , K , parziale, rimanenti):
        if len(parziale)==K:
            if self.isValid(parziale):
                if len(self._insieme) == 0 or self.calcolaRangeEta(parziale) < self.calcolaRangeEta(self._insieme):
                    self._insieme = copy.deepcopy(parziale)
        else:
            for i in range(len(rimanenti)):
                parziale.append(rimanenti[i])
                nuovi_rimanenti = copy.deepcopy(rimanenti)
                nuovi_rimanenti.remove(rimanenti[i])
                if self.isValid(parziale):
                    self.ricorsione(K, parziale, nuovi_rimanenti)
                parziale.pop()


    def isValid(self, parziale):
        if len(parziale) <= 1:
            return True
        set_nodi = set(parziale)
        conn = nx.connected_components(self._grafo)
        for comp in conn:
            nodi_comuni = set_nodi.intersection(comp)
            if len(nodi_comuni) > 1:
                return False
        return True


    def calcolaRangeEta(self, parziale):
        lista_ordinata = sorted(parziale, key = lambda x : x.oldest_driver_dob, reverse = True)
        range =lista_ordinata[0].oldest_driver_dob - lista_ordinata[-1].oldest_driver_dob
        return range
