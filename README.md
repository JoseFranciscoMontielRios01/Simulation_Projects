# Simulation_Projects
​El Generador Congruencial Lineal Mixto es un algoritmo clásico utilizado para generar secuencias de números pseudoaleatorios. Su funcionamiento se basa en la siguiente relación de recurrencia:​
Wikipedia, la enciclopedia libre
+2
LEARN STATISTICS EASILY
+2
Barcelona Geeks
+2

𝑋
𝑛
+
1
=
(
𝑎
⋅
𝑋
𝑛
+
𝑐
)
m
o
d
 
 
𝑚
X 
n+1
​
 =(a⋅X 
n
​
 +c)modm​
LEARN STATISTICS EASILY

Donde:

𝑋
𝑛
X 
n
​
  es el número pseudoaleatorio actual.​
LEARN STATISTICS EASILY
+1
Barcelona Geeks
+1

𝑎
a es el multiplicador.​

𝑐
c es el incremento.​
LEARN STATISTICS EASILY
+2
Barcelona Geeks
+2
Wikipedia, la enciclopedia libre
+2

𝑚
m es el módulo.​

𝑋
𝑛
+
1
X 
n+1
​
  es el siguiente número pseudoaleatorio generado.​

Para garantizar que el generador tenga un período completo, es esencial que los parámetros 
𝑎
a, 
𝑐
c y 
𝑚
m cumplan con ciertas condiciones, conocidas como el Teorema de Hull-Dobell:​
Wikipedia, la enciclopedia libre

𝑐
c y 
𝑚
m deben ser primos relativos, es decir, su máximo común divisor debe ser 1.​
Wikipedia, la enciclopedia libre

𝑎
−
1
a−1 debe ser divisible por todos los factores primos de 
𝑚
m.​

Si 
𝑚
m es múltiplo de 4, entonces 
𝑎
−
1
a−1 también debe serlo.​
Wikipedia, la enciclopedia libre

En el código Java proporcionado, se implementa un Generador Congruencial Lineal Mixto con parámetros específicos:​

Semilla (
𝑋
0
X 
0
​
 ): 1​

Multiplicador (
𝑎
a): 21​
Barcelona Geeks
+2
LEARN STATISTICS EASILY
+2
Wikipedia, la enciclopedia libre
+2

Incremento (
𝑐
c): 13​

Módulo (
𝑚
m): 50​

Estos valores han sido seleccionados para cumplir con las condiciones mencionadas anteriormente, asegurando así un período completo en la generación de números pseudoaleatorios.​
Barcelona Geeks

El programa solicita al usuario la cantidad de números pseudoaleatorios que desea generar y luego produce una secuencia que incluye, para cada iteración:​

El número de iteración.​

El valor actual 
𝑋
𝑛
X 
n
​
 .​

El siguiente valor 
𝑋
𝑛
+
1
X 
n+1
​
 .​

El número uniforme correspondiente, calculado como 
𝑋
𝑛
+
1
/
𝑚
X 
n+1
​
 /m.​

Además, el programa verifica y muestra si los parámetros elegidos cumplen con las condiciones necesarias para garantizar un período completo. Al final, calcula y presenta estadísticas básicas, como el promedio de los números uniformes generados.​

Esta implementación es útil para comprender el funcionamiento de los generadores congruenciales lineales mixtos y para aplicaciones que requieren secuencias de números pseudoaleatorios con buenas propiedades estadísticas
