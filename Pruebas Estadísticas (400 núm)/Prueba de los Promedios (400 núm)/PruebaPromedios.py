import numpy as np #Proporciona estructuras de datos eficientes para arrays y matrices.
from scipy.stats import norm #Es una biblioteca para computación científica y estadística que importa la "Distribución normal estándar".
from typing import List, Dict, Union #Es una biblioteca para anotaciones de tipos en Python. Nos ayuda a documentar los tipos de datos que esperamos.

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

class PruebaPromedios:
    def __init__(self, numeros: List[float], alpha: float = 0.05):
        # Inicializa la prueba de promedios con los números y el nivel de significancia.
        # Args:
        # numeros (List[float]): Lista de números pseudoaleatorios a probar.
        # alpha (float): Nivel de significancia (default 0.05).
        self.numeros = np.array(numeros) #Convierte la lista de números a un array de numpy para cálculos más eficientes.
        self.alpha = alpha #Nivel de significancia para la prueba de hipótesis.
        self.N = len(numeros) #Tamaño de la muestra (N = 400 números).
        
        # Inicialización de variables para almacenar resultados.
        self.promedio_muestral = None #Almacenará el promedio aritmético de los números (x̄).
        self.z_estadistico = None #Almacenará el valor del estadístico Z₀ calculado.
        self.z_critico = None #Almacenará el valor crítico Zα/2 de la distribución normal.
        self.decision = None #Almacenará la decisión final de la prueba.
        
        # Validar que los datos cumplan con los requisitos.
        self._validar_entradas()
    
    def _validar_entradas(self) -> None:
        # Verifica que los parámetros cumplan con los requisitos necesarios para la prueba.
        # Raises:
        # ValueError: Si el nivel de significancia no está entre 0 y 1.
        # ValueError: Si la lista de números está vacía.
        # ValueError: Si algún número está fuera del intervalo [0,1].
        if not (0 < self.alpha < 1): #Verifica que el nivel de significancia esté entre 0 y 1.
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1")
            
        if self.N == 0: #Verifica que la lista de números no esté vacía.
            raise ValueError("La lista de números no puede estar vacía")
            
        if any(not (0.0 <= num <= 1.0) for num in self.numeros): #Verifica que todos los números estén en el intervalo [0,1].
            raise ValueError("Todos los números deben estar en el intervalo [0.0, 1.0]")
    
    def calcular_promedio_muestral(self) -> float:
        # Calcula el promedio aritmético de los números pseudoaleatorios.
        # Fórmula: x̄ = (U₁ + U₂ + ... + Uₙ) / N
        # Returns:
        # float: Promedio muestral (x̄)
        self.promedio_muestral = np.mean(self.numeros) #Calcula el promedio usando la función mean() de numpy.
        return self.promedio_muestral
    
    def calcular_z_estadistico(self) -> float:
        # Calcula el estadístico Z₀ usando la fórmula:
        # Z₀ = [(x̄ - 0.5) * √N] / √(1/12)
        # Donde:
        # - x̄ es el promedio muestral
        # - N es el tamaño de la muestra (400)
        # - √(1/12) es la desviación estándar de la distribución uniforme (0,1)
        # Returns:
        # float: Valor del estadístico Z₀
        if self.promedio_muestral is None: #Si el promedio muestral no está calculado, lo calcula.
            self.calcular_promedio_muestral()
            
        promedio_esperado = 0.5 #Promedio esperado de la distribución uniforme (0,1).
        desviacion_uniforme = np.sqrt(1/12) #Desviación estándar de la distribución uniforme (0,1).
        
        # Cálculo del estadístico Z₀ usando la fórmula.
        self.z_estadistico = (self.promedio_muestral - promedio_esperado) * np.sqrt(self.N) / desviacion_uniforme
        return self.z_estadistico
    
    def obtener_z_critico(self) -> float:
        # Obtiene el valor crítico Zα/2 de la distribución normal estándar.
        # El valor crítico se obtiene de la distribución normal estándar para un nivel de significancia α/2.
        # Returns:
        # float: Valor crítico Zα/2
        self.z_critico = norm.ppf(1 - self.alpha/2) #Calcula el cuantil de la distribución normal estándar.
        return self.z_critico
    
    def tomar_decision(self) -> str:
        # Toma la decisión estadística basada en la comparación de |Z₀| con Zα/2.
        # Criterio de decisión:
        # - Si |Z₀| < Zα/2: No se rechaza H₀
        # - Si |Z₀| ≥ Zα/2: Se rechaza H₀
        # Returns:
        # str: Decisión de la prueba
        if self.z_estadistico is None: #Si el estadístico Z₀ no está calculado, lo calcula.
            self.calcular_z_estadistico()
        if self.z_critico is None: #Si el valor crítico Zα/2 no está calculado, lo calcula.
            self.obtener_z_critico()
            
        # Toma la decisión según el criterio establecido.
        if abs(self.z_estadistico) < self.z_critico:
            self.decision = "No se rechaza H₀: Los números provienen de una distribución uniforme con promedio 0.5"
        else:
            self.decision = "Se rechaza H₀: Los números no provienen de una distribución uniforme con promedio 0.5"
            
        return self.decision
    
    def ejecutar_prueba(self) -> Dict[str, Union[float, str]]:
        # Ejecuta la prueba completa y devuelve todos los resultados.
        # El proceso incluye:
        # 1. Calcular el promedio muestral
        # 2. Calcular el estadístico Z₀
        # 3. Obtener el valor crítico Zα/2
        # 4. Tomar la decisión estadística
        # Returns:
        # Dict: Diccionario con todos los resultados de la prueba
        self.calcular_promedio_muestral() #Calcula el promedio muestral.
        self.calcular_z_estadistico() #Calcula el estadístico Z₀.
        self.obtener_z_critico() #Obtiene el valor crítico Zα/2.
        self.tomar_decision() #Toma la decisión estadística.
        
        return {
            "tamaño_muestra": self.N, #Tamaño de la muestra (400 números).
            "nivel_significancia": self.alpha, #Nivel de significancia (α = 0.05).
            "promedio_muestral": self.promedio_muestral, #Promedio muestral calculado.
            "z_estadistico": self.z_estadistico, #Valor del estadístico Z₀.
            "z_critico": self.z_critico, #Valor crítico Zα/2.
            "decision": self.decision #Decisión final de la prueba.
        }
    
    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba con todos los resultados y cálculos.
        # El reporte incluye:
        # - Hipótesis nula y alternativa
        # - Parámetros de la prueba
        # - Resultados obtenidos
        # - Cálculo del estadístico Z₀
        # - Decisión estadística
        # Returns:
        # str: Reporte formateado de la prueba
        if self.promedio_muestral is None: #Si el promedio muestral no está calculado, ejecuta la prueba.
            self.ejecutar_prueba()
            
        reporte = "\n" + "="*80 #Línea separadora.
        reporte += "\nPRUEBA DE LOS PROMEDIOS"
        reporte += "\n" + "="*80 #Línea separadora.
        
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\nHipótesis nula    (H₀) : μ = 0.5 (Los números provienen de una distribución uniforme con promedio 0.5)"
        reporte += "\nHipótesis altern. (H₁) : μ ≠ 0.5 (Los números no provienen de una distribución uniforme con promedio 0.5)"
        
        reporte += "\n\nPARÁMETROS PARA REALIZAR LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {self.N}" #Tamaño de la muestra (400 números).
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}" #Nivel de significancia (α = 0.05).
        
        reporte += "\n\nRESULTADOS OBTENIDOS:"
        reporte += f"\n- Promedio muestral (x̄) : {self.promedio_muestral:.5f}" #Promedio muestral con 5 decimales.
        reporte += f"\n- Promedio esperado (μ) : 0.50000" #Promedio esperado de la distribución uniforme.
        
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO Z₀:"
        reporte += "\nZ₀ = [(x̄ - 0.5) * √N] / √(1/12)"
        reporte += f"\n   = [({self.promedio_muestral:.5f} - 0.5) * √{self.N}] / 0.288675" #Cálculo detallado del estadístico Z₀.
        reporte += f"\n   = {self.z_estadistico:.5f}" #Valor final del estadístico Z₀.
        
        reporte += "\n\nDECISIÓN ESTADÍSTICA:"
        reporte += f"\n- Valor crítico Zα/2: {self.z_critico:.5f} (α={self.alpha})" #Valor crítico Zα/2.
        reporte += f"\n- |Z₀| = {abs(self.z_estadistico):.5f}" #Valor absoluto del estadístico Z₀.
        reporte += f"\n- Criterio: |Z₀| {'≥' if abs(self.z_estadistico) >= self.z_critico else '<'} Zα/2" #Criterio de decisión.
        reporte += f"\n\nConclusión: {self.decision}" #Decisión final de la prueba.
        
        reporte += "\n" + "="*80 #Línea separadora.
        return reporte #Retorna el reporte formateado.

if __name__ == "__main__":
    # Crear y ejecutar la prueba con los 400 números proporcionados.
    prueba = PruebaPromedios(numeros=numeros, alpha=0.05)
    print(prueba.generar_reporte())