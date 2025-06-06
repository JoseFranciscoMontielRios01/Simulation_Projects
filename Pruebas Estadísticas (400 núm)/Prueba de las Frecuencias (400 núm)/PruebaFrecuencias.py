import numpy as np # Importamos numpy para operaciones matemáticas eficientes con arrays y matrices.
from scipy.stats import chi2 # Importamos la distribución chi-cuadrada para calcular el valor crítico de la prueba.
from typing import List, Dict, Union # Importamos tipos para mejorar la documentación y el tipado del código.

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

class PruebaFrecuencias:
    # Clase que implementa la Prueba de Frecuencias para validar números pseudoaleatorios, dividiendo el intervalo [0,1] en n subintervalos y comparando las frecuencias observadas con las esperadas mediante la prueba chi-cuadrada.
    # La prueba verifica si los números siguen una distribución uniforme mediante la hipótesis H₀: los números provienen de una distribución uniforme (0,1) vs H₁: los números no provienen de una distribución uniforme (0,1).
    # El estadístico de prueba es χ² = Σ(FO-FE)²/FE, donde FO son las frecuencias observadas y FE es la frecuencia esperada (N/n).
    # La decisión se toma comparando χ² con el valor crítico de la distribución chi-cuadrada con n-1 grados de libertad y nivel de significancia α.
    
    def __init__(self, numeros: List[float], n_intervalos: int = 5, alpha: float = 0.05): # Constructor que inicializa la prueba con los números a analizar, número de intervalos y nivel de significancia.
        self.numeros = np.array(numeros) # Convertimos la lista de números a un array de numpy para operaciones vectorizadas.
        self.n_intervalos = n_intervalos # Número de subintervalos en los que dividiremos el rango [0,1].
        self.alpha = alpha # Nivel de significancia para la prueba (probabilidad de error tipo I).
        self.N = len(numeros) # Tamaño total de la muestra (cantidad de números a analizar).
        
        # Inicialización de variables para almacenar resultados de la prueba.
        self.frecuencias_obs = None # Array que almacenará las frecuencias observadas en cada intervalo.
        self.frecuencia_esp = None # Valor de la frecuencia esperada (N/n_intervalos).
        self.chi_cuadrada = None # Estadístico chi-cuadrada calculado.
        self.valor_critico = None # Valor crítico de la distribución chi-cuadrada.
        self.decision = None # Decisión final de la prueba.
        
        self._validar_entradas() # Validamos que los parámetros cumplan con los requisitos necesarios.
    
    def _validar_entradas(self) -> None: # Método que verifica que los parámetros de entrada sean válidos para la prueba.
        if not (0 < self.alpha < 1): # El nivel de significancia debe estar entre 0 y 1.
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1") # Si no, se lanza un error.
        
        if self.N == 0: # La muestra no puede estar vacía.
            raise ValueError("La lista de números no puede estar vacía") # Si no, se lanza un error.
        
        if any(not (0.0 <= num <= 1.0) for num in self.numeros): # Todos los números deben estar en [0,1].
            raise ValueError("Todos los números deben estar en el intervalo [0.0, 1.0]") # Si no, se lanza un error.
        
        if self.n_intervalos < 2: # Debe haber al menos 2 intervalos para la prueba.
            raise ValueError("El número de intervalos debe ser al menos 2") # Si no, se lanza un error.
    
    def calcular_frecuencias(self) -> None:
        # Método que calcula las frecuencias observadas y esperadas para cada intervalo.
        limites = np.linspace(0, 1, self.n_intervalos + 1) # Generamos los límites de los intervalos uniformemente espaciados.
        self.frecuencias_obs = np.histogram(self.numeros, bins=limites)[0] # Calculamos las frecuencias observadas usando histograma.
        self.frecuencia_esp = self.N / self.n_intervalos # La frecuencia esperada es N/n (total de números entre número de intervalos).
    
    def calcular_chi_cuadrada(self) -> float:
        # Método que calcula el estadístico chi-cuadrada usando la fórmula: χ² = Σ(FO-FE)²/FE.
        if self.frecuencias_obs is None: # Si no se han calculado las frecuencias, las calculamos.
            self.calcular_frecuencias() # Calculamos las frecuencias observadas.
        
        # Calculamos χ² = Σ(FO-FE)²/FE usando operaciones vectorizadas de numpy
        self.chi_cuadrada = np.sum((self.frecuencias_obs - self.frecuencia_esp)**2 / self.frecuencia_esp) # Calculamos el estadístico chi-cuadrada.
        return self.chi_cuadrada # Devolvemos el estadístico chi-cuadrada.
    
    def obtener_valor_critico(self) -> float:
        # Método que obtiene el valor crítico de la distribución chi-cuadrada para α y n-1 grados de libertad.
        self.valor_critico = chi2.ppf(1 - self.alpha, self.n_intervalos - 1) # Usamos la función de punto percentil de chi2.
        return self.valor_critico # Devolvemos el valor crítico.
    
    def tomar_decision(self) -> str:
        # Método que toma la decisión estadística comparando χ² con el valor crítico.
        if self.chi_cuadrada is None: # Si no se ha calculado χ², lo calculamos.
            self.calcular_chi_cuadrada() # Calculamos el estadístico chi-cuadrada.
        if self.valor_critico is None: # Si no se ha calculado el valor crítico, lo calculamos.
            self.obtener_valor_critico() # Obtenemos el valor crítico.
        
        # Si χ² < valor_critico, no rechazamos H₀; en caso contrario, rechazamos H₀.
        if self.chi_cuadrada < self.valor_critico:
            self.decision = "No se rechaza H₀: Los números provienen de una distribución uniforme." # Si χ² < valor_critico, no rechazamos H₀; en caso contrario, rechazamos H₀.
        else:
            self.decision = "Se rechaza H₀: Los números no provienen de una distribución uniforme." # Si χ² < valor_critico, no rechazamos H₀; en caso contrario, rechazamos H₀.
        
        return self.decision # Devolvemos la decisión final.
    
    def ejecutar_prueba(self) -> Dict[str, Union[float, str, np.ndarray]]: # Método que ejecuta la prueba completa y devuelve todos los resultados en un diccionario.
        self.calcular_frecuencias() # Calculamos frecuencias observadas y esperadas.
        self.calcular_chi_cuadrada() # Calculamos el estadístico chi-cuadrada.
        self.obtener_valor_critico() # Obtenemos el valor crítico.
        self.tomar_decision() # Tomamos la decisión estadística.
        
        # Devolvemos un diccionario con todos los resultados de la prueba.
        return {
            "tamaño_muestra": self.N, # Tamaño de la muestra.
            "n_intervalos": self.n_intervalos, # Número de intervalos.
            "nivel_significancia": self.alpha, # Nivel de significancia.
            "frecuencias_obs": self.frecuencias_obs, # Frecuencias observadas.
            "frecuencia_esp": self.frecuencia_esp, # Frecuencia esperada.
            "chi_cuadrada": self.chi_cuadrada, # Estadístico chi-cuadrada.
            "valor_critico": self.valor_critico, # Valor crítico.
            "decision": self.decision # Decisión final.
        }
    
    def generar_reporte(self) -> str: # Método que genera un reporte detallado de la prueba con todos los cálculos.
        if self.chi_cuadrada is None: # Si no se ha ejecutado la prueba, la ejecutamos.
            self.ejecutar_prueba()
        
        # Generamos el encabezado del reporte.
        reporte = "\n" + "="*80 # Agregamos una línea de separación.
        reporte += "\nPRUEBA DE FRECUENCIAS - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "="*80 # Agregamos una línea de separación.
        
        # Agregamos las hipótesis.
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\nHipótesis nula    (H₀) : Los números provienen de una distribución uniforme (0,1)."
        reporte += "\nHipótesis altern. (H₁) : Los números no provienen de una distribución uniforme (0,1)."
        
        # Agregamos los parámetros de la prueba.
        reporte += "\n\nPARÁMETROS DE LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {self.N}" # Agregamos el tamaño de la muestra.
        reporte += f"\n- Número de intervalos   (n) : {self.n_intervalos}" # Agregamos el número de intervalos.
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}" # Agregamos el nivel de significancia.
        
        # Agregamos el cálculo de frecuencias esperadas
        reporte += "\n\nCÁLCULO DE FRECUENCIAS ESPERADAS:"
        reporte += f"\nFE = N/n = {self.N}/{self.n_intervalos} = {self.frecuencia_esp:.1f}" # Agregamos el cálculo de las frecuencias esperadas.
        
        # Agregamos las frecuencias por intervalo.
        reporte += "\n\nFRECUENCIAS POR INTERVALO:"
        reporte += "\n" + "-"*80 # Agregamos una línea de separación.
        reporte += "\nIntervalo | Frecuencia Obs. | Frecuencia Esp. | (FO-FE)²/FE"
        reporte += "\n" + "-"*80 # Agregamos una línea de separación.
        for i in range(self.n_intervalos): # Iteramos sobre cada intervalo.
            inicio = i/self.n_intervalos # Límite inferior del intervalo.
            fin = (i+1)/self.n_intervalos # Límite superior del intervalo.
            termino = (self.frecuencias_obs[i] - self.frecuencia_esp)**2 / self.frecuencia_esp # Término (FO-FE)²/FE.
            reporte += f"\n[{inicio:.1f}-{fin:.1f}] | {self.frecuencias_obs[i]:14d} | {self.frecuencia_esp:14.1f} | {termino:10.4f}" # Agregamos el cálculo de las frecuencias por intervalo.
        
        # Agregamos el cálculo del estadístico chi-cuadrada.
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO CHI-CUADRADA:"
        reporte += "\nChi cuadrada = Σ(FO-FE)²/FE"
        reporte += "\nChi cuadrada = "
        terminos = []
        for i in range(self.n_intervalos):
            termino = (self.frecuencias_obs[i] - self.frecuencia_esp)**2 / self.frecuencia_esp # Calculamos cada término.
            terminos.append(f"({self.frecuencias_obs[i]}-{self.frecuencia_esp:.1f})²/{self.frecuencia_esp:.1f}") # Agregamos el cálculo de cada término.
        reporte += " + ".join(terminos) # Unimos todos los términos con +.
        reporte += f"\nChi cuadrada = {self.chi_cuadrada:.4f}" # Agregamos el cálculo del estadístico chi-cuadrada.
        
        # Agregamos el cálculo del valor crítico.
        reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:" # Agregamos un encabezado.
        reporte += f"\nGrados de libertad = n-1 = {self.n_intervalos}-1 = {self.n_intervalos-1}" # Agregamos el cálculo de los grados de libertad.
        reporte += f"\nValor crítico Chi cuadrada(α={self.alpha}, Grados de libertad ={self.n_intervalos-1}) = {self.valor_critico:.4f}" # Agregamos el cálculo del valor crítico.
        
        # Agregamos la decisión final.
        reporte += "\n\nDECISIÓN:" # Agregamos un encabezado.
        reporte += f"\nComo Chi cuadrada = {self.chi_cuadrada:.4f} {'<' if self.chi_cuadrada < self.valor_critico else '>'} {self.valor_critico:.4f}" # Agregamos el cálculo de la decisión.
        reporte += f"\n{self.decision}" # Agregamos la decisión final.
        
        reporte += "\n" + "="*80 # Agregamos una línea de separación.    
        return reporte

if __name__ == "__main__":
    # Crear y ejecutar la prueba con los 400 números proporcionados.
    prueba = PruebaFrecuencias(numeros=numeros, n_intervalos=5, alpha=0.05)
    print(prueba.generar_reporte())