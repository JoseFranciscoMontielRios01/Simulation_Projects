# Generador Congruencial Lineal Mixto (GCLM)
El funcionamiento detallado del código que has proporcionado es el siguiente:

### 1. Declaración de Variables y Valores Iniciales:
En esta sección, se definen las constantes necesarias para el generador congruencial lineal mixto. Cada una de estas constantes tiene un propósito específico dentro de la fórmula matemática que define el generador:

Xn+1 = (a * Xn + c) mod m

- Xo: La semilla inicial (valor de arranque).
- a: El multiplicador, que debe cumplir con varias condiciones para asegurar un ciclo completo.
- c: El incremento que se suma al producto de a * Xn.
- m: El módulo, que define el rango de los números generados.

### 2. Presentación de Información:
Una vez definidas las constantes, el código imprime la fórmula que se utilizará para generar los números pseudoaleatorios. También explica el significado de cada componente en la fórmula (Xn+1, Xn, a, c, m).

### 3. Verificación de Condiciones:
Antes de proceder con la generación de números, el programa verifica que las condiciones necesarias para que el generador tenga un periodo completo sean cumplidas. Estas son:

1. Xo > 0: La semilla debe ser positiva.
2. a > 0: El multiplicador debe ser mayor que cero, y debe cumplir las siguientes condiciones adicionales:
   - a debe ser impar.
   - a no debe ser divisible por 3 ni 5.
   - (a - 1) mod 4 = 0.
3. c > 0: El incremento debe ser positivo.
4. c debe ser impar y primo relativo con m: El valor de c debe ser relativamente primo a m, lo que significa que su máximo común divisor (MCD) con m debe ser 1.
5. m > X₀, a, c: El módulo debe ser mayor que la semilla, el multiplicador y el incremento.
6. (a - 1) debe ser divisible por todos los factores primos de m: Esta condición asegura que la secuencia generada tenga un periodo completo.

### 4. Generación de Números Pseudoaleatorios:
Una vez que se ha verificado que todas las condiciones son correctas, el programa solicita al usuario cuántos números pseudoaleatorios desea generar. Luego, el programa calcula y muestra los números en una tabla con la siguiente información:

- Número de iteración: La posición del número en la secuencia.
- Estado actual (Xn): El valor de la semilla o número actual en la secuencia.
- Siguiente estado (Xn+1): El número generado en la iteración siguiente.
- Número uniforme: El número generado, normalizado en el rango [0, 1], obtenido dividiendo Xn+1 por m.

### 5. Cálculo de Estadísticas:
El programa también realiza un cálculo adicional para obtener el promedio de los números uniformes generados. Para hacer esto, vuelve a generar la secuencia de números sin perder los valores originales y suma todos los valores generados, para finalmente obtener el promedio.

### 6. Presentación de Resultados:
Finalmente, el programa imprime un resumen con las siguientes estadísticas:

- Cantidad total de números generados: La cantidad de números pseudoaleatorios que el usuario ha solicitado.
- Promedio de los números uniformes: El promedio de todos los números generados, que proporciona una medida de su distribución.

Este generador es especialmente efectivo cuando se necesita una secuencia de números pseudoaleatorios con un buen comportamiento estadístico y un periodo completo.
