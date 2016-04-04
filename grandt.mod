
# conjunto de jugadores y fechas;

set FECHAS;
set FORMACIONES;
param MAXPRESUPUESTO;	
param MULTIPLICADORCAPITAN;
param MAXIMOPOREQUIPO;
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



#leo los datos del csv
table resultados IN "CSV" "GranDT2015_formatted.csv": JUGADORES <- [Jugador,Puesto,Equipo], COTIZACIONES~Cotizacion,
PUNTAJES1~F1, PUNTAJES2~F2, PUNTAJES3~F3, PUNTAJES4~F4, PUNTAJES5~F5, PUNTAJES6~F6, PUNTAJES7~F7, 
PUNTAJES8~F8, PUNTAJES9~F9, PUNTAJES10~F10, PUNTAJES11~F11, PUNTAJES12~F12, PUNTAJES13~F13, PUNTAJES14~F14, 
PUNTAJES15~F15;


#extraigo los equipos y las posiciones
set POSICIONES dimen 1 := setof{(i,j,k) in JUGADORES}(j);
set EQUIPOS dimen 1 := setof{(i,j,k) in JUGADORES}(k);

#El jugador i,j,k juega en la posicion m
param JUEGADE 'el jugador juega de' {(i,j,k) in JUGADORES, m in POSICIONES} := if j = m then 1 else 0 binary;

#El jugador i,j,k juega en el equipo e
param JUEGAEN 'el jugador juega en' {(i,j,k) in JUGADORES, e in EQUIPOS} := if k = e then 1 else 0 binary;


#Puntaje por fecha
param PUNTAJES_BASICOS {(i,j,k) in JUGADORES, l in FECHAS} := if l = 1 then PUNTAJES1[i,j,k] else 
if l = 2 then PUNTAJES2[i,j,k] else if l = 3 then PUNTAJES3[i,j,k] else if l = 4 then PUNTAJES4[i,j,k] else 
if l = 5 then PUNTAJES5[i,j,k] else if l = 6 then PUNTAJES6[i,j,k] else if l = 7 then PUNTAJES7[i,j,k] else 
if l = 8 then PUNTAJES8[i,j,k] else if l = 9 then PUNTAJES9[i,j,k] else if l = 10 then PUNTAJES10[i,j,k] else 
if l = 11 then PUNTAJES11[i,j,k] else if l = 12 then PUNTAJES12[i,j,k] else if l = 13 then PUNTAJES13[i,j,k] else 
if l = 14 then PUNTAJES14[i,j,k] else PUNTAJES15[i,j,k];

printf: "\n****** Han sido leidos %i jugadores ****** \n", card (JUGADORES);
printf: "****** Han sido leidos %i equipos     ****** \n", card (EQUIPOS);
printf: "****** Han sido leidas %i posiciones   ****** \n\n", card (POSICIONES);


#Binaria que indica si el jugador pertenece al equipo (1)
var EQUIPO{(i,j,k) in JUGADORES}, binary;

#Binaria que indica si el jugador (i,j,k) es titular en la fecha (l)
var TITULARES{(i,j,k) in JUGADORES, l in FECHAS}, binary;

#Binaria que indica el capitan por fecha.
var CAPITAN{(i,j,k) in JUGADORES, l in FECHAS}, binary;


maximize z: sum {(i,j,k) in JUGADORES, l in FECHAS} (PUNTAJES_BASICOS[i, j, k, l] * (TITULARES[i,j,k,l] + CAPITAN[i,j,k,l])) ;



#un jugador no puede ser titular en una fecha si no es del equipo.
s.t. CONDEQUIPO{(i,j,k) in JUGADORES, l in FECHAS}:  TITULARES[i,j,k,l] <= EQUIPO[i,j,k];

#el equipo no puede tener ni mas ni menos de 15 jugadores
s.t. CONDGRUPO: sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k] = 15;

#no puedo sobrepasar el presupuesto
s.t. CONDMAXIMOPRESUPUESTO: sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k] * COTIZACIONES[i,j,k] <= MAXPRESUPUESTO;

#un capitan por fecha
s.t. CONDCAPITAN {l in FECHAS}: sum{(i,j,k) in JUGADORES} CAPITAN[i,j,k,l] = 1;

#no puedo tener mas de MAXIMOPOREQUIPO jugadores  de un mismo equipo
s.t. CONDJUGADORESPOREQUIPO {e in EQUIPOS}: sum{(i,j,k) in JUGADORES} JUEGAEN[i,j,k,e] * EQUIPO[i,j,k] <= MAXIMOPOREQUIPO; 



end;