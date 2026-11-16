# ARCHITECTURE
How chiron works, how it interacts with the data, which tech stack we use, 
how the apps deploys at infra level.

## CHIRON
Chiron its a health solutions provided to astronauts who lives on the 
space station.

It gives to the personal inside of the ship, the capability to measure
they vital signs and alert if an annomaly it's detected.

## INFRASTRUCTURE
We use an architecture of microservices for comunication between ship,
models and monolithic apps.

- The full software runs on a Ubuntu 26.04 host.

- The host runs the docker images for the software.

- Docker image for service

- Docker compose route the whole images

We use `Github Actions Container Register` for the container images and
an a CI github actions to uploads the images from the repository.

The docker daemon runs on the background to supply continuous containers
to the backend/frontend/ML

We use CD to launch a new version of the code when we made approved chang-
es to production.

This project will grow to a cloud enviorment, the IaC will be the main idea
for this objective.

- Terraform: Build the main infra to deploy the main server
- We don't use kubernetes yet

### Comunication between the docker and exterior:

- The open port for comunication between the frontend interface and backend is: 8080
- The open port for comunication between the data stream interface and backend is: 8001

### Comunication between internal sockets:

- The open port for comunication between the backend and the ML is: 80002
- The open port for comunication between database and backend is: 3306

## MACHINE LEARNING

### Predictive model
We already train a predictive model for vital signs monitoring. This model
have an adaptative feature. It doesn't work with only trained data (that is 
another learnign that we include) but with a delta change variable, we try
to predict the next vital sign from a patron learning of the model.

Delta is the coefficent of change in the time, we want to delta stay on 
certain range, when the coefficent arrise, something it's wrong

The model gives the next JSON output:


```JSON
{
  "astronaut_id": "astro-1", "timestamp": 912.0, "model_version": "gru-v1",
  "status": "ok",                       // or "warming_up"
  "horizon_s": 120, "sample_rate_hz": 1.0,
  "baseline": {"hr": 65.0, "spo2": 98.0, ...},  // personal baseline, from the first 120 s
  "delta": {
    "per_vital": {"hr": {"window": .., "observed": .., "session": ..,
                         "danger_window": .., "danger_observed": .., "confidence": .., ...}},
    "shock_index_delta": .., "shock_index_observed": .., "confidence": ..
  },
  "zone": {
    "overall": "normal|watch|alert", "level": 0|1|2,
    "per_vital": {"hr": "watch", ...}, "shock_index": "normal",
    "reasons": [{"vital": "hr", "metric": "window_delta", "zone": "watch", "score": 0.17, "threshold": 0.157}],
    "low_confidence": false,
    "recommended_source": "ml"          // or "deterministic", meaning "trust NEWS2 instead"
  },
  "forecast": {"hr": {"p10": [...120], "p50": [...], "p90": [...]}, ...}
}
```

### Contextual model (Future feature)

This model will recieve the full context data on the pipeline, it's our last step
on the pipeline.
It uses the context given from the predictive model and the triage from the backend
to deduce from a categorize learning,  if this alert it's a false positive, an error
or is a real emergency.


## BACKEND
The backend works as a messenger:

- Comunicate the interested parts (API)
- Send the streaming data to the ML predictive model.
- Receive the alerts from the predective model and classificate on a triage
- Pass the classfication to the Contextual model.
- Comunicates to the sql base for the medical expedient and pass to the predictive 

We built the first monolithic app (Backend + Frontend) as a single docker container.
The backend uses the API to get the streaming data from the astronaut and pass it to
the ML predictive model, via API.

Then the backend listen for the alerts on the model side and when an alert gets through
the interface using defaults variables of clasification do the triage functions.

When the data gets triaged this code modules pass the full information 


## FRONTEND
Estructura del archivo
index.html
├── <head>
│   ├── fuente Roboto Mono
│   └── <style>      tokens, layout, componentes
├── <body>
│   ├── <header>     indicador de conexión, título, perfil
│   ├── <nav #crew>  selector de astronautas
│   ├── <main>       3 columnas: #cards | #astro | #cls
│   └── <svg defs>   degradado compartido de las gráficas
└── <script>
    ├── CONFIGURACIÓN
    ├── VARIABLES Y RANGOS
    ├── ESTADO
    ├── ENTRADA DE DATOS   (ingest)
    ├── CONECTORES         (ws, sse, poll)
    ├── INTERFAZ           (build*, render, classify)
    └── INICIO

