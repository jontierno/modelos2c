
# conjunto de jugadores y fechas;

set JUGADORES;
set FECHAS;

#
var EQUIPO{i in JUGADORES}, BINARY;
var TITULARES{i in JUGADORES, j in FECHAS}, BINARY;
param PUNTOS_BASICOS{i in JUGADORES, j IN FECHAS}


maximize z: sum {i JUGADORES} sum{j in FECHAS} (PUNTOS_BASICOS[i, j] * TITULARES[i,j]) ;



#un jugador no puede ser titular en una fecha si no es del equipo.
s.t. EQUIPO{i in JUGADORES, j in FECHAS}:  TITULARES[i, j] <= EQUIPO[i];

#el equipo no puede tener ni mas ni menos de 15 jugadores
s.t. MAXEQUIPO: sum{i in JUGADORES} EQUIPO[i] = 15;


