# Importar la lista de tipos para anotaciones de variables, mejorando la legibilidad y el control de tipos.
from typing import List, Tuple # Importar List para indicar que una variable es una lista y Tuple para indicar que una variable es una tupla, específicamente para definir la estructura de los elementos en la lista de diferencias como tuplas de números de punto flotante.
# Importar la librería numpy, que es fundamental para realizar operaciones numéricas eficientes, como el cálculo de la raíz cuadrada utilizada para determinar el valor crítico.
import numpy as np
# Importar el módulo ksone de scipy.stats. Aunque inicialmente comentado para indicar que no se usó una función específica de Scipy para el valor crítico en el enfoque de Coss Bu descrito, la línea de importación se mantiene aquí si se deseara usar funciones de distribución de KS más avanzadas en el futuro.
from scipy.stats import ksone
# Importamos uniform de scipy.stats para trabajar con la distribución uniforme continua.
from scipy.stats import uniform
# Importamos kstest para realizar la prueba de Kolmogorov-Smirnov.
from scipy.stats import kstest
# Importamos herramientas para definir los tipos de datos que usaremos.
from typing import Dict, Union

class GCM:
    def __init__(self, m: int, X0: int, a: int):
        # Inicializa el generador congruencial multiplicativo con los parámetros dados.
        self.m = m
        self.X0 = X0
        self.a = a
        self.Xn = X0
        self.numeros_generados = set()
        
    def generar_numero(self) -> float:
        # Genera un número pseudoaleatorio usando el método congruencial multiplicativo.
        self.Xn = (self.a * self.Xn) % self.m
        return self.Xn / self.m
        
    def generar_hasta_periodo(self) -> List[float]:
        # Genera números hasta que se complete el período del GCM.
        numeros = []
        self.Xn = self.X0  # Reiniciamos el generador
        self.numeros_generados = set()
        
        while True:
            numero = self.generar_numero()
            if numero in self.numeros_generados:
                break
            numeros.append(numero)
            self.numeros_generados.add(numero)
            
        return numeros

