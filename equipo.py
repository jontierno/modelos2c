from collections import Counter

MAXIMO_POR_EQUIPO=3

class Equipo:

	def __init__(self, formacion , cotizacionMax, fecha):
		self.formacion = formacion
		self.cotizacionMax = cotizacionMax
		self.cotizacion = 0
		self.jugadores = []
		self.puntaje = 0
		self.fecha = fecha

	def agregar(self, jugador, puedeSerSuplente):
		 #si no puede ser suplente, lo agrego solo si hay espacio titular
		if(self.existe(jugador)):
			return False
		formacion = self.formacion
		jug = {}
		if puedeSerSuplente == False and not formacion.hayEspacioTitularTipo(jugador.posicion):
			return False
		
		jug["titular"] = formacion.hayEspacioTitularTipo(jugador.posicion)

		## si no puede entrar retorno false.		
		if self.violaCotizacion(jugador) is True or not formacion.hayDisponibles(jugador.posicion):
			return False

		if self.violaMaximoPorEquipos(jugador.equipo):
			return False
		#en otro caso lo agrego feliz.
		jug["jugador"] = jugador
		self.jugadores.append(jug)
		self.cotizacion = self.cotizacion + jugador.cotizacion
		if jug["titular"]:
			self.puntaje = self.puntaje + jugador.puntajes[self.fecha]
			
		formacion.agregar(jugador.posicion)
		return True
	
#	def reordenarTitulares():
#		for j in jugadores:
#			for j2 in jugadores:
#				if self.esMejorQue(j,j2):
#					self.intercambiar(j,j2)
#				elif:
#				if(j["titular"])

	def violaCotizacion(self, jugador):
		return self.cotizacion + jugador.cotizacion > self.cotizacionMax

	def violaMaximoPorEquipos(self, equipo):
		equipos = [j["jugador"].equipo for j in self.jugadores]
		cnt = Counter(equipos)
		cantidad = cnt[equipo];
		
		return cantidad +1 > MAXIMO_POR_EQUIPO


	def equipoTitularCompleto(self):
		return self.formacion.hayEspacioTitular() is False

	def existe(self,jugador):
		for j in self.jugadores:
			if j["jugador"].id == jugador.id:
				return True
		return False

	def __str__(self):
		return "Fecha: {}\nFormación: {} \nPuntaje: {} \nCotizacion: {}\nJugadores: {}".format(self.fecha +1, self.formacion, self.puntaje, self.cotizacion, len(self.jugadores))
