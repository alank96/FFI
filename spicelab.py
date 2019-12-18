# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# 
#  # Objetivo del laboratorio
#  El objetivo de la presenta práctica es conocer el estándar de simulación de circuitos [SPICE](http://bwrcs.eecs.berkeley.edu/Classes/IcBook/SPICE) y realizar pequeñas simulaciones en corriente continua con el mismo. SPICE es una forma elegante y sencilla de codificar circuitos eléctricos de manera que puedan ser procesados por un ordenador. Mediante un sencillo lenguaje podemos definir resistencias, fuentes de alimentación, etc., las conexiones entre ellos y los resultados que deseamos obtener.
# 
#  # El estándar SPICE
#  **SPICE** es una abreviabiación de *Simulation Program with Integrated Circtuit Emphasis*.
#  Se trata básicamente de un método estándar para describir circuitos usando texto plano en
#  lugar de una representación gráfica (o *esquemática*). A esta descripción en texto se
#  la llama también **netlist** y básicamente se corresponde con la *lista* de los componentes del circuito y cómo estos están conectados entre sí, es decir, de los nodos de unión.
#  Los ficheros netlist pueden tener extensiones `.cir`, `.net`, `.ckt`, ó `.sp` y es muy común encontrárselos con cualquiera de estas.
# 
#  Existen en el mercado muchas variantes (intérpretes) de Spice, aunque el original fue descrito
#  en la Universidad de Berkeley. En la lista de intérpretes de Spice tenemos desde esfuerzos y proyectos comerciales hasta *open source* y regidos por distintas comunidades de usuarios y programadores.
# 
# > **Pregunta:** Enumera todos los intérprete de Spice que puedas encontrar. Crea una tabla en Markdown con varias columnas (para el nombre, fabricante, versión actual, licencia y alguna característica sobresaliente). Aquí tienes un ejemplo del que puedes partir y seguir completando:
# 
# | Intérprete | Licencia | Fabricante         | Características  |
# | ---------- | -------- | ------------------ | ---------------- |
# | Ahkab      | GPL      | Giuseppe Venturini | Basado en Python |
# | PSpice/OrCAD | 	Propietario | OrCAD | 	Basado en C++ | 
# | Spice Opus  | Propietario | EDA Group| 	Basado en Python | 
# | LTSPICE | 	Propietario	| Linear Technology Corp | Basado en C++ | 
# | Qucs    | GNU | 	GNU/Linux OS | 	Basado en C++ | 
# | Gnucap  | GNU | 	GNU/Linux OS | 	Basado en C++ | 
# 
#  > **Pregunta:** ¿Qué comparación puedes efectuar entre C y Spice como estándares (lenguajes) y sus respectivas implementaciones en software? ¿Qué implementaciones reales (compiladores) del lenguaje C conoces? 
#
#  C es un lenguaje de alto nivel mientras que Spice es un lenguaje interpretado, como hemos visto en el ejercicio anterior Spice precisa de otros interpretes como C o en versiones anteriores FORTRAN.
#
#  En mi caso el compilador que usabamos para C era Microsoft visual Studio.
#  ## Elementos de un netlist
#  Como acabamos de comentar, un netlist se corresponde con la codificación de los elementos electrónicos de un circuito y las uniones entre los mismos. Veamos con más concreción qué partes y secciones lo componen.
# 
#  ## Comentarios
# 
#  La primera línea de un netlist se corresponderá siempre con un comentario. A partir de esta línea se pueden introducir más comentarios pero tienen que ir siempre precedidos de un `*`. Ejemplo:
#  
#  ```spice
#  Mi primer circuito
#  * Otro comentario
#  * más comentarios
#  *
#  ```
# 
#  ## Dispositivos básicos de un circuito
#  Los elementos de un netlist son los mismos que encontramos en cualquier circuito eléctrico sencillo,
#  tales como resistencias, **condensadores**, **bobinas**, **interruptores**, **hilos** y **fuentes** de alimentación.
#  Para distinguir uno de otro, se reserva una letra característica: `V` para fuentes de alimentación, `R` para resistencias, `C` para condensadores y `L` para bobinas. También es posible usar estas letras en su versión en minúscula (`r`, `v`, `c`, `l`, etc.).
#  Después de esta letra característica se puede sufijar cualquier texto para diferenciar un elemento de otro (números, letras, palabras, etc.). Ejemplo:
# 
#  ```
#  * Una resistencia
#  R1
#  *  Otra resistencia
#  R2
#  * Fuente de alimentación
#  V
#  * Un condensador
#  Cprincipal
#  ```
# 
#  ## Conexiones
#  A continuación de indicar el elemento eléctrico, tenemos que informar a Spice cuáles
#  son los puntos de unión tanto a un lado como al otro del elemento.
#  Así es como Spice sabe qué está conectado a qué: porque comparten un **punto**
#  (o **nodo**, aunque este término se reserva sobretodo a uniones de más de dos elementos)
#  que hemos señalizado correctamente. Para nombrar nodos, lo mejor es emplear una
#  numeración secuencial: 0...n. **La enumeración de los puntos de unión es completamente
#  a nuestro criterio**.
# 
#  ```
#  * Una resistencia
#  * entre cables 0 y 1
#  R1 0 1
#  ```
# 
#  **Sólo es necesario seguir un criterio**: en el caso de una
#  fuente de alimentación, el nodo que pondremos primero será
#  aquel que está más cerca del *borne* positivo. Ejemplo:
# 
#  ```spice
#  * Para una fuente indicamos primeramente conexión a nodo positivo.
#  v 2 3 type=vdc vdc=1
#  ```
#  
# En el *caso de LTspice* no es necesario indicar los parámetros `type=vdc` y `vdc=X`, sino que si no se especifica nada, se supone que el último valor es el del voltaje a corriente continua:
# 
# ```spice
# * Especificación de una fuente de alimentación de 10 V en corrient continua en el caso de LTspice
# v 0 1 10
# ```
# 
# Aquí tienes un ejemplo gráfico de los componentes comentados justo arriba (resistencia y voltaje):
# 
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencia%20y%20pila%20con%20nodos.svg?sanitize=true)
# 
#  ## Unidades en SPICE
# 
#  Las unidades de las magnitudes características del circuito son siempre [unidades
#  del Sistema Internacional](https://en.wikipedia.org/wiki/SI_electromagnetism_units) y no es necesario indicarlo explícitamente en el netlist.
# 
#  La forma de especificar múltiplos de estas cantidades es añadiendo una letra.
#  Básicamente las que nos interesan y las que suelen aparecer mayoritariamente son `k` para "kilo-," `m` para "mili?" y `u` para "micro?".
# 
#  > **Pregunta:** Crea una tabla en Markdown con todos los prefijos de múltiplos que puedas, su abreviatura y su equivalencia numérica.
# 
#| Prefijo     | Símbolo | Valor |
#|-------------|---------|-------|
#| yotta       | Y       | 10^24  |
#| zetta       | Z       | 10^21  |
#| exa         | E       | 10^18  |
#| peta        | P       | 10^15  |
#| tera        | T       | 10^12  |
#| giga        | G       | 10^9   |
#| mega        | M       | 10^6  |
#| kilo        | k       | 10^3   |
#| hecto       | h       | 10^2   |
#| deca        | da      | 10^1   |
#| deci        | d       | 10^−1  |
#| centi       | c       | 10^−2  |
#| mili        | m       | 10^−3  |
#| micro       | µ       | 10^−6  |
#| nano        | n       | 10^−9  |
#| pico        | p       | 10^−12 |
#| femto       | f       | 10^−15 |
#| atto        | a       | 10^−18 |
#| zepto       | z       | 10^−21 |
#| yocto       | y       | 10^−24 |
#
#  En el caso de las fuentes de alimentación hemos de especificar si se trata de corriente contínua (`vdc`) o alterna (`ac`).
# 
#  ```
#  * Una resistencia de 5 Ohmios
#  R2 1 0 5
#  * Una pila de 10 Voltios (continua)
#  V1 1 0 type=vdc vdc=10
#  * Una resistencia de 5 kΩ
#  RX 2 4 5k
#  ```
# 
#  > **Pregunta**: ¿qué unidades del Sistema Internacional relacionadas con la asignatura –y los circuitos en general– conoces? Responde aquí mismo en una celda de Markdown con una tabla.
# 
# Las que yo conozco son las siguientes:
#
#| Magnitud física básica        | Unidad Basica | Simbolo |
#|-------------------------------|---------------|---------|
#| longitud [L]                  | metro         | m       |
#| masa [M]                      | kilogramo     | Kg      |
#| tiempo [T]                    | segundo       | s       |
#| corriente eléctrica [I]       | amperio       | A       |
#| temperatura termodinámica [Θ] | kelvin        | K       |
#| cantidad de sustancia [N]     | mol           | mol     |
#| intensidad luminosa [J]       | candela       | cd      |
#
#| Cantidad física                             | Nombre        | Simbolo |
#|---------------------------------------------|---------------|---------|
#| frecuencia                                  | hercio        | Hz      |
#| fuerza                                      | newton        | N       |
#| presión                                     | pascal        | Pa      |
#| energía (incluyendo calor)                  | julio         | J       |
#| potencia y flujo radiante                   | vatio         | W       |
#| carga eléctrica                             | culombio      | C       |
#| tensión eléctrica y diferencia de potencial | voltio        | V       |
#| capacitancia                                | faradio       | F       |
#| resistencia eléctrica                       | ohmio         | Ω       |
#| campo magnético                             | tesla         | T       |
#| temperatura Celsius                         | grado Celsius | °C      |
#  ## Valores iniciales
# 
#  Aparecen justo al final de la definición del componente (`ic`). Suelen aplicarse principalmente con condensadores.
# 
#  ```
#  * Una condensador inicialmente no cargado
#  c 1 0 1u ic=0
#  ```
# 
#  ## Fin del circuito
# 
#  El fin de la descripción de un netlist se especifica mediante el
#  comando `.end`.
# 
#  ```spice
#  * Mi primer circuito
#  V 1 0 vdc=10 type=vdc
#  R 1 0 5
#  * Fin del circuito
#  .end
#  ```
# 
# 
#  ## Comandos SPICE para circuitos en corriente continua
# 
#  Además de la descripción del circuito, hemos de indicar al intérprete de Spice qué
#  tipo de análisis queremos realizar en sobre el mismo y cómo queremos presentar
#  la salida de la simulación. Los comandos en Spice empiezan por un `.` y suelen
#  escribirse justo al final del circuito, pero antes del comando `.end`.
# 
#  ```
#   Mi primer circuito
#  * Aquí van los componentes
#  R 1 0 6k
#  ...
#  * Comandos
#  .op
#  ...
#  * Fin del circuito
#  .end
#  ```
# 
#  > **Pregunta**: Hasta lo que has visto del lenguaje Spice, ¿dentro de qué tipo o conjunto de lenguajes encajaría? ¿Funcionales? ¿Específicos de dominio? ¿Procedurales? ¿Estructurados? ¿Orientado a Objetos ¿Funcionales? Justifica tu respuesta. 
#
# Creo que encajaria dentro de lenguaje especifico de dominio, ya que es un lenguaje creado explicitamente para la simulación de circuitos 
#
#  Veamos los principales comandos de simulación:
# 
#  - `.op` es el comando más sencillo que podemos emplear en. Devuelve el voltaje e intensidad en cada ramal y componente del circuito. Este comando no necesita parámetros.
#  - `.dc` es uy parecido al comando `.op` pero nos permite cambiar el valor del voltaje de una fuente de alimentación en pasos consecutivos entre el valor A y el valor B.
#  En el caso de que la fuente tuviera asignada ya un valor para su voltaje, este sería ignorado. Ejemplo:
# 
# 
#  ```spice
#  * Variamos el valor del voltaje
#  * de la fuente "v" de 1 a 1000
#  * en pasos de 5 voltios
#  v 1 0 type=vdc vdc=10
#  .dc v 1 start=1 stop=1000 step=20
#  v2a 2 4 type=vdc vdc=9
#  * Igual para v2a. Se ignora su voltaje de 9V
#  .dc v2a start=0 stop=10 step=2
#  ```
# 
#  - El comando `.tran` realiza un análisis en el tiempo de los parámetros del
#  circuito. Si no se emplea la directiva `uic` (*use initial conditions*) o esta es igual a cero, este análisis se realiza desde el punto estable de funcionamiento del circuito hasta un tiempo `tfinal`.
#  y en intervalos `tstep`. Si empleamos un varlor distinto para parámetro `uic`,
#  entonces se hará uso de las condiciones iniciales definidas para cada componente
#   (típicamente `ic=X` en el caso de los condensadores, que da cuenta de la carga incial que estos pudieran tener).
# 
# 
#  ```
#  * Hacemos avanzar el tiempo entre
#  * tinicial y tfinal en pasos tstep
#  .tran tstart=X tstop=Y tstep=Z uic=0/1/2/3
#  ```
# 
#  `X`, `Y` y `Z` tienen, evidentemente unidades de tiempo en el S.I. (segundos).
# 
#  > **Pregunta**: El parámetro `uic` puede tener varios valores y cada uno significa una cosa. Detállalo usando un celda Markdown y consultando la [documentación de Ahkab](https://buildmedia.readthedocs.org/media/pdf/ahkab/latest/ahkab.pdf).
# 
#UIC se usa para especificar el estado del circuito en el tiempo.
#En caso de que UIC sea 0, todos los voltajes y corrientes son 0.
#En caso de que UIC sea 1, se utiliza los valores del último análisis .op.
#En caso de que UIC sea 2, se utilizan los valores del último análisis .op en el que se establecen los valores de corrientes a través de inductores y voltajes en condensadores especificados en su ic
#En caso de que UIC sea 3, se utiliza un ic suministrado por el usuario.
#
#  ## Intérprete SPICE que vamos a usar: Ahkab
#  Tras un estándar siempre hay una o varias implementaciones. Ahkab no deja de ser una implmentación más en Python del estándar Spice.
#  > **Pregunta:** Comenta las distintas implementaciones de lenguajes y estándares que conozcas. Hazlo usando una tabla en Markdown. [Aquí](https://www.markdownguide.org/extended-syntax/#tables) tienes un poco de ayuda (aunque antes ya se ha puesto el ejemplo de una tabla).
#  
# | Lenguajes   | Implementación        |
# |-------------|-----------------------|
# | C++         | Orientado a objetos   |
# | SQL         | Base de datos         |
# | HTML        | Frontend              |
# | PHP         | Backend               |
# | Phyoth      | Programas             |
# | Java        | Programas             |
#
#  > **Pregunta:** Describe brevemente este software (creador, objetivos, versiones, licencia, características principales, dependencias, etc.).
# 
# Fue desarrollado por la Universidad de California, Berkeley en 1973 por Donald O. Pederson y Laurence W. Nagel, su objetivo es simular circuitos electrónicos analógicos compuestos por resistencias, condensadores, diodos, transistores, etc. Ha tenido 3 versiones SPICE, SPICE2 y la última SPICE3, tiene una licencia de tipo BSD.
# SPICE realiza los siguientes tipos de análisis:
# DC - Función de transferencia
# AC - Respuesta en frecuencia de circuito.
# Transitorio - Evolución del circuito en el tiempo.
#
#  # Trabajo práctico
#  Muy bien, ahora toca definir circuitos y ejecutar simulaciones sobre los mismos gracias a Ahkab.
#  ## Instalación de bibliotecas necesarias
#  Si estás utilizando Anaconda, asegúrate de tener su entorno activado:
#  
#  ```cmd
#  C:\> conda activate base (en el caso de Windows)
#  ```
#  ó
# 
#  ```bash
#  $ source /usr/local/Caskroom/miniconda/base/bin/activate (en el caso de macOS)
#  ```
# 
#  En el caso de Windows tienes que tener en el PATH el directorio donde se encuentre el comando `conda` (visita la sección de [Environment Variables](https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10) del [Panel de Control](https://www.digitalcitizen.life/8-ways-start-control-panel-windows-10)). Si has instalado Anaconda con [esta opción](https://docs.anaconda.com/_images/win-install-options.png) marcada, ya no tienes que preocuparte por ello. 
# 
#  Ahora ya puedes instalar Ahkab:
# 
#  ```
#  (base) $ pip install ahkab
#  ```
# 
#  Como siempre, una vez instalado cualquier framework para Python, ya lo podemos utilizar, tanto desde el [REPL](https://en.wikipedia.org/wiki/Read–eval–print_loop) como desde un entorno Jupyter (Jupyter, [Jupyterlab](http://jupyterlab.readthedocs.io/en/stable/), VS Code o nteract). Recuerda que para usar el kernel Python (que viene con Anaconda) desde nteract debes seguir las instrucciones que se indican en su [documentación oficial](https://nteract.io/kernels).  