# Definición de la clase llamada PruebaKolmogorovSmirnov. Esta clase agrupa todos los datos y métodos necesarios para realizar la prueba de Kolmogorov-Smirnov en un conjunto de números pseudoaleatorios.
class PruebaKolmogorovSmirnov:
    # Implementa la Prueba de Kolmogorov-Smirnov para validar números pseudoaleatorios.
    # Esta prueba estadística evalúa si un conjunto de números proviene de una distribución específica, en este caso, la uniforme continua entre 0 y 1.
    # Compara la distribución de probabilidad acumulada empírica (basada en los datos) con la distribución de probabilidad acumulada teórica (la uniforme).
    # La prueba se basa en el siguiente proceso:
    # 1. Se ordenan los números pseudoaleatorios de menor a mayor.
    # 2. Se calcula la diferencia máxima entre la distribución acumulada empírica (Fn(xᵢ)) y la teórica (F(xᵢ)).
    # 3. Se obtiene el valor crítico Dα usando tablas o funciones estadísticas.
    # 4. Se compara la diferencia máxima (D) con el valor crítico (Dα).
    # 5. Se toma la decisión estadística basada en esta comparación.
    
    # Este es el método especial constructor de la clase. Se ejecuta automáticamente cuando se crea una nueva instancia (objeto) de PruebaKolmogorovSmirnov.
    def __init__(self, numeros: List[float], alpha: float = 0.05):
        # Inicializa la prueba con los números a analizar y el nivel de significancia.
        # Args:
        #   numeros (List[float]): Lista de números pseudoaleatorios a probar.
        #   alpha (float): Nivel de significancia para la prueba (usualmente 0.05).
        
        # Guardamos la lista de números en un array de numpy para facilitar las operaciones matemáticas.
        self.numeros = np.array(numeros)
        # Guardamos el nivel de significancia que usaremos para la decisión.
        self.alpha = alpha
        # Obtenemos el tamaño de la muestra (cuántos números tenemos).
        self.N = len(numeros)
        
        # Validamos que los datos de entrada sean correctos antes de proceder.
        self._validar_entradas()
        
    def _validar_entradas(self) -> None:
        # Verifica que los parámetros cumplan con los requisitos necesarios para la prueba.
        # Raises:
        #   ValueError: Si el nivel de significancia no está entre 0 y 1.
        #   ValueError: Si la lista de números está vacía.
        #   ValueError: Si algún número está fuera del intervalo [0,1].
        
        # Comprobamos que el nivel de significancia sea válido.
        if not (0 < self.alpha < 1):
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1.")
            
        # Comprobamos que la lista de números no esté vacía.
        if self.N == 0:
            raise ValueError("La lista de números no puede estar vacía.")
            
        # Comprobamos que todos los números estén en el rango esperado [0, 1].
        if any(not (0.0 <= num <= 1.0) for num in self.numeros):
            raise ValueError("Todos los números deben estar en el intervalo [0.0, 1.0].")
            
    def ejecutar_prueba(self) -> Dict[str, Union[float, str, np.ndarray]]:
        # Ejecuta la prueba de Kolmogorov-Smirnov completa y devuelve los resultados.
        # Este método coordina todos los pasos de la prueba.
        # Returns:
        #   Dict: Diccionario que contiene todos los resultados de la prueba.
        
        # Ordenamos los números de menor a mayor, lo cual es necesario para calcular la distribución empírica.
        numeros_ordenados = np.sort(self.numeros)
        
        # Calculamos el estadístico D manualmente para el reporte detallado.
        diferencias = []
        for i, xi in enumerate(numeros_ordenados):
            fn_xi = (i + 1) / self.N
            f_xi = xi
            diferencia = abs(fn_xi - f_xi)
            diferencias.append(diferencia)
        d_estadistico = max(diferencias)
        
        # Calculamos el valor crítico usando la fórmula de Coss Bu para α=0.05.
        d_critico = 1.36 / np.sqrt(self.N)
        
        # Calculamos el p-value usando kstest para la decisión.
        _, p_value = kstest(numeros_ordenados, 'uniform')
        
        # La decisión se basa en el p-value.
        if p_value < self.alpha:
            decision = "Se rechaza H₀: Los números no provienen de una distribución uniforme (0,1)."
        else:
            decision = "No se rechaza H₀: Los números provienen de una distribución uniforme (0,1)."
            
        # Devolvemos un diccionario con todos los resultados importantes de la prueba.
        return {
            "tamaño_muestra": self.N,
            "nivel_significancia": self.alpha,
            "numeros_ordenados": numeros_ordenados,
            "d_estadistico": d_estadistico,
            "p_value": p_value,
            "d_critico": d_critico,
            "decision": decision
        }

    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba de Kolmogorov-Smirnov.
        # El reporte incluye hipótesis, parámetros, tabla de comparación Fn(xi) vs F(xi), estadístico, valor crítico y decisión.
        # Returns:
        #   str: El reporte formateado listo para imprimir.
        
        # Ejecutamos la prueba para obtener todos los resultados necesarios para el reporte.
        resultados = self.ejecutar_prueba()
        
        # Extraemos los resultados del diccionario para usarlos en el reporte.
        N = resultados["tamaño_muestra"]
        alpha = resultados["nivel_significancia"]
        numeros_ordenados = resultados["numeros_ordenados"]
        d_estadistico = resultados["d_estadistico"]
        p_value = resultados["p_value"]
        d_critico = resultados["d_critico"]
        decision = resultados["decision"]
        
        reporte = "\n" + "="*80
        reporte += "\nPRUEBA DE KOLMOGOROV-SMIRNOV - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "="*80
        
        # Agregamos las hipótesis de la prueba.
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\nHipótesis nula    (H₀) : Los números provienen de una distribución uniforme (0,1)."
        reporte += "\nHipótesis altern. (H₁) : Los números no provienen de una distribución uniforme (0,1)."
        
        # Agregamos los parámetros de la prueba.
        reporte += "\n\nPARÁMETROS DE LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {N}"
        reporte += f"\n- Nivel de significancia (α) : {alpha}"
        
        # Preparamos la tabla de comparación de distribuciones.
        reporte += "\n\nCOMPARACIÓN DE DISTRIBUCIONES ACUMULADAS:"
        reporte += "\n" + "-"*70
        reporte += f"\n{'i':<5} {'x(i)':<10} {'F(x(i))':<15} {'Fn(x(i))':<15} {'|Fn(x(i)) - F(x(i))|':<20}"
        reporte += "\n" + "-"*70
        
        # Calculamos los valores para cada fila de la tabla.
        for i, xi in enumerate(numeros_ordenados):
            # i+1 es la posición del número en la lista ordenada (1-based index).
            # Fn(xi) es la frecuencia acumulada observada, es decir, la proporción de números menores o iguales a xi.
            fn_xi = (i + 1) / N
            # F(xi) es la frecuencia acumulada teórica para una distribución uniforme (0,1), que es simplemente xi.
            f_xi = xi
            # Calculamos la diferencia absoluta entre la distribución empírica y teórica.
            diferencia = abs(fn_xi - f_xi)
            
            # Agregamos la fila a la tabla en el reporte.
            reporte += f"\n{i+1:<5} {xi:<10.5f} {f_xi:<15.5f} {fn_xi:<15.5f} {diferencia:<20.5f}"
        
        reporte += "\n" + "-"*70
        
        # Mostramos el cálculo del estadístico D.
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO D:"
        reporte += "\nD = max |Fn(xᵢ) - F(xᵢ)|"
        reporte += f"\nD = {d_estadistico:.5f}"
        
        # --- Inicio de la sección para explicar el cálculo del valor crítico ---
        # Calculamos el valor crítico Dα usando la fórmula 1.36 / sqrt(N) para un nivel de significancia del 0.05.
        # Esta fórmula es una aproximación comúnmente usada para la distribución de Kolmogorov-Smirnov para muestras grandes (N > 35) cuando α = 0.05.
        if N > 0:
            valor_critico_cos = 1.36 / np.sqrt(N)
            reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
            reporte += "\nEl valor crítico (Dα) para  el nivel de significancia \u03b1 = 0.05 y para N grande se puede aproximar con la fórmula:"
            reporte += "\nD\u03b1 \u2248 1.36 / \u221aN"
            reporte += f"\nD\u03b1 \u2248 1.36 / \u221a{N} = 1.36 / {np.sqrt(N):.5f} = {valor_critico_cos:.5f}"
        else:
            valor_critico_cos = float('inf') # Evitar división por cero, aunque la validación previa debería prevenir esto.
            reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
            reporte += "\nNo se puede calcular el valor crítico con N=0."
        
        # --- Inicio de la sección modificada para mostrar la comparación con 1.36/sqrt(N) con formato similar a PruebaSeries ---
        reporte += "\n\nDECISIÓN:"
        
        # Comparamos el estadístico D calculado con el valor crítico de Coss Bu y mostramos el resultado detallado.
        if d_estadistico <= valor_critico_cos:
            # Si D es menor o igual al valor crítico, no rechazamos H₀.
            reporte += f"\nComo D = {d_estadistico:.5f} \u2264 {valor_critico_cos:.5f} (Coss Bu para \u03b1={alpha}, \u221an={np.sqrt(N):.5f})"
            reporte += "\nNo se rechaza H₀: Los números provienen de una distribución uniforme (0,1)."
        else:
            # Si D es mayor que el valor crítico, rechazamos H₀.
            reporte += f"\nComo D = {d_estadistico:.5f} > {valor_critico_cos:.5f} (Coss Bu para \u03b1={alpha}, \u221an={np.sqrt(N):.5f})"
            reporte += "\nSe rechaza H₀: Los números no provienen de una distribución uniforme (0,1)."
            
        # --- Fin de la sección modificada ---
        
        # Agregamos una línea decorativa al final.
        reporte += "\n" + "="*80
        return reporte

# Este bloque de código se ejecuta solo cuando el script PruebaKolmogorovSmirnov.py se corre directamente como un programa principal (no cuando es importado como un módulo en otro script).
if __name__ == "__main__":
    # Comentario que indica el propósito de este bloque principal: demostrar el uso de la clase PruebaKolmogorovSmirnov.
    # Ejemplo de uso de la clase PruebaKolmogorovSmirnov.
    # Parámetros del GCM para generar números pseudoaleatorios.
    parametros = [
        {"m": 32057, "X0": 20855, "a": 9600}
    ]
    
    # Aplicar la prueba a cada conjunto de parámetros.
    for params in parametros:
        print(f"\nProbando con m={params['m']}, X0={params['X0']}, a={params['a']}")
        print("="*80)
        
        # Generar números pseudoaleatorios usando el GCM hasta el período.
        gcm = GCM(params['m'], params['X0'], params['a'])
        numeros = gcm.generar_hasta_periodo()
        
        # Crear y ejecutar la prueba de Kolmogorov-Smirnov.
        prueba = PruebaKolmogorovSmirnov(numeros=numeros, alpha=0.05)
        print(prueba.generar_reporte())
