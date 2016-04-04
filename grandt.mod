
# conjunto de jugadores y fechas;

set FECHAS;
set FORMACIONES;

set JUGADORES dimen 3;

param COTIZACIONES 'el jugador cotiza' {(i,j,k) in JUGADORES};
param PUNTAJES1 'el jugador en la fecha 1 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES2 'el jugador en la fecha 2 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES3 'el jugador en la fecha 3 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES4 'el jugador en la fecha 4 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES5 'el jugador en la fecha 5 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES6 'el jugador en la fecha 6 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES7 'el jugador en la fecha 7 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES8 'el jugador en la fecha 8 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES9 'el jugador en la fecha 9 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES10 'el jugador en la fecha 10 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES11 'el jugador en la fecha 11 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES12 'el jugador en la fecha 12 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES13 'el jugador en la fecha 13 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES14 'el jugador en la fecha 14 puntuó' {(i,j,k) in JUGADORES};
param PUNTAJES15 'el jugador en la fecha 15 puntuó' {(i,j,k) in JUGADORES};



table resultados IN "CSV" "GranDT2015_formatted.csv": JUGADORES <- [Jugador,Puesto,Equipo], COTIZACIONES~Cotizacion,
PUNTAJES1~F1, PUNTAJES2~F2, PUNTAJES3~F3, PUNTAJES4~F4, PUNTAJES5~F5, PUNTAJES6~F6, PUNTAJES7~F7, 
PUNTAJES8~F8, PUNTAJES9~F9, PUNTAJES10~F10, PUNTAJES11~F11, PUNTAJES12~F12, PUNTAJES13~F13, PUNTAJES14~F14, 
PUNTAJES15~F15;


set POSICIONES dimen 1 := setof{(i,j,k) in JUGADORES}(j);
set EQUIPOS dimen 1 := setof{(i,j,k) in JUGADORES}(k);


param PUESTOS 'el jugador juega de' {(i,j,k) in JUGADORES, m in POSICIONES} := if j = m then 1 else 0 binary;
printf: "\n****** Han sido leidos %i jugadores ****** \n", card (JUGADORES);
printf: "****** Han sido leidos %i equipos     ****** \n", card (EQUIPOS);
printf: "****** Han sido leidas %i posiciones   ****** \n\n", card (POSICIONES);


var EQUIPO{(i,j,k) in JUGADORES}, binary;
var TITULARES{(i,j,k) in JUGADORES, l in FECHAS}, binary;

var xi >= 0;

minimize z : xi;

#maximize z: sum {i JUGADORES} sum{j in FECHAS} (PUNTOS_BASICOS[i, j] * TITULARES[i,j]) ;



#un jugador no puede ser titular en una fecha si no es del equipo.
s.t. COND{(i,j,k) in JUGADORES, l in FECHAS}:  TITULARES[i,j,k,l] <= EQUIPO[i,j,k];

#el equipo no puede tener ni mas ni menos de 15 jugadores
s.t. MAXEQUIPO: sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k] = 15;








end;