# %%
import pylab as plt
import ahkab

# %% [markdown]
# También vamos a importar Sympy para hacer algún cálculo más *manual* más adelante:

# %%
import sympy.physics.units as u
from sympy.physics.units import Dimension 
from sympy import * 
from sympy.physics.units import convert_to

# %% [markdown]
#  > **Pregunta:** ¿Qué es y para qué sirve PyLab?
# 
# Es un conglomerado de librerias y sirve para la generación de graficos. 
#  ## Circuitos sencillos para trabjar con la ley de Ohm:
# 
#  La *mal llamada* ley de Ohm reza que el voltaje (la *energía por unidad de carga*) que se disipa en un tramo de un circuito eléctrico es equivalente a la intensidad ($I$) de la corriente (es decir, cuántos electrones circulan por unidad de tiempo) por la resistencia del material ($R$) en el que está desplazándose dicha corriente. Matemáticamente:
# 
#  $$
#  V = I\cdot R
#  $$
# 
#  > **Pregunta:** comprueba que la ecuación anterior está ajustada a nivel dimensional, es decir, que la naturaleza de lo que está a ambos lados del signo igual es la misma. Realiza este ejercicio con LaTeX en una celda Markdown.
# 
# $$
#  I(A) = \frac{V(V)}{R(\Omega)}
# $$
# $$
#  R(\Omega) = \frac{V(V)}{I(A)}  
# $$
# $$
#  V(V) = \frac{V(V)}{R(\Omega)}\cdot R(\Omega) => V(V)=V(V)
# $$
# $$
#  V(V) = \frac{V(V)}{I(A)}\cdot I(A) =>  V(V)=V(V)
# $$
#
#  Comencemos con el circuito más sencillo posible de todos:
# 
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/primer%20circuito.svg?sanitize=true)
# 
#  Vamos a escribir su contenido (componentes o *netlist*) en disco con el nombre `circuito sencillo.sp`. Esto lo podemos lograr directamente y en tiempo real desde una celda de Jupyter gracias a los *comandos mágicos* de este entorno de programación literaria. En concreto vamos a utilizar `%%writefile` que guarda los contenidos de una celda como un fichero. 

