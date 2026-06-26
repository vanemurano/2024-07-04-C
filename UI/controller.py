import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year=None

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._year is None:
            self._view.txt_result1.controls.append(
                ft.Text("Selezionare prima un anno!", color="red"))
            self._view.update_page()
            return
        shape=self._view.ddshape.value
        if shape is None:
            self._view.txt_result1.controls.append(
                ft.Text("Selezionare prima una forma!", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(self._year, shape)
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNNodes()}\n"
                    f"Numero di archi: {self._model.getNEdges()}\n"
                    f"I 5 archi di peso maggiore sono:"))
        for s1, s2, peso in self._model.archiMax():
            self._view.txt_result1.controls.append(
                ft.Text(f"{s1.id} -> {s2.id} | weight = {peso}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDYear(self):
        anni=self._model.getAllYears()
        anniOpt=list(map(lambda x: ft.dropdown.Option(text=x,
                                                      data=x,
                                                      on_click=self.readDDYear), anni))
        self._view.ddyear.options=anniOpt
        self._view.update_page()

    def fillDDShape(self):
        shapes = self._model.getAllShapes(self._year)
        shapeOpt = list(map(lambda x: ft.dropdown.Option(x), shapes))
        self._view.ddshape.options = shapeOpt
        self._view.update_page()

    def readDDYear(self, e):
        self._year=None
        self._year=e.control.data
        self.fillDDShape()