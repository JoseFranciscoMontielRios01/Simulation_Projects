# Simulation_Projects
Te explicaré detalladamente el funcionamiento del código:
Declaración de Variables y Valores Iniciales:
Apply to GeneradorCon...
Estas son las constantes que definen el generador congruencial mixto
Cada una tiene un propósito específico en la fórmula: Xn+1 = (a * Xn + c) mod m
Presentación de Información:
Apply to GeneradorCon...
Muestra el título y la fórmula matemática del generador
Explica cada componente de la fórmula (Xn+1, Xn, a, c, m)
Verificación de Condiciones:
Apply to GeneradorCon...
Verifica que el generador cumpla con todas las condiciones necesarias:
La semilla (Xo) debe ser positiva
El multiplicador (a) debe ser impar, no divisible por 3 ni 5, y (a-1) mod 4 = 0
El incremento (c) debe ser impar y primo relativo con m
El módulo (m) debe ser mayor que Xo, a y c
a-1 debe ser divisible por todos los factores primos de m
Generación de Números Pseudoaleatorios:
Apply to GeneradorCon...
Solicita al usuario cuántos números desea generar
Usa un Scanner para leer la entrada del usuario
Cálculo y Visualización de Números:
Apply to GeneradorCon...
Para cada iteración:
Calcula el siguiente número usando la fórmula: Xn+1 = (a * Xn + c) mod m
Convierte el número a uniforme dividiendo por m
Muestra:
Número de iteración
Estado actual (Xn)
Siguiente estado (Xn+1)
Número uniforme (entre 0 y 1)
Cálculo de Estadísticas:
Apply to GeneradorCon...
Calcula el promedio de los números uniformes generados
Vuelve a generar la secuencia para no perder los valores originales
Presentación de Resultados:
Apply to GeneradorCon...
Muestra un resumen con:
Cantidad total de números generados
Promedio de los números uniformes
Este generador es especialmente útil porque:
Tiene período completo (m-1 = 49 iteraciones)
Cumple con todas las condiciones necesarias para ser un buen generador
Produce números pseudoaleatorios uniformemente distribuidos
Permite generar cualquier cantidad de números que el usuario desee
Proporciona información detallada sobre el proceso y las estadísticas