# %%
get_ipython().run_cell_magic('writefile', '"circuito sencillo.sp"', '* Este es un circuito sencillo\nr1 1 0 100\nv1 0 1 type=vdc vdc=9\n.op\n.dc v1 start=0 stop=9 step=1\n.end')

# %% [markdown]
# Ahora vamos a leer su descripción con Ahkab, interpretar y ejecutar las simulaciones que en él estén descritas.

# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('circuito sencillo.sp')

# %% [markdown]
#  Separamos la información del netlist (componentes) de los análisis (uno de tipo `op` y otro de tipo `dc`):

# %%
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
print(lista_de_análisis)

# %% [markdown]
# > **Pregunta:** ¿qué tipo de estructura de Python es `lista_de_análisis`?
# 
#  lista_de_análisis es un array.
#
#  Las simulaciones que implican listas de datos (`.dc`, `.tran`, etc.) necesitan de un fichero temporal (`outfile`)
#  donde almacenar los resultados. Para ello tenemos que definir la propiedad `outfile`.

# %%
#Comentamos la linea que añade el outfile ya que cambiamos el codigo en la siguiente pregunta.
#lista_de_análisis[1]['outfile'] = "simulación dc.tsv"

# %% [markdown]
#  > **Pregunta:** escribe el código Python necesario para identificar qué análisis de `lista_de_análisis`
#  son de tipo `dc` ó `tran` y sólo añadir la propiedad `outfile` en estos casos.
# Aquí tenéis un post de Stackoverflow con algo de [ayuda](https://stackoverflow.com/questions/49194107/how-to-find-index-of-a-dictionary-key-value-within-a-list-python).
#  Un poco más de ayuda: el siguiente código (sí, una única línea) devuelve el índice de la simulación que es de tipo `dc`. Para simplificar un poco el ejercicio, suponed que, como máximo, habrá un análisis de tipo `tran` y/o `dc`.
# 
# Creamos un bucle que se ejecute tantas veces como registros hay en el array, en caso de que el tipo sea dc o tran le añade el outfile.
for i in range(len(lista_de_análisis)) :
    if lista_de_análisis[i]['type'] == 'dc' or lista_de_análisis[i]['type'] == 'tran' :
        lista_de_análisis[i]['outfile'] = "simulación dc.tsv"

