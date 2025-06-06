import numpy as np # Importamos numpy para operaciones matemáticas eficientes con arrays y matrices.
from scipy.stats import chi2 # Importamos la distribución chi-cuadrada para calcular el valor crítico de la prueba.
from typing import List, Dict, Union # Importamos tipos para mejorar la documentación y el tipado del código.

class GCM:
    def __init__(self, m: int, X0: int, a: int):
        self.m = m
        self.X0 = X0
        self.a = a
        self.Xn = X0
        
    def generar_numero(self) -> float:
        self.Xn = (self.a * self.Xn) % self.m
        return self.Xn / self.m

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
    # Parámetros del GCM
    parametros = [
        {"m": 32057, "X0": 20855, "a": 9600}
    ]
    
    # Aplicar la prueba a cada conjunto de parámetros.
    for params in parametros:
        print(f"\nProbando con m={params['m']}, X0={params['X0']}, a={params['a']}")
        print("="*80)
        
        # Generar números pseudoaleatorios.
        gcm = GCM(params['m'], params['X0'], params['a'])
        numeros = [gcm.generar_numero() for _ in range(10000)]
        
        # Crear y ejecutar la prueba.
        prueba = PruebaFrecuencias(numeros=numeros, n_intervalos=5, alpha=0.05)
        print(prueba.generar_reporte())