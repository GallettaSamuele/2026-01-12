import networkx as nx

from model.model import Model

anno1 = 2012
anno2 = 2016
m = Model()
m.creaGrafo(anno1, anno2)
nodi = list(m._grafo.nodes())
print(f"Numero costruttori: {len(nodi)}")
for nodo in nodi:
    print(nodo.constructorId , nodo.oldest_driver_dob)
conn = list(nx.connected_components(m._grafo))
m.ricorsione(2, [], nodi)
print(m._insieme)
print(m.calcolaRangeEta(m._insieme))