# %% [markdown]
# Una vez que ya hemos separado netlists de simulaciones, ahora ejecutamos las segundas (¡todas a la vez!) gracias al método `.run` de Ahkab: 

# %%º
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# ### Resultados de la simulación `.dc`
# Imprimimos información sobre la simulación de tipo `.dc`:

# %%
print(resultados['dc'])

# %% [markdown]
#  Veamos qué variables podemos dibujar para el caso del análisis `dc`.

# %%
print(resultados['dc'].keys())

# %% [markdown]
# Y ahora graficamos el resultado del análisis anterior. Concretamente vamos a representar el voltaje en el borne 1 (`V1`) con respecto a la intensidad del circuito (`I(V1)`).

# %%
figura = plt.figure()
plt.title("Prueba DC")
plt.xlabel('Voltaje')
plt.ylabel('Intensidad')
plt.plot(resultados['dc']['V1'], resultados['dc']['I(V1)'], label="Voltaje (V1)")


# %% [markdown]
# > **Pregunta:** comenta la gráfica anterior… ¿qué estamos viendo exactamente? Etiqueta los ejes de la misma convenientemente. Así como ningún número puede *viajar* solo sin hacer referencia a su naturaleza, ninguna gráfica puede estar sin sus ejes convenientemente etiquetados. Algo de [ayuda](https://matplotlib.org/3.1.0/gallery/pyplots/fig_axes_labels_simple.html). ¿Qué biblioteca estamos usando para graficar? Una [pista](https://matplotlib.org).
# 
#En la grafica anterior podemos ver como a medida que va subiendo el voltaje la intensidad va aumentando también, se utiliza la libreria matplotlib que esta dentro de PyLab. 
# %% [markdown]
#  ### Resultados de la simulación `.op` 
#  El método `.results` nos devuelve un diccionario con los resultados de la simulación.

