import math


class Formacion:
    def __init__(self, defensores, volantes, delanteros, suplentesPorPuesto):
        self.arquerosDisp = 1
        self.disponibles = {}
        self.disponibles["ARQ"] = 1 + suplentesPorPuesto
        self.disponibles["DEF"] = defensores + suplentesPorPuesto
        self.disponibles["VOL"] = volantes + suplentesPorPuesto
        self.disponibles["DEL"] = delanteros + suplentesPorPuesto
        self.cupos = {}
        self.cupos["ARQ"] = 1
        self.cupos["DEF"] = defensores
        self.cupos["VOL"] = volantes
        self.cupos["DEL"] = delanteros
        self.suplentesPorPuesto = suplentesPorPuesto

    def agregar(self, tipo):
        if self.hayDisponibles(tipo):
            self.disponibles[tipo] = self.disponibles[tipo] - 1
            return True
        return False

    def quitar(self, tipo):
        if self.disponibles[tipo] < self.cupos[tipo] + self.suplentesPorPuesto:
            self.disponibles[tipo] = self.disponibles[tipo] + 1

    def hayEspacioTitularTipo(self, tipo):
        return self.suplentesPorPuesto < self.disponibles[tipo]

    def hayDisponibles(self, tipo):
        return self.disponibles[tipo] > 0

    def hayEspacioTitular(self):
        return self.hayEspacioTitular("ARQ") or self.hayEspacioTitular("DEF") or self.hayEspacioTitular(
            "VOL") or self.hayEspacioTitular("DEL")

    def printCupos(self):
        disponibles = self.disponibles
        cupos = self.cupos
        suplentesPorPuesto = self.suplentesPorPuesto
        return "ARQ: {}/{}, DEF: {}/{}, VOL: {}/{}, DEL: {}/{}".format(cupos["ARQ"] + suplentesPorPuesto - disponibles["ARQ"],
                                                                       cupos["ARQ"] + suplentesPorPuesto,
                                                                       cupos["DEF"] + suplentesPorPuesto - disponibles["DEF"],
                                                                       cupos["DEF"] + suplentesPorPuesto,
                                                                       cupos["VOL"] + suplentesPorPuesto - disponibles["VOL"],
                                                                       cupos["VOL"] + suplentesPorPuesto,
                                                                       cupos["DEL"] + suplentesPorPuesto - disponibles["DEL"],
                                                                       cupos["DEL"] + suplentesPorPuesto)

    def clonar(self):
        return Formacion(self.cupos["DEF"], self.cupos["VOL"], self.cupos["DEL"], self.suplentesPorPuesto)

    def __str__(self):
        return '({}-{}-{}) {}'.format(self.cupos["DEF"], self.cupos["VOL"], self.cupos["DEL"], self.printCupos())

    def reset(self):
        self.disponibles = {}
        self.disponibles["ARQ"] = 1 + self.suplentesPorPuesto
        self.disponibles["DEF"] = self.cupos["DEF"] + self.suplentesPorPuesto
        self.disponibles["VOL"] = self.cupos["VOL"] + self.suplentesPorPuesto
        self.disponibles["DEL"] = self.cupos["DEL"] + self.suplentesPorPuesto

    def hayAlgunEspacioDisponible(self):
        return self.hayDisponibles("ARQ") or self.hayDisponibles("DEF") or self.hayDisponibles("VOL") or self.hayDisponibles("DEL")