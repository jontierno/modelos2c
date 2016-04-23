
set FECHAS;
set FORMACIONES;
param MAXPRESUPUESTO;	
param MULTIPLICADORCAPITAN;
param MAXIMOPOREQUIPO;
param SUPLENTESPORPUESTO;
param MAXIMATRANSFERENCIASPORFECHA;
param SUPLENTESLIBRES;

param TAMEQUIPO := 11+ SUPLENTESPORPUESTO *4 + SUPLENTESLIBRES;
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

param CANTFECHAS  := card(FECHAS);

#defino cuantos jugadores maximos por posicion por la formacion seleccionada
param JUGADORESPORFORMACION {p in POSICIONES, f in FORMACIONES};

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


#Binaria que indica si el jugador pertenece al equipo una fecha (1)
var EQUIPO{(i,j,k) in JUGADORES, l in FECHAS}, binary;

#Binaria que indica si el jugador (i,j,k) es titular (1) en la fecha (l)
var TITULARES{(i,j,k) in JUGADORES, l in FECHAS}, binary;

#Binaria que indica el capitan por fecha (1).
var CAPITAN{(i,j,k) in JUGADORES, l in FECHAS}, binary;

#Binaria que indica la formación seleccionada (1)
var FORMACIONSEL {f in FORMACIONES}, binary;

#puntaje obtenido por fecha;
var PUNTAJEOBTENIDO{f in FECHAS} >= 0;

#el jugador entra entre la fecha l y l +1 al equipo
var ENTRAENEQUIPO{(i,j,k) in JUGADORES, l in FECHAS: l < CANTFECHAS}, binary;

#
var SULPLENTESLIBRESENPOSICION {p in POSICIONES}, binary;
maximize z: sum {f in FECHAS} PUNTAJEOBTENIDO [f] ;



#un jugador no puede ser titular en una fecha si no es del equipo.
s.t. CONDEQUIPO{(i,j,k) in JUGADORES, l in FECHAS}:  TITULARES[i,j,k,l] <= EQUIPO[i,j,k, l];

#el equipo no puede tener ni mas ni menos de 15 jugadores
s.t. CONDGRUPO{l in FECHAS}: sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k,l] = TAMEQUIPO;

#el equipo no puede tener ni mas ni menos de 11 titulares por fecha
s.t. CONDTITULARES{f in FECHAS}: sum{(i,j,k) in JUGADORES} TITULARES[i,j,k,f] = 11;

#no puedo sobrepasar el presupuesto en ninguna fecha
s.t. CONDMAXIMOPRESUPUESTO {l in FECHAS}: sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k,l] * COTIZACIONES[i,j,k] <= MAXPRESUPUESTO;

#un capitan por fecha
s.t. CONDCAPITAN {l in FECHAS}: sum{(i,j,k) in JUGADORES} CAPITAN[i,j,k,l] = 1;

#el capitan no puede serlo si no es titular en la fecha
s.t. CONDTITULARCAP {(i,j,k) in JUGADORES, l in FECHAS}: CAPITAN[i,j,k,l] <= TITULARES[i,j,k,l];

#no puedo tener mas de MAXIMOPOREQUIPO jugadores  de un mismo equipo en ninguna fecha
s.t. CONDJUGADORESPOREQUIPO {e in EQUIPOS, l in FECHAS}: sum{(i,j,k) in JUGADORES} JUEGAEN[i,j,k,e] * EQUIPO[i,j,k,l] <= MAXIMOPOREQUIPO; 

#en cada fecha hay que respetar la formacion
s.t. CONDFORMACION {l in FECHAS, p in POSICIONES}: 
		sum{(i,j,k) in JUGADORES} (JUEGADE[i,j,k,p] * TITULARES [i,j,k,l]) = 
		sum{f in FORMACIONES} JUGADORESPORFORMACION[p, f] * FORMACIONSEL[f];


#

s.t. CONDNOJUEGASINOESTABAYNOENTRA{(i,j,k) in JUGADORES, l in FECHAS: l < CANTFECHAS}: 
		 EQUIPO[i,j,k,l+1] <= EQUIPO[i,j,k,l] + ENTRAENEQUIPO[i,j,k,l];

s.t. CONDNOENTRA{(i,j,k) in JUGADORES, l in FECHAS: l < CANTFECHAS}:  
	 EQUIPO[i,j,k,l+1] >= ENTRAENEQUIPO[i,j,k,l];

