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
		formacion = self.formacion
		jug = {}
		if puedeSerSuplente == False and not formacion.hayEspacioTitularTipo(jugador.posicion):
			return False
		
		jug["titular"] = formacion.hayEspacioTitularTipo(jugador.posicion)

		## si no puede entrar retorno false.		
		if self.violaCotizacion(jugador) is True or formacion.hayDisponibles(jugador.posicion) is False:
			return False

		#en otro caso lo agrego feliz.
		jug["jugador"] = jugador
		self.jugadores.append(jug)
		self.cotizacion = self.cotizacion + jugador.cotizacion
		self.puntaje = self.puntaje + jugador.puntajes[self.fecha]
		formacion.agregar(jugador.posicion)
		return True
		

	def violaCotizacion(self, jugador):
		return self.cotizacion + jugador.cotizacion > self.cotizacionMax

	def equipoTitularCompleto(self):
		return self.formacion.hayEspacioTitular() is False

	def __str__(self):
		return "Fecha: " +str(self.fecha) + "\nFormacion: " + str(self.formacion) + "\nPuntaje: " + str(self.puntaje) \
		+ "\nCotizacion: " + str(self.cotizacion)