# %%
print(resultados['op'].results)

# %% [markdown]
#  > **Pregunta:** justifica el sencillo resultado anterior (análisis `op`). Repite el cálculo con Sympy, atendiendo con mimo a las unidades y al formateo de los resultados (tal y como hemos visto en muchos otros notebooks en clase).
#
# En el ejercicio teniamos una bateria continua 9 V y una resistencia de  100 Ohmios, apicamos la ley de ohm I = V/R y observamos que al igual que en el resultado anterior, obtenemos los 0,09 Amperios.
# %%
v1= 9*u.volts
r_total = 100*u.ohms
intensidad = u.Quantity('i')
intensidad.set_dimension(u.current)
ley_ohm = Eq(v1, intensidad*r_total)
Resultado = solve(ley_ohm, intensidad)
pprint(convert_to(Resultado[0], [u.ampere]).n(2))

# %% [markdown]
#  ## Análisis de circuito con resistencias en serie
# %% [markdown]
# Vamos a resolver (en punto de operación) el siguiente circuito:
# 
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencias%20en%20serie.svg?sanitize=true)
# 
# Al igual que antes, grabamos el netlist en disco desde Jupyter gracias a la *palabra mágica* [`%writefile`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#cellmagic-writefile). 

# %%
get_ipython().run_cell_magic('writefile', '"resistencias en serie.net"', '* circuito con tres resistencias en serie\nv1 1 0 type=vdc vdc=9\nR1 0 2 3k\nR2 2 3 10k\nR3 3 1 5k\n* análisis del circuito\n.op\n.end')


# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en serie.net')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# Imprimos los resultados del análisis `.op`:

# %%
print(resultados['op'])

# %% [markdown]
# Los cantidades `V1`, `V2` y `V3` hacen referencia a los distintos valores del potencial que se ha perdido en cada uno de los bornes que has elegido para describir el netlist (`1`, `2`, etc.). Por ejemplo, podemos calcular el *potencial consumido* por la resistencia `R1` y verás que coincide con el del punto `V2` devuelto por Ahkab. 

# %%
r1 = 3E3*u.ohms
intensidad_ahkab = resultados['op']['I(V1)'][0][0]*u.ampere
v2 = convert_to(intensidad_ahkab*r1, [u.volt])
pprint(v2)

# %% [markdown]
#  > **Pregunta**: reproduce el resto de los valores anteriores de manera *manual* mediante Sympy (es decir, aplicando la ley de Ohm, pero con tun *toque computacional*). Te pongo aquí un ejemplo del que puedes partir… En él sólo calculo la corriente que circula por el circuito (sí, justo la que antes Ahkab ha devuelto de manera automática). Para ello necesito previamente computar la resistencia total (`r_total`). Faltarían el resto de resultados y convertirlos a unidades más *vistosas* (mediante la orden `convert_to` y `.n()`).
#
# Aplicamos Ley de Ohm para hallar la Intensidad.
#%%
v1 = 9*u.volts
r1 = 3*u.kilo*u.ohms
r2 = 10*u.kilo*u.ohms
r3 = 5*u.kilo*u.ohms
r_total = r1 + r2 + r3
intensidad = u.Quantity('i')
intensidad.set_dimension(u.current)
ley_ohm = Eq(v1, intensidad*r_total)
solucion_para_intensidad = solve(ley_ohm, intensidad)
pprint(convert_to(solucion_para_intensidad[0], [u.ampere]).n(2))
intensidad_total=convert_to(solucion_para_intensidad[0], [u.ampere]).n(2)

