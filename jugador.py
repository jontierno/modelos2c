
import math
class Jugador:

	def __init__(self, id, nombre, posicion, equipo, cotizacion, puntajes):
		self.id = id
		self.nombre = nombre
		self.posicion = posicion
		self.equipo = equipo
		self.cotizacion = cotizacion
		self.puntajes = puntajes
		self.puntajeTotal = 0
		for i in puntajes:
			self.puntajeTotal = self.puntajeTotal + i
		self.sensibilidad = []
		for i in puntajes:
			self.sensibilidad.append(self.calcularIndiceSensibilidad(i))

	def calcularIndiceSensibilidad (self, puntaje):
		return self.puntajeTotal * puntaje / math.log10(self.cotizacion + 10)