s.t. CONDNOENTRASIESTAENAMBASFECHAS{(i,j,k) in JUGADORES, l in FECHAS: l < CANTFECHAS}:  
	 2 - EQUIPO[i,j,k,l] - EQUIPO[i,j,k,l+1] >= ENTRAENEQUIPO[i,j,k,l];


#En el equipo no pueden entrar mas jugadores que MAXIMATRANSFERENCIASPORFECHA
s.t. CONDMAXIMASTRANSFERENCIASPORFECHA{l in FECHAS: l < CANTFECHAS}:  
		sum {(i,j,k) in JUGADORES} (ENTRAENEQUIPO[i,j,k,l]) <= MAXIMATRANSFERENCIASPORFECHA;

#en cada fecha solo se pueden asignar mas suplentes como SUPLENTESLIBRES se indiquen
s.t. CONDMAXSUMPLENTESLIBRES: sum{p in POSICIONES} SULPLENTESLIBRESENPOSICION[p] = SUPLENTESLIBRES;

#por puesto tiene que haber SUPLENTESPORPUESTO suplentes.
s.t. CONDSUPLENTES {p in POSICIONES, l in FECHAS}: 
		sum{(i,j,k) in JUGADORES} (JUEGADE[i,j,k,p] * EQUIPO[i,j,k,l]) = 
		sum{f in FORMACIONES} (JUGADORESPORFORMACION[p, f] + SUPLENTESPORPUESTO)* FORMACIONSEL[f] + SULPLENTESLIBRESENPOSICION[p];




#solo una formacion seleccionada
s.t. CONDUNAFORMACION: sum{f in FORMACIONES} FORMACIONSEL[f] = 1;

#armo una variable de puntaje por fecha para poder expresarlo mas facil
s.t. CONDPUNTAJEPORFECHA{f in FECHAS}: 
PUNTAJEOBTENIDO[f] = sum {(i,j,k) in JUGADORES} (PUNTAJES_BASICOS[i, j, k, f] * (TITULARES[i,j,k,f] + CAPITAN[i,j,k,f])); 
solve;


#Máximo 


#Impresión de la salida.
printf "\n***** EL PUNTAJE OBTENIDO ES %i *****\n", z;




for {i in FORMACIONES: FORMACIONSEL[i] = 1}
{
	printf "\n***** LA FORMACIÓN SELECCIONADA ES %s *****\n",i;
}


printf "\n***** DATOS POR FECHA *****\n\n";

for {f in FECHAS} 
{
	printf "********** FECHA %i **********\n", f;
	printf "EQUIPO SELECCIONADO: \n";
	for {(i,j,k) in JUGADORES: EQUIPO[i,j,k,f] = 1}
	{ 
	  printf " %s, Posición: %s, Equipo: %s \n", i,j,k;

	}

	printf "\nCOTIZACIÓN %i\n", sum{(i,j,k) in JUGADORES} EQUIPO[i,j,k,f] * COTIZACIONES[i,j,k];
	printf "\n\nTITULARES: \n";
	for {(i,j,k) in JUGADORES: TITULARES[i,j,k,f] = 1}
	{ 
	  printf "	%s, Posición: %s, Equipo: %s \n", i,j,k;
	}

	for {(i,j,k) in JUGADORES: CAPITAN[i,j,k,f] = 1}
	{ 
	  printf "\n El Capitan es %s %s %s\n", i,j,k;
	}
	
	for {i in 1..1: f > 1}
	{ 
	 printf "\nJUGADORES QUE ENTRARON EN ESTA FECHA: \n"; 
	}
	
	for {(i,j,k) in JUGADORES: f > 1 && EQUIPO[i,j,k,f-1] = 0 && EQUIPO[i,j,k,f] = 1}
	{ 
	  printf "	%s, Posición: %s, Equipo: %s \n", i,j,k;
	}

	for {i in 1..1: f < CANTFECHAS}
	{ 
	 printf "\nJUGADORES QUE SALIERON EN ESTA FECHA: \n"; 
	}
	for {(i,j,k) in JUGADORES: f < CANTFECHAS && EQUIPO[i,j,k,f] = 1 && EQUIPO[i,j,k,f + 1] = 0}
	{ 
	  printf "	%s, Posición: %s, Equipo: %s \n", i,j,k;
	}
	printf "\nPUNTAJE OBTENIDO: %i\n\n", PUNTAJEOBTENIDO[f]; 

}
	printf "\nHAY MAS SUPLENTES EN: "; 	
	for {p in POSICIONES: SULPLENTESLIBRESENPOSICION[p] = 1}
	{ 
	  printf "%s\n", p;

	}

end;