# %% [markdown]
# Ahora que tenemos la intensidad procedemos a hallar el voltaje para cada resistencia.
# %%
voltaje = u.Quantity('v')
voltaje.set_dimension(u.voltage)
r=r1
ley_ohm_voltaje = Eq(voltaje, intensidad_total*r)
sol_voltaje_r1= solve(ley_ohm_voltaje,voltaje)
pprint(convert_to(sol_voltaje_r1[0], [u.volt]).n(3))
v_r1=convert_to(sol_voltaje_r1[0], [u.volt]).n(3)
r=r2
ley_ohm_voltaje = Eq(voltaje, intensidad_total*r)
sol_voltaje_r2= solve(ley_ohm_voltaje,voltaje)
pprint(convert_to(sol_voltaje_r2[0], [u.volt]).n(3))
v_r2=convert_to(sol_voltaje_r2[0], [u.volt]).n(3)
r=r3
ley_ohm_voltaje = Eq(voltaje, intensidad_total*r)
sol_voltaje_r3= solve(ley_ohm_voltaje,voltaje)
pprint(convert_to(sol_voltaje_r3[0], [u.volt]).n(3))
v_r3=convert_to(sol_voltaje_r3[0], [u.volt]).n(3)
# %% [markdown]
# Ahora podemos realizar lo mismo para hallar las resistencias.
#%%
resistencia = u.Quantity('ohm')

v=v_r1
ley_ohm_resistencia = Eq(v, intensidad_total*resistencia)
sol_voltaje_r1= solve(ley_ohm_resistencia,resistencia)
pprint(convert_to(sol_voltaje_r1[0], [u.ohm]).n(1))

v=v_r2
ley_ohm_resistencia = Eq(v, intensidad_total*resistencia)
sol_voltaje_r1= solve(ley_ohm_resistencia,resistencia)
pprint(convert_to(sol_voltaje_r1[0], [u.ohm]).n(1))

v=v_r3
ley_ohm_resistencia = Eq(v, intensidad_total*resistencia)
sol_voltaje_r1= solve(ley_ohm_resistencia,resistencia)
pprint(convert_to(sol_voltaje_r1[0], [u.ohm]).n(1))



# %% [markdown]
# > **Pregunta**: Demuestra que se cumple la Ley de Kirchhoff de la energía en un circuito, es decir, que la suma de la energía suministrada por las fuentes (pilas) es igual a la consumida por las resistencias. Realiza la operación con Sympy.
# 
# $$
# \sum_i^N V_{\text{fuentes}} = \sum_j^M V_{\text{consumido en resistencias}}
# $$
# 
# Ten en cuenta que en este caso sólo hay una fuente.
# %%
v1= 9*u.volts
r1=3*u.kilo*u.ohms
r2=10*u.kilo*u.ohms
r3=5*u.kilo*u.ohms
# %% [markdown]
# sumamos las resistencias, ya que en un circuito en serie la resistencia total es igual a la suma de todas las resistencias.
# %%
r_total= r1+r2+r3
print(r_total) 
intensidad = u.Quantity('i')
intensidad.set_dimension(u.current)
ley_ohm_intensidad = Eq(v1, intensidad*r_total)
Intensidad_T = solve(ley_ohm_intensidad, intensidad)
# %% [markdown]
# Tras hallar la resistencia total, aplicamos ley de ohm para obtener la intensidad.
# %%
intensidad_total=convert_to(Intensidad_T[0], [u.ampere]).n(2)
print(intensidad_total)
# %% [markdown]
# una vez hallada la intensidad podemos aplicar la ley de ohm para obtener el voltaje.
# %%
voltaje = u.Quantity('v')
voltaje.set_dimension(u.voltage)
ley_ohm_resistencia = Eq(voltaje, intensidad_total*r_total)
voltaje_total= solve(ley_ohm_resistencia,voltaje)
# %% [markdown]
# Como podemos observar el voltaje consumido por la resistencia total, es el mismo que el de la pila. 
# %%
pprint(convert_to(voltaje_total[0], [u.volt]).n(3))

# %% [markdown]
# ## Análisis `.op` de circuitos con resistencias en paralelo
# 
# Vamos a complicar un poco el trabajo añadiendo elementos en paralelo.
# 
#  > **Pregunta**: realiza los análisis `.op` de los siguientes circuitos.
#  Para ello crea un netlist separado para cada uno donde queden correctamente descritos
#  junto con la simulación (`.op`). Comenta los resultados que devuelve Ahkab (no imprimas los resultados de las simulaciones *sin más*).
# 
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/resistencias%20en%20paralelo.svg?sanitize=true)
# 
#  Aquí tienes el análisis del primer circuito, para que sirva de ejemplo:

# %%
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 1.cir"', '* resistencias en paralelo\nvdd 0 1 vdc=12 type=vdc\nr2 1 2 1k\nr3 2 3 220\nr4 3 0 1.5k\nr5 2 0 470\n.op\n.end')

# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en paralelo 1.cir')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)

# %% [markdown]
# Imprimimos los resultados del análisis `.op`. Como puedes comprobar, Ahkab sólo reporta la intensidad de corriente en las ramas en las que hay una pila (en este caso, la rama donde está la pila `VDD`).