Capa de presentación (CSS)
3.1 Tokens
Todo color y fuente sale de variables en :root:
Variable	Uso
--bg, --panel, --panel2	Fondo de página y dos niveles de superficie (azul profundo)
--line	Bordes
--text, --mute	Texto principal y texto secundario
--accent	Azul de acento: selección, foco y línea de encabezado
--green, --amber, --red	Los tres estados del triage
--mono	Pila tipográfica

3.2 Layout
main es una rejilla de tres columnas: minmax(300px,1.15fr) minmax(240px,.75fr) minmax(300px,1fr). Corresponden a gráficas, astronauta y clasificador.
Por debajo de 1000 px de ancho pasa a una sola columna.
El selector de astronautas (#crew) es una fila con desplazamiento horizontal.
@media (prefers-reduced-motion: reduce) desactiva todas las animaciones y transiciones.

3.3 Cómo se comunica el estado visual
Se usa una única técnica: una variable CSS local --c por elemento. JavaScript solo escribe --c (el color del estado) y el CSS decide cómo usarlo:
Elemento	Uso de --c
.card	Color del punto de estado
.chip	Color del punto de triage del astronauta
.z (zona del astronauta)	Relleno al 30% de opacidad y borde al 60%
.cls	Borde del panel y color del botón (mediante color-mix)
.desc li i	Viñeta de cada hallazgo

Datos y configuración
4.1 CONFIG
Clave	Función
mode	Selecciona el conector: ws, sse o poll. Se lee de ?mode=
url	Dirección del backend. Se lee de ?url=
pollMs	Intervalo del modo poll (1000 ms)
window	Puntos que conserva cada serie (60)
staleMs	Milisegundos sin datos para declarar "Sin señal" (5000)

4.2 VARS: definición de las variables
Es el único lugar donde se declara una variable fisiológica. De aquí se generan las tarjetas, las gráficas, la evaluación de rangos y los textos.
Campo	Significado
k	Clave que debe coincidir con la que envía el backend
name, unit	Texto visible
g	Rango verde [mín, máx]
a	Rango ámbar [mín, máx]; fuera de él es rojo
min, max	Límites del eje vertical de la gráfica
zone	Nombre de la zona corporal asociada (texto del pie del astronauta)

Valores actuales:
k	Variable	Unidad	Verde	Ámbar	Eje de la gráfica	Zona
spo2	SpO₂	%	95 a 100	90 a 100	80 a 100	Cabeza
hr	Frecuencia cardiaca	lpm	60 a 100	50 a 120	30 a 160	Corazón
rr	Frecuencia respiratoria	rpm	12 a 20	8 a 24	4 a 34	Tórax
urine	Uresis (volumen)	mL/h	30 a 100	15 a 150	0 a 200	Abdomen
bv	Volumen sanguíneo	% del basal	90 o más	80 o más	60 a 110	Piernas

4.3 Tablas auxiliares
COL: color hexadecimal de cada estado (green, amber, red), usado cuando JavaScript debe escribir un color.
RANK: orden de gravedad (green 0, amber 1, red 2), usado para calcular el peor estado.
LABEL: texto de cada nivel de triage.
MSG: textos de interpretación. Está indexado por variable, luego por dirección (0 baja, 1 alta) y luego por nivel (0 ámbar, 1 rojo). Si una variable no define la dirección alta (por ejemplo SpO₂ o volumen sanguíneo), se usa la baja.

5. Contrato de entrada
El frontend acepta un objeto o un arreglo de objetos con esta forma:
json
{
  "astronaut_id": "A-01",
  "name": "Ares",
  "ts": 1731700000000,
  "vitals": { "spo2": 97, "hr": 74, "rr": 16, "urine": 52, "bv": 98 },
  "ml": {
    "triage": "green",
    "label": "Texto del modelo",
    "prob": 0.91,
    "flags": { "spo2": "green", "hr": "amber" }
  }
}

Expectativas hacia el backend:
Un mensaje por astronauta por muestra, a ritmo regular.
Los mensajes se grafican en el orden en que llegan. El frontend no reordena ni elimina duplicados.
Para WebSocket y SSE, cada evento debe ser un JSON completo.
Para poll, el endpoint debe devolver el último estado de los astronautas (objeto o arreglo) en cada consulta.
Si el frontend se sirve por HTTPS, el WebSocket debe ser wss://. Si el backend es otro origen y se usa SSE o poll, debe habilitar CORS.

6. Modelo de estado

Todo vive en el objeto S y en una bandera de repintado:

js
S = {
  crew: Map<id, Astronauta>,   // todos los astronautas conocidos
  sel:  id,                    // astronauta seleccionado
  vk:   'spo2' | 'hr' | ...,   // variable seleccionada
  open: boolean,               // clasificador desplegado
  last: number                 // ms de la última recepción
}
let dirty = false              // hay cambios pendientes de pintar

Cada astronauta:

js
{
  id, name,
  s:    { spo2: [..], hr: [..], ... },   // series, máximo CONFIG.window puntos
  last: { spo2: 97, ... },               // último valor
  st:   { spo2: 'green', ... },          // estado por variable
  ml:   null | { ... },                  // último bloque del modelo
  tri:  'green' | 'amber' | 'red'        // triage global
}

7. Flujo de datos
  Backend
     │  (WebSocket / SSE / consulta periódica)
     ▼
  Conector ──► ingest(msg) ──► S.crew (series, last, st, ml, tri)
                                   │
                                   ├─ dirty = true
                                   └─ requestAnimationFrame(render)
                                            │
                                            ▼
                               render()  ──► tarjetas + gráficas
                                         ──► zonas del astronauta
                                         ──► chips
                                         ──► classify() ──► botón y descripción

7.1 ingest(m)
Si m es un arreglo, procesa cada elemento.
Valida astronaut_id y vitals; si faltan, termina.
Si el astronauta no existe, crea su registro, inicializa una serie vacía por variable, lo selecciona si es el primero y reconstruye los chips.
Por cada variable de VARS: convierte el valor, lo agrega a la serie, recorta a window, guarda last y fija st[k] como ml.flags[k] si existe, o rate(v, x) si no.
Guarda ml y calcula tri como ml.triage si existe, o worst(st) si no.
Registra S.last, marca dirty y pide un cuadro de animación.
7.2 render()
Cada llamada a ingest pide un cuadro de animación, pero render sale de inmediato si dirty es falso. Si llegan varios mensajes entre dos cuadros, se pinta una sola vez.
Solo pinta el astronauta seleccionado, salvo los chips, que se actualizan todos (color de triage).
Orden: chips, tarjetas y gráficas, zonas del astronauta, pie del astronauta y classify.
7.3 Evaluación de estado:
rate(v, x) devuelve green si x cae en v.g, amber si cae en v.a y red en otro caso. worst(st) devuelve el estado de mayor RANK entre las variables.

9.1 Tarjetas de gráfica (#cards):
buildCards() genera una tarjeta por entrada de VARS y guarda referencias DOM en el objeto ref (valor, línea, área, banda, cursor y etiqueta de hover), de modo que render solo actualiza atributos sin reconstruir el DOM.
Cada gráfica es un SVG con viewBox="0 0 300 64" y preserveAspectRatio="none", por lo que se estira al ancho de la tarjeta.
Elemento	Cómo se calcula
Línea y área	Para el punto i de n, x = 300 − (n−1−i)·300/(window−1) (el dato más reciente queda a la derecha y la serie crece hacia la izquierda) y y = yOf(v, valor). El área cierra hasta el borde inferior
yOf	Normaliza el valor entre min y max del eje, lo limita a ese rango y lo mapea a [4, 60] px
Banda verde	Rectángulo entre g[0] y g[1] limitados al eje, con 10% de opacidad
Punto de estado	--c de la tarjeta, según st[k]

9.2 Astronauta (#astro):
Es un SVG de viewBox="0 0 240 420" con dos clases de forma:
.body: contornos neutros (botas, brazos, manos, cuello, casco).
.z: zonas con señalética. Cada una lleva data-k con la clave de una variable.
Zona	Elemento	Variable
Visor	Elipse	spo2
Tórax	Rectángulo	rr
Corazón	Círculo con "♥" encima	hr
Abdomen	Rectángulo	urine
Piernas	Dos rectángulos	bv
render escribe --c según st[k], activa .red si el estado es rojo y .sel si es la variable seleccionada. Al hacer clic en una zona se llama a pick(k).
El pie (#cap) muestra el nombre, el valor y la zona de la variable seleccionada.

9.3 Selector de astronautas (#crew)

buildChips() genera un botón por astronauta, con aria-pressed según la selección y el color del triage global. Se reconstruye al aparecer un astronauta nuevo y al hacer clic en un chip. En los repintados normales solo se actualizan el color y aria-pressed, sin reconstruir.

9.4 Clasificador (#cls)
Parte	Comportamiento
Panel (.cls)	Su data-t toma el triage global (green, amber, red) y el CSS colorea borde y botón
Botón #cbtn	Siempre visible, con el nivel actual. Alterna la clase open y aria-expanded
Texto guía (.hint)	Visible mientras el panel está cerrado
Descripción (#desc)	Solo existe visualmente con el panel abierto. Es una región aria-live="polite"
classify(a) siempre actualiza data-t y el texto del botón. Solo si el panel está abierto reescribe la descripción, que se compone de:
El nivel de triage como título.
Si hay ml.label, una línea del modelo, con ml.prob como porcentaje cuando existe.
Una lista de hallazgos, o una frase de normalidad si no hay ninguno.
Una nota fija de que es orientativo.
findings(a) recorre VARS, omite las variables verdes y, para las demás, elige el texto de MSG según la dirección (x < g[0] es baja, en otro caso alta) y el nivel. Después añade dos patrones combinados:

Patrón	Condición	Mensaje
1. Hipovolemia o sangrado	hr > 100 y bv < 90	Pulso alto con volumen bajo 
2. Compromiso respiratorio	SpO₂ no verde y rr > 20	SpO₂ baja con respiración acelerada
Los umbrales de estos patrones están escritos directamente en findings, no en VARS.

10. Interacción
Acción	Resultado
Clic en tarjeta o en zona del astronauta	pick(k) fija S.vk y repinta: resalta tarjeta y zona, y actualiza el pie
Clic en chip	Cambia S.sel y repinta
Hover o toque en una gráfica	Cursor y valor de ese momento
Clic en CLASIFICADOR	Alterna el despliegue y repinta la descripción
11. Accesibilidad y seguridad
Tarjetas y chips son <button>, con foco visible (:focus-visible).
El estado se comunica con texto además de color (valor, nivel de triage y mensajes).
Hay aria-pressed en chips, aria-expanded en el botón del clasificador y aria-label en el SVG del astronauta.
Se respeta prefers-reduced-motion.
Todo texto que viene del backend y se inserta como HTML (name, id, ml.label) pasa por esc(), que escapa & < > ". Los textos de MSG son constantes del código.

12. Cómo extender
Agregar una variable
Añadir un objeto a VARS con k, name, unit, g, a, min, max y zone.
Añadir sus textos a MSG (bajo y, si aplica, alto; cada uno con versión ámbar y roja).
Asociar una zona del SVG del astronauta con data-k igual a k (o reutilizar una existente).
Pedir al backend que incluya vitals.<k>.
Las tarjetas, las series, la evaluación de rangos y los hallazgos se generan solos desde VARS.
Cambiar rangos o paleta
Los rangos se editan en g y a de VARS. Los colores, en :root (para CSS) y en COL (para los que escribe JavaScript); ambos deben mantenerse iguales.

Agregar un transporte nuevo:
Crear una función que reciba datos y llame a ingest(msg) y a setConn(...), y registrarla en la tabla de conectores de la sección INICIO.
Cambiar el origen del triage
No requiere cambios en el frontend: basta con que el backend envíe ml.triage y, opcionalmente, ml.flags. Las reglas locales quedan como respaldo para cuando esos campos no llegan.

13. Puntos de atención y deuda técnica
Tema	                                     |Detalle
Recuperación del indicador	                  Tras una pérdida de señal, el indicador queda en "Sin señal" en WebSocket y SSE hasta que el                                            conector se reconecte, aunque vuelvan a llegar datos. Conviene restaurar el estado "En vivo" dentro                                        de ingest
Eje de tiempo	                             "hace N s" supone una muestra por segundo. ts no se usa para posicionar los puntos
Nombre del astronauta	                      Si name cambia después de la primera recepción, el chip no se reescribe hasta que se reconstruya
Historial	                                  No hay recuperación de datos perdidos al reconectar ni persistencia al recargar
Orden y duplicados	                          No se ordenan ni se descartan mensajes repetidos
Zonas del astronauta	                      Responden a clic, pero no son accesibles con teclado (no tienen tabindex)
Umbrales de patrones	                      Los de findings están fijos en código
Valor por defecto de CONFIG.mode	          Debe fijarse al transporte de producción antes del despliegue
WebSocket	                                  No se guarda el manejador de la conexión, por lo que no se puede cerrar de forma limpia
Sin autenticación	                          Las credenciales, si se requieren, deben agregarse en el conector
Fuente	                                      Depende de Google Fonts; sin internet se usa la monoespaciada del sistema