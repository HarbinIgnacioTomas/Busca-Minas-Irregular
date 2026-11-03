class celdaLogica():
    def __init__(self, coordenadas):
        self.coordenadas = list(coordenadas)
        self.valor = None
        self.es_mina = False
        self.oculta = True
        self.celda_segura = False
        self.vecinas = set()

    def es_celda_grande(self):
        return True if len(self.coordenadas) == 4 else False