# %%
print(resultados['op'])
#%%
#%% [markdown]
#Circuito 2
# creamos una netlist para el circuito 2, donde tiene un total de 5 resistencias y 2 pilas.
# en el .op podemos observar la inmtenccidad total y la intencidad que pasa por el cable que tiene la otra pila de 1.5 V
#%%
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 2.cir"', '* resistencias en paralelo\nvdd1 0 1 vdc=9 type=vdc\nvdd2 5 0 vdc=1.5 type=vdc\nr2 1 2 47\nr3 2 3 220\nr4 3 4 1k\nr5 4 0 560\nr6 2 5 180\n.op\n.end')
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en paralelo 2.cir')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])


#%% [markdown]
#Circuito 3
# creamos una netlist para el circuito 3, donde hay 3 resistencias en paralelo y 3 pilas de 0 V donde su función seria como un cable, pero de esta manera podemos medir la intencidad que pasa por cada uno de los cables.
# en el .op podemos observar la intenccidad total y la intencidad que hay por los 3 cables en paralelo.
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 3.cir"','* resistencias en paralelo\nvdd1 0 1 vdc=9 type=vdc\nvdd2 1 2 vdc=0 type=vdc\nvdd3 1 3 vdc=0 type=vdc\nvdd4 1 4 vdc=0 type=vdc\nr2 2 0 10k\nr3 3 0 2k\nr4 4 0 1k\n.op\n.end')
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en paralelo 3.cir')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])
# %% [markdown]
# Como podemos comprobar, en el tercer circuito, se cumple la ley de kirchhoff, donde la suma de la intencidad de las resistencias es igual a la intencidad total.
#%%
print(resultados['op']['I(VDD2)'] + resultados['op']['I(VDD3)']+ resultados['op']['I(VDD4)'])
print(resultados['op']['I(VDD1)'])



# %% [markdown]
# > **Pregunta:** inserta dos *pilas virtuales* de 0 voltios en el resto de ramas del circuito (`Vdummy1` en la rama donde está `R5` y `Vdummy2` en la rama donde está `R3` y `R4`) para que Ahkab nos imprima también la corriente en las mismas. Es muy parecido al tercer circuito que tienes que resolver, donde `V1`, `V2` y `V3` tienen cero voltios. Estas *pilas nulas* son, a todos los efectos, *simples cables*. Una vez que ya tienes las corrientes en todas las ramas, comprueba que se cumple la Ley de Kirchhoff para las corrientes:
#
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 1.cir"', '* resistencias en paralelo\nvdd 0 1 vdc=12 type=vdc\nVdummy1 4 0 vdc=0 type=vdc\nVdummy2 5 0 vdc=0 type=vdc\nr2 1 2 1k\nr3 2 3 220\nr4 3 5 1.5k\nr5 2 4 470\n.op\n.end')
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en paralelo 1.cir')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])
# %% [markdown]
# Como podemos comprobar, en el primero circuito, se cumple la ley de kirchhoff, donde la suma de la intencidad de las resistencias es igual a la intencidad total.
#%%
print(resultados['op']['I(Vdummy1)'] + resultados['op']['I(Vdummy2)'])
print(resultados['op']['I(VDD)'])

#%%
get_ipython().run_cell_magic('writefile', '"resistencias en paralelo 2.cir"', '* resistencias en paralelo\nvdd1 0 1 vdc=9 type=vdc\nvdd2 5 6 vdc=1.5 type=vdc\nVdummy1 6 0 vdc=0 type=vdc\nVdummy2 7 0 vdc=0 type=vdc\nr2 1 2 47\nr3 2 3 220\nr4 3 4 1k\nr5 4 7 560\nr6 2 5 180\n.op\n.end')
circuito_y_análisis = ahkab.netlist_parser.parse_circuit('resistencias en paralelo 2.cir')
circuito = circuito_y_análisis[0]       
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])
# %% [markdown]
# Como podemos comprobar, en el segundo circuito, se cumple la ley de kirchhoff, donde la suma de la intencidad de las resistencias es igual a la intencidad total.
#%%
print((resultados['op']['I(Vdummy1)'] + resultados['op']['I(Vdummy2)']) * u.ampere)
print(resultados['op']['I(VDD1)']* u.ampere)
#%%
# 
# $$
# I_{\text{entrante}} = \sum_i^{N} I_{\text{salientes}}
# $$
# 
# Repite lo mismo para los otros dos circuitos. Realiza además los cálculos con Sympy (recalcula los mismos voltajes que devuelve Ahkab a partir de la corriente que sí te devuelve la simulación) y cuidando de no olvidar las unidades. Recuerda que el objeto `resultados` alberga toda la información que necesitas de manera indexada. Ya han aparecido un ejemplo más arriba. Es decir: no *copies* los números *a mano*, trabaja de manera informáticamente elegante (usando la variable `resultados`). 
# %% [markdown]
#  # Circuitos en DC que evolucionan con el tiempo
# %% [markdown]
#  ## Carga de un condensador
#  Vamos a ver qué le pasa a un circuito de corriente continua cuando tiene un condensador
#  en serie.
# 
#  ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensador%20en%20continua.svg?sanitize=true)
# 
#  Al igual que antes, primero guardamos el circuito en un netlist externo:

# %%
get_ipython().run_cell_magic('writefile', '"condensador en continua.ckt"', '* Carga condensador\nv1 0 1 type=vdc vdc=6\nr1 1 2 1k\nc1 2 0 1m ic=0\n.op\n.tran tstep=0.1 tstop=8 uic=0\n.end')

