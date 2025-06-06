import numpy as np #Proporciona estructuras de datos eficientes para arrays y matrices.
from scipy.stats import norm #Es una biblioteca para computación científica y estadística que importa la "Distribución normal estándar".
from typing import List, Dict, Union #Es una biblioteca para anotaciones de tipos en Python. Nos ayuda a documentar los tipos de datos que esperamos.

class GCM:
    def __init__(self, m: int, X0: int, a: int):
        self.m = m
        self.X0 = X0
        self.a = a
        self.Xn = X0
        
    def generar_numero(self) -> float:
        self.Xn = (self.a * self.Xn) % self.m
        return self.Xn / self.m

class PruebaPromedios:
    # Implementa la Prueba de los Promedios para validar números pseudoaleatorios.
    # Esta prueba estadística verifica si los números provienen de una distribución uniforme (0,1) con promedio teórico de 0.5 mediante una prueba de hipótesis estadística.
    # La prueba se basa en el siguiente proceso:
    # 1. Se calcula el promedio aritmético de los números pseudoaleatorios.
    # 2. Se calcula el estadístico Z₀ usando la fórmula: Z₀ = [(x̄ - 0.5) * √N] / √(1/12).
    # 3. Se compara |Z₀| con el valor crítico Zα/2 de la distribución normal estándar.
    # 4. Se toma la decisión estadística basada en esta comparación.
    
    def __init__(self, numeros: List[float], alpha: float = 0.05):
        # Inicializa la prueba de promedios con los números y el nivel de significancia.
        # Args:
        # numeros (List[float]): Lista de números pseudoaleatorios a probar
        # alpha (float): Nivel de significancia (default 0.05)
        #Estamos creando un atributo "self." que pertenece a esta instancia específica de la clase actual.
        # Convertir la lista a array de numpy para cálculos más eficientes; por ejemplo, para usar la función np.mean() que calcula el promedio.
        self.numeros = np.array(numeros) #Es una lista de números pseudoaleatorios.
        self.alpha = alpha #Es el nivel de significancia.
        self.N = len(numeros) #Es el tamaño de la muestra.
        
        # Inicialización de variables para almacenar resultados.
        self.promedio_muestral = None  # Promedio aritmético de los números.
        self.z_estadistico = None     # Valor del estadístico Z₀.
        self.z_critico = None         # Valor crítico Zα/2.
        self.decision = None          # Decisión final de la prueba.
        
        # Validar que los datos cumplan con los requisitos.
        self._validar_entradas()
    
    def _validar_entradas(self) -> None:
        # Verifica que los parámetros cumplan con los requisitos necesarios para la prueba.
        # Raises:
        # ValueError: Si el nivel de significancia no está entre 0 y 1
        # ValueError: Si la lista de números está vacía
        # ValueError: Si algún número está fuera del intervalo [0,1]
        if not (0 < self.alpha < 1): #Si el nivel de significancia no está entre 0 y 1, se lanza un error.
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1")
            
        if self.N == 0: #Si el tamaño de la muestra es 0, se lanza un error.
            raise ValueError("La lista de números no puede estar vacía")
            
        if any(not (0.0 <= num <= 1.0) for num in self.numeros): #any() es una función que verifica si algún elemento de la lista cumple con la condición.
            raise ValueError("Todos los números deben estar en el intervalo [0.0, 1.0]")
    
    def calcular_promedio_muestral(self) -> float:
        # Calcula el promedio aritmético de los números pseudoaleatorios.
        # El promedio se calcula como: x̄ = (U₁ + U₂ + ... + Uₙ) / N
        # Returns:
        # float: Promedio muestral (x̄)
        self.promedio_muestral = np.mean(self.numeros) #np.mean() es una función de numpy que calcula el promedio de los elementos de un array.
        return self.promedio_muestral
    
    def calcular_z_estadistico(self) -> float:
        # Calcula el estadístico Z₀ usando la fórmula:
        # Z₀ = [(x̄ - 0.5) * √N] / √(1/12)
        # Donde:
        # - x̄ es el promedio muestral
        # - N es el tamaño de la muestra
        # - √(1/12) es la desviación estándar de la distribución uniforme (0,1)
        # Returns:
        # float: Valor del estadístico Z₀
        # Asegurar que el promedio muestral esté calculado.
        if self.promedio_muestral is None: #Si el promedio muestral no está calculado, se calcula.
            self.calcular_promedio_muestral() 
            
        # Promedio esperado de la distribución uniforme (0,1).
        promedio_esperado = 0.5
        
        # Desviación estándar de la distribución uniforme (0,1).
        desviacion_uniforme = np.sqrt(1/12) #np.sqrt() es una función de numpy que calcula la raíz cuadrada de un número.
        
        # Cálculo del estadístico Z₀.
        self.z_estadistico = (self.promedio_muestral - promedio_esperado) * np.sqrt(self.N) / desviacion_uniforme
        return self.z_estadistico
    
    def obtener_z_critico(self) -> float:
        # Obtiene el valor crítico Zα/2 de la distribución normal estándar.
        # El valor crítico se obtiene de la distribución normal estándar para un nivel de significancia α/2.
        # Returns:
        # float: Valor crítico Zα/2
        self.z_critico = norm.ppf(1 - self.alpha/2) #norm.ppf() es una función de scipy.stats que calcula el cuantil de la distribución normal estándar.
        return self.z_critico
    
    def tomar_decision(self) -> str:
        # Toma la decisión estadística basada en la comparación de |Z₀| con Zα/2.
        # La decisión se toma según el siguiente criterio:
        # - Si |Z₀| < Zα/2: No se rechaza H₀
        # - Si |Z₀| ≥ Zα/2: Se rechaza H₀
        # Returns:
        # str: Decisión de la prueba
        # Asegurar que los valores necesarios estén calculados
        if self.z_estadistico is None: #Si el estadístico Z₀ no está calculado, se calcula.
            self.calcular_z_estadistico()
        if self.z_critico is None: #Si el valor crítico Zα/2 no está calculado, se calcula.
            self.obtener_z_critico()
            
        # Tomar decisión según el criterio
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
        self.calcular_promedio_muestral() 
        self.calcular_z_estadistico()
        self.obtener_z_critico()
        self.tomar_decision()
        
        return {
            "tamaño_muestra": self.N, #Es el tamaño de la muestra.
            "nivel_significancia": self.alpha, #Es el nivel de significancia.
            "promedio_muestral": self.promedio_muestral, #Es el promedio muestral.
            "z_estadistico": self.z_estadistico, #Es el estadístico Z₀.
            "z_critico": self.z_critico, #Es el valor crítico Zα/2.
            "decision": self.decision #Es la decisión final de la prueba.
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
        # str: Imprimir el reporte formateado de la prueba
        # Asegurar que la prueba se haya ejecutado
        if self.promedio_muestral is None: #Si el promedio muestral no está calculado, se ejecuta la prueba.
            self.ejecutar_prueba()
            
        reporte = "\n" + "="*80 #Es una línea de 80 caracteres.
        reporte += "\nPRUEBA DE LOS PROMEDIOS"
        reporte += "\n" + "="*80 #Es una línea de 80 caracteres.
        
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\nHipótesis nula    (H₀) : μ = 0.5 (Los números provienen de una distribución uniforme con promedio 0.5)"
        reporte += "\nHipótesis altern. (H₁) : μ ≠ 0.5 (Los números no provienen de una distribución uniforme con promedio 0.5)"
        
        reporte += "\n\nPARÁMETROS PARA REALIZAR LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {self.N}" #Es el tamaño de la muestra.
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}" #Es el nivel de significancia.
        
        reporte += "\n\nRESULTADOS OBTENIDOS:"
        reporte += f"\n- Promedio muestral (x̄) : {self.promedio_muestral:.5f}" #Es el promedio muestral con 5 decimales.
        reporte += f"\n- Promedio esperado (μ) : 0.50000"
        
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO Z₀:"
        reporte += "\nZ₀ = [(x̄ - 0.5) * √N] / √(1/12)"
        reporte += f"\n   = [({self.promedio_muestral:.5f} - 0.5) * √{self.N}] / 0.288675" #Es el estadístico Z₀ con 5 decimales.
        reporte += f"\n   = {self.z_estadistico:.5f}" #Es el estadístico Z₀ con 5 decimales.
        
        reporte += "\n\nDECISIÓN ESTADÍSTICA:"
        reporte += f"\n- Valor crítico Zα/2: {self.z_critico:.5f} (α={self.alpha})" #Es el valor crítico Zα/2 con 5 decimales.
        reporte += f"\n- |Z₀| = {abs(self.z_estadistico):.5f}" #Es el valor absoluto del estadístico Z₀ con 5 decimales.
        reporte += f"\n- Criterio: |Z₀| {'≥' if abs(self.z_estadistico) >= self.z_critico else '<'} Zα/2" #Es el criterio de la prueba.
        reporte += f"\n\nConclusión: {self.decision}" #Es la decisión final de la prueba.
        
        reporte += "\n" + "="*80 #Es una línea de 80 caracteres.
        return reporte #Es el reporte formateado de la prueba.

if __name__ == "__main__":
    # Parámetros del GCM
    parametros = [
        {"m": 32057, "X0": 20855, "a": 9600},
    ]
    
    # Aplicar la prueba a cada conjunto de parámetros
    for params in parametros:
        print(f"\nProbando con m={params['m']}, X0={params['X0']}, a={params['a']}")
        print("="*80)
        
        # Generar números pseudoaleatorios
        gcm = GCM(params['m'], params['X0'], params['a'])
        numeros = [gcm.generar_numero() for _ in range(10000)]
        
        # Crear y ejecutar la prueba
        prueba = PruebaPromedios(numeros=numeros, alpha=0.05)
        print(prueba.generar_reporte())