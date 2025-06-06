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

# Lista de 400 números pseudoaleatorios uniformes entre 0 y 1.
numeros = [
    0.03911, 0.38555, 0.17546, 0.32643, 0.69572, 0.24122, 0.61196, 0.30532, 0.03788, 0.48228,
    0.88618, 0.71299, 0.27954, 0.80863, 0.33564, 0.90899, 0.78038, 0.55986, 0.87539, 0.16818,
    0.34677, 0.45305, 0.59747, 0.1652, 0.68652, 0.79375, 0.33521, 0.59589, 0.20554, 0.59404,
    0.42614, 0.34994, 0.99385, 0.66497, 0.48509, 0.1547, 0.20094, 0.73788, 0.6053, 0.44372,
    0.10461, 0.95554, 0.73704, 0.52861, 0.68777, 0.66591, 0.30231, 0.21704, 0.97599, 0.63379,
    0.19161, 0.23853, 0.58909, 0.00514, 0.6078, 0.75754, 0.70267, 0.66485, 0.08823, 0.60311,
    0.583, 0.07521, 0.67277, 0.69676, 0.27376, 0.9522, 0.36665, 0.49067, 0.92409, 0.72059,
    0.29297, 0.41374, 0.416, 0.68646, 0.23929, 0.48355, 0.98977, 0.06533, 0.45128, 0.15486,
    0.93716, 0.32886, 0.92052, 0.95819, 0.3951, 0.27699, 0.92962, 0.10274, 0.75867, 0.85783,
    0.4129, 0.0587, 0.82444, 0.20247, 0.4846, 0.60833, 0.43529, 0.88722, 0.94813, 0.74457,
    0.7491, 0.61318, 0.76503, 0.11654, 0.92852, 0.01159, 0.55823, 0.66821, 0.96277, 0.43947,
    0.01918, 0.70071, 0.11133, 0.78138, 0.27482, 0.88651, 0.74843, 0.28597, 0.74022, 0.65741,
    0.16894, 0.5978, 0.46215, 0.06831, 0.35905, 0.06494, 0.61773, 0.12202, 0.20717, 0.47619,
    0.67312, 0.01119, 0.99005, 0.81759, 0.85558, 0.25983, 0.96318, 0.56736, 0.319, 0.90561,
    0.64345, 0.31855, 0.34513, 0.99893, 0.55866, 0.63267, 0.47641, 0.41575, 0.48257, 0.5108,
    0.28316, 0.14736, 0.07586, 0.66559, 0.45476, 0.22596, 0.93413, 0.20405, 0.84617, 0.14014,
    0.98953, 0.09958, 0.15917, 0.1964, 0.85244, 0.03152, 0.22109, 0.94205, 0.82037, 0.87481,
    0.71857, 0.92784, 0.04921, 0.45197, 0.15191, 0.01291, 0.38384, 0.66164, 0.54155, 0.72848,
    0.19325, 0.14413, 0.39663, 0.02181, 0.88448, 0.10622, 0.86225, 0.49767, 0.50816, 0.43852,
    0.25163, 0.65251, 0.36815, 0.64397, 0.04515, 0.83761, 0.14387, 0.51321, 0.72472, 0.05466,
    0.73231, 0.18065, 0.06253, 0.99413, 0.35159, 0.19121, 0.78508, 0.2038, 0.10268, 0.3722,
    0.15957, 0.2634, 0.73701, 0.25332, 0.18782, 0.41349, 0.74761, 0.49431, 0.83436, 0.11834,
    0.81549, 0.70951, 0.77544, 0.68161, 0.03584, 0.48391, 0.31704, 0.04037, 0.97616, 0.59693,
    0.01889, 0.07629, 0.43625, 0.11692, 0.25624, 0.60873, 0.06345, 0.92246, 0.00008, 0.55306,
    0.39528, 0.81616, 0.07586, 0.90767, 0.40188, 0.34414, 0.63439, 0.67049, 0.79495, 0.91704,
    0.48545, 0.75122, 0.92904, 0.68902, 0.94972, 0.19152, 0.36024, 0.94458, 0.54158, 0.75051,
    0.60365, 0.83799, 0.3296, 0.19322, 0.1122, 0.31751, 0.88492, 0.30934, 0.22888, 0.78212,
    0.70014, 0.37239, 0.18637, 0.05327, 0.95096, 0.43253, 0.80854, 0.80088, 0.8089, 0.93128,
    0.72484, 0.18711, 0.1612, 0.04235, 0.28193, 0.82157, 0.75363, 0.0907, 0.04146, 0.30552,
    0.35247, 0.11724, 0.13141, 0.63742, 0.11598, 0.00023, 0.00867, 0.74284, 0.34243, 0.93029,
    0.94653, 0.42402, 0.07405, 0.53845, 0.94747, 0.5726, 0.99382, 0.47744, 0.48893, 0.16993,
    0.15021, 0.33295, 0.37509, 0.82162, 0.67946, 0.84145, 0.90279, 0.77074, 0.18002, 0.18464,
    0.82474, 0.53342, 0.82641, 0.13574, 0.29593, 0.86887, 0.44989, 0.93399, 0.52162, 0.04737,
    0.18619, 0.74627, 0.32392, 0.78464, 0.62095, 0.12302, 0.76378, 0.05041, 0.46978, 0.47665,
    0.35075, 0.56623, 0.36409, 0.5762, 0.07399, 0.6898, 0.14454, 0.07481, 0.27499, 0.45902,
    0.68971, 0.18477, 0.14707, 0.83745, 0.1693, 0.20368, 0.41196, 0.66919, 0.35352, 0.79982,
    0.25593, 0.44276, 0.2282, 0.172, 0.88627, 0.55087, 0.16822, 0.45547, 0.90286, 0.21031,
    0.13674, 0.73707, 0.19763, 0.22501, 0.36787, 0.80783, 0.41605, 0.49807, 0.35482, 0.64382,
    0.33949, 0.34442, 0.83232, 0.52606, 0.37408, 0.05339, 0.04504, 0.83828, 0.98748, 0.91386,
    0.11403, 0.65622, 0.93997, 0.22567, 0.33361, 0.07126, 0.3748, 0.31678, 0.54131, 0.68416
]

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
            fn_xi = (i + 1) / self.N  # Fn(xi) = i/N, donde i es la posición del número ordenado.
            f_xi = xi  # F(xi) = xi para la distribución uniforme (0,1).
            diferencia = abs(fn_xi - f_xi)  # |Fn(xi) - F(xi)|
            diferencias.append(diferencia)
        d_estadistico = max(diferencias)  # D = max |Fn(xi) - F(xi)|
        
        # Calculamos el valor crítico usando la fórmula de Coss Bu para α=0.05.
        d_critico = 1.36 / np.sqrt(self.N)  # Dα = 1.36/√N para α=0.05 y N grande.
        
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
        
        # Calculamos el valor crítico Dα usando la fórmula 1.36 / sqrt(N) para un nivel de significancia del 0.05.
        # Esta fórmula es una aproximación comúnmente usada para la distribución de Kolmogorov-Smirnov para muestras grandes (N > 35) cuando α = 0.05.
        if N > 0:
            valor_critico_cos = 1.36 / np.sqrt(N)
            reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
            reporte += "\nEl valor crítico (Dα) para  el nivel de significancia \u03b1 = 0.05 y para N grande se puede aproximar con la fórmula:"
            reporte += "\nD\u03b1 \u2248 1.36 / \u221aN"
            reporte += f"\nD\u03b1 \u2248 1.36 / \u221a{N} = 1.36 / {np.sqrt(N):.5f} = {valor_critico_cos:.5f}"
        else:
            valor_critico_cos = float('inf')  # Evitar división por cero, aunque la validación previa debería prevenir esto.
            reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
            reporte += "\nNo se puede calcular el valor crítico con N=0."
        
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
            
        reporte += "\n" + "="*80
        return reporte

if __name__ == "__main__":
    # Crear y ejecutar la prueba con los 400 números proporcionados.
    prueba = PruebaKolmogorovSmirnov(numeros=numeros, alpha=0.05)
    print(prueba.generar_reporte())