# %% [markdown]
# > **Pregunta:** ¿qué significa el parámetro `ic=0`? ¿qué perseguimos con un análisis de tipo `.tran`?
# 
# Ic= 0 Significa que la carga inicial del condensador es 0 y con un analisis de tipo .tran (Transitorio) podemos analizar los parametros del circuito en distintos tramos temporales.
#
# Leamos el circuito:

# %%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit("condensador en continua.ckt")

# %% [markdown]
#  Separamos el netlist de los análisis y asignamos un fichero de almacenamiento de datos (`outfile`):

# %%
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
lista_de_análisis[1]['outfile'] = "simulación tran.tsv"

# %% [markdown]
#  Ejecutamos la simulación:

# %%
resultados = ahkab.run(circuito, lista_de_análisis)
print(resultados['op'])
#print(resultados['tran'].keys())

# %% [markdown]
#  Dibujamos la gráfica de carga del condensador con el tiempo, centrándonos en la intensidad que circula por la pila. 

# %%
figura = plt.figure()
plt.title("Carga de un condensador")
plt.xlabel('Tramo')
plt.ylabel('Intensidad')
plt.plot(resultados['tran']['T'], resultados['tran']['I(V1)'], label="Una etiqueta")



# %% [markdown]
# > **Pregunta:** Etiqueta los ejes convenientemente y comenta la gráfica. Dibuja otra gráfica con el voltaje en el borne `V1`. ¿Por qué son *opuestas*? ¿Qué le ocurre al voltaje a medida que evoluciona el circuito en el tiempo? Dibuja las gráficas en un formato estándar de representación vectorial (SVG, por ejemplo). Algo de ayuda [aquí](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.set_matplotlib_formats). ¿Qué valores devuelve el análisis de tipo `.op`? Justifícalo.
#
# Los condensadores en corriente continua se comportan como un circuito abierto, de tal manera que cuando se llegan a cargar impiden el paso de la corriente porque no pueden descargarse.
# Al principio si que se deja pasar corriente en el periodo denomindo transitorio hasta que se estabiliza.
# El analisis de tipo OP nos dice que la corriente del circuito es 0, por lo explicado anteriormente ya que el condensador en corriente continua se comporta como un cirrcuito abierto impidiendo el paso de la corriente.
#Como podemos observar en el siguiente grafico, el proceso de carga en un condensador al contrario que la corriente empieza desde los 0 voltios y se va cargando hasta llegar a los X voltios (Donde X es el voltaje de la fuente)
#%%
figura = plt.figure()
plt.title("Carga de un condensador")
plt.xlabel('Tramo')
plt.ylabel('Voltaje')
plt.plot(resultados['tran']['T'], resultados['tran']['v2'], label="Voltaje")



# %% [markdown]
# ## Carrera de condensadores
# 
# Ahora tenemos un circuito con dos condensadores en paralelo: 
# 
# ![](https://raw.githubusercontent.com/pammacdotnet/spicelab/master/condensadores%20en%20paralelo.svg?sanitize=true)
# 
# > **Pregunta:** Crea el netlist de este circuito e identifica qué condensador se satura primero. Dibuja la evolución de la intensidad en ambas ramas de manera simultánea. [Aquí](https://matplotlib.org/gallery/api/two_scales.html) tienes un ejemplo de cómo se hace esto en Matplotlib. Recuerda que para que Ahkab nos devuelva la corriente en una rama, debe de estar presente una pila. Si es necesario, inserta pilas virtuales de valor nulo (cero voltios), tal y como hemos comentado antes. Grafica también los voltajes (en otra gráfica, pero que aparezcan juntos). 
get_ipython().run_cell_magic('writefile', '"2 condensadores en continua.ckt"', '* Carga condensador\nv1 0 1 type=vdc vdc=10\nvdummy1 2 4 type=vdc vdc=0\nvdummy2 3 4 type=vdc vdc=0\nc1 1 2 47u ic=0\nc2 1 3 22u ic=0\nr1 4 0 3.3k\n.op\n.tran tstep=0.1 tstop=8 uic=0\n.end')
#%%
circuito_y_análisis = ahkab.netlist_parser.parse_circuit("2 condensadores en continua.ckt")
circuito = circuito_y_análisis[0]
análisis_en_netlist = circuito_y_análisis[1]
lista_de_análisis = ahkab.netlist_parser.parse_analysis(circuito, análisis_en_netlist)
lista_de_análisis[1]['outfile'] = "simulación tran.tsv"
resultados = ahkab.run(circuito, lista_de_análisis)
#%%
print(resultados['op'])

# %% [markdown]
# Como podemos observar se satura primero el que menos capacidad tiene.
#%%
figura = plt.figure()
plt.title("Carga de un condensador")
plt.xlabel('Tramo')
plt.ylabel('Intensidad')

plt.plot(resultados['tran']['T'], resultados['tran']['I(VDUMMY1)'], label="Intensidad vdummy1")
plt.plot(resultados['tran']['T'], resultados['tran']['I(VDUMMY2)'], label="Intensidad vdummy2")# %%
figura = plt.figure()
plt.title("Voltaje Condensador")
plt.xlabel('Tramo')
plt.ylabel('Voltaje')
plt.plot(resultados['tran']['T'], resultados['tran']['v2'], label="Voltaje (V2)")
plt.plot(resultados['tran']['T'], resultados['tran']['v3'], label="Voltaje (V3)")



# %%
