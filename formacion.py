
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

	def agregar (self, tipo):
		if self.hayDisponibles(tipo):
			self.disponibles[tipo] = self.disponibles[tipo] - 1
			return True
		return False
	
	def hayEspacioTitularTipo(self, tipo):
		return self.suplentesPorPuesto < self.disponibles[tipo]


	def hayDisponibles(self, tipo):
		return self.disponibles[tipo] >0
	
	def hayEspacioTitular(self):
		return self.hayEspacioTitular("ARQ") or self.hayEspacioTitular("DEF") or self.hayEspacioTitular("VOL") or self.hayEspacioTitular("DEL")
	
	def __str__(self):

		return '{}-{}-{}'.format(self.cupos["DEF"], self.cupos["VOL"], self.cupos["DEL"])
     