
import math
MU = 1
class Jugador:

	def __init__(self, id, nombre, posicion, equipo, cotizacion, puntajes):
		self.id = id
		self.nombre = nombre
		self.posicion = posicion
		self.equipo = equipo
		self.cotizacion = cotizacion
		self.puntajes = puntajes
		self.puntajeTotal = sum (puntajes)
		self.sensibilidad = []

		media = sum(puntajes) / len(puntajes)
		restas = [(x - media) * (x - media) for x in puntajes]
		varianza = math.sqrt(sum(restas) / len(restas))
		for i in puntajes:
			self.sensibilidad.append(self.calcularIndiceSensibilidad(i, varianza, media))


	def calcularIndiceSensibilidad (self, puntaje, varianza, media ):
		return  puntaje + media
		#return puntaje

	def __str__(self):
		return "{} {} {} {}".format(self.nombre, self.posicion, self.equipo, self.cotizacion)