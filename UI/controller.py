import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        anno1 = int(self._view._ddAnno1.value)
        anno2 = int(self._view._ddAnno2.value)
        if anno1 is None or anno1 == "" or anno2 is None or anno2 == "":
            self._view.txt_result.controls.append(ft.Text("Inserire correttamente gli anni !!!!!"))
            self._view.update_page()
            return
        if anno1 >= anno2:
            self._view.txt_result.controls.append(ft.Text("Anno1 deve essere strettamente minore di anno2 !!!!!"))
            self._view.update_page()
            return
        self._model.creaGrafo(anno1, anno2)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model._grafo.number_of_nodes()} nodi e {self._model._grafo.number_of_edges()} archi", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Ecco i nodi: ", color="blue"))
        for nodo in self._model._grafo.nodes():
            self._view.txt_result.controls.append(ft.Text(f"{nodo.__str__()}"))
        self._view.txt_result.controls.append(ft.Text(f"Ecco gli archi: ", color="blue"))
        for arco in self._model._grafo.edges(data=True):
            self._view.txt_result.controls.append(ft.Text(f"{arco[0].__str__()}  ||||  {arco[1].__str__()}  ||||  {arco[2]["weight"]}"))
        self._view.update_page()
        return

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()
        conn = sorted(nx.connected_components(self._model._grafo), key = lambda x : len(x), reverse = True)
        archi = sorted(self._model._grafo.edges(data=True), key= lambda x : x[2]["weight"], reverse= True)
        self._view.txt_result.controls.append(ft.Text(f"Archi con peso maggiore", color="blue"))
        if len(archi) >= 3:
            for i in range(3):
                self._view.txt_result.controls.append(ft.Text(f"{archi[i][0]} ||||| {archi[i][1]} |||||  Peso:  {archi[i][2]["weight"]}"))
        else:
            for i in range(len(archi)):
                self._view.txt_result.controls.append(ft.Text(f"{archi[i][0]} ||||| {archi[i][1]} |||||  Peso:  {archi[i][2]["weight"]}"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(conn)} componenti connesse", color="blue"))
        connMax = list(conn[0])
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa maggiore ha dimensione {len(connMax)}", color="blue"))
        for nodo in connMax:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.__str__()}"))
        self._view.update_page()
        return


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        numC = int(self._view._txtInK.value)
        nodi = self._model._grafo.nodes()
        self._model.ricorsione(numC, [], nodi)
        for nodo in self._model._insieme:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.__str__()}"))
        self._view.update_page()
        return

    def fillDDAnno(self):
        anni = self._model.getAllYears()
        for anno in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(anno))
            self._view._ddAnno2.options.append(ft.dropdown.Option(anno))