from collections import Counter

MAXIMO_POR_EQUIPO = 3
MAXIMO_TRANSFERENCIAS = 4

class Equipo:
    def __init__(self, formacion, cotizacionMax, fecha):
        self.formacion = formacion
        self.cotizacionMax = cotizacionMax
        self.cotizacion = 0
        self.jugadores = []
        self.puntaje = 0
        self.fecha = fecha
        self.transferencias = 0

    def agregar(self, jugador, puedeSerSuplente):
        # si no puede ser suplente, lo agrego solo si hay espacio titular
        if (self.existe(jugador)):
            return True
        formacion = self.formacion
        jug = {}
        if puedeSerSuplente == False and not formacion.hayEspacioTitularTipo(jugador.posicion):
            return False

        jug["titular"] = formacion.hayEspacioTitularTipo(jugador.posicion)

        # si no puede entrar retorno false.
        if self.violaCotizacion(jugador) is True or not formacion.hayDisponibles(jugador.posicion):
            return False

        if self.violaMaximoPorEquipos(jugador.equipo):
            return False
        # en otro caso lo agrego feliz.
        jug["jugador"] = jugador
        self.jugadores.append(jug)
        self.cotizacion = self.cotizacion + jugador.cotizacion
        if jug["titular"]:
            self.puntaje = self.puntaje + jugador.puntajes[self.fecha]

        formacion.agregar(jugador.posicion)
        return True

    def violaCotizacion(self, jugador):
        return self.cotizacion + jugador.cotizacion > self.cotizacionMax

    def violaMaximoPorEquipos(self, equipo):
        equipos = [j["jugador"].equipo for j in self.jugadores]
        cnt = Counter(equipos)
        cantidad = cnt[equipo]

        return cantidad + 1 > MAXIMO_POR_EQUIPO

    def equipoTitularCompleto(self):
        return self.formacion.hayEspacioTitular() is False

    def existe(self, jugador):
        for j in self.jugadores:
            if j["jugador"].id == jugador.id:
                return True
        return False

    def mejorar(self, jugadores):
        jugadores.sort(key=lambda y: y.sensibilidad[self.fecha], reverse=True)
        self.jugadores.sort(key=lambda y: y["jugador"].sensibilidad[self.fecha], reverse=False)
        for nuevo in jugadores:
            if(self.existe(nuevo)):
                continue
            for antiguo in self.jugadores:
                jugAct = antiguo["jugador"]
                if (jugAct.posicion == nuevo.posicion and jugAct.sensibilidad[self.fecha] < nuevo.sensibilidad[
                    self.fecha]):
                    if self.intercambiar(antiguo, nuevo):
                        break

        self.reordenarTitulares()


    def __str__(self):
        return "Fecha: {}\nFormación: {} \nPuntaje: {} \nCotizacion: {}\nJugadores: {}".format(self.fecha + 1,
                                                                                               self.formacion,
                                                                                               self.puntaje,
                                                                                               self.cotizacion,
                                                                                               len(self.jugadores))

    def intercambiar(self, jugAct, nuevo):
        self.remover(jugAct)
        res = self.agregar(nuevo, True)
        if not res:
            self.agregar(jugAct["jugador"], True)
        return res

    def remover(self, jugAct):
        self.jugadores.remove(jugAct)
        self.cotizacion = self.cotizacion - jugAct["jugador"].cotizacion
        if jugAct["titular"]:
            self.puntaje = self.puntaje - jugAct["jugador"].puntajes[self.fecha]
        self.formacion.quitar(jugAct["jugador"].posicion)

    def clonar(self):
        eq = Equipo(self.formacion.clonar(), self.cotizacionMax, self.fecha)
        for j in self.jugadores:
            eq.agregar(j["jugador"], True)
        return eq

    def reordenarTitulares(self):
        jugadores = sorted(self.jugadores, key=lambda y: y["jugador"].sensibilidad[self.fecha], reverse=True)
        self.jugadores = []
        self.cotizacion = 0
        self.puntaje = 0
        self.formacion.reset()
        for j in jugadores:
            self.agregar(j["jugador"], True)
