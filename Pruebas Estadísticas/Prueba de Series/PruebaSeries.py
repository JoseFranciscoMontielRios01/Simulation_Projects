# Importamos numpy para realizar operaciones matemáticas y manejo de matrices.
import numpy as np
# Importamos la función chi2 que nos ayudará a calcular valores de la distribución chi-cuadrada.
from scipy.stats import chi2
# Importamos herramientas para definir tipos de datos que usaremos en el código.
from typing import List, Tuple

class GCM:
    def __init__(self, m: int, X0: int, a: int):
        # Inicializa el generador congruencial multiplicativo con los parámetros dados.
        self.m = m
        self.X0 = X0
        self.a = a
        self.Xn = X0
        
    def generar_numero(self) -> float:
        # Genera un número pseudoaleatorio usando el método congruencial multiplicativo.
        self.Xn = (self.a * self.Xn) % self.m
        return self.Xn / self.m

class PruebaSeries:
    # Implementa la Prueba de Series para validar números pseudoaleatorios.
    # Esta prueba estadística verifica si los números consecutivos son independientes mediante una prueba chi-cuadrada.
    # La prueba se basa en el siguiente proceso:
    # 1. Se forman pares consecutivos de números (x,y).
    # 2. Se divide el espacio [0,1]x[0,1] en k² celdas (k=5 según Coss Bu).
    # 3. Se cuenta cuántos pares caen en cada celda (frecuencias observadas).
    # 4. Se calcula el estadístico chi-cuadrado usando la fórmula: χ² = (k²/(N-1)) * Σ(FO-FE)².
    # 5. Se compara con el valor crítico de la distribución chi-cuadrada.
    # 6. Se toma la decisión estadística basada en esta comparación.
    
    def __init__(self):
        # Inicializa la prueba de series con los parámetros necesarios.
        # Creamos una lista vacía donde guardaremos nuestros números aleatorios.
        self.numeros: List[float] = []
        # Creamos una variable para contar cuántos números tenemos (N).
        self.n: int = 0
        # Definimos que usaremos 5 intervalos en cada dimensión (k=5 según Coss Bu).
        self.k: int = 5
        # Calculamos el tamaño de cada intervalo dividiendo 1 entre 5 (1/k).
        self.intervalo: float = 1.0 / self.k
        # Creamos una lista vacía donde guardaremos los pares de números consecutivos.
        self.pares: List[Tuple[float, float]] = []
        # Creamos una matriz de 5x5 llena de ceros para guardar las frecuencias observadas.
        self.frecuencias_obs: np.ndarray = np.zeros((self.k, self.k))
        # Definimos el nivel de significancia α=0.05 para nuestra prueba estadística.
        self.alpha: float = 0.05
        
    def cargar_numeros_pseudoaleatorios(self, numeros: List[float]) -> None:
        # Carga los números pseudoaleatorios y realiza los cálculos iniciales.
        # Este método:
        # 1. Carga la lista de números pseudoaleatorios.
        # 2. Actualiza el tamaño de la muestra (N).
        # 3. Calcula el tamaño del intervalo.
        # 4. Forma los pares consecutivos.
        # 5. Calcula las frecuencias observadas.
        try:
            self.numeros = numeros
            self.n = len(self.numeros)
            self.intervalo = 1.0 / self.k
            self.formar_pares_consecutivos()
            self.calcular_frecuencias_observadas()
        except Exception as e:
            # Si ocurre algún error, lo mostramos en pantalla.
            print(f"Error al cargar los números: {str(e)}")
            raise
    
    def formar_pares_consecutivos(self) -> None:
        # Forma pares consecutivos de números para la prueba.
        # Para cada número en la lista (excepto el último), creamos un par con el siguiente número.
        # Esto nos da N-1 pares en total.
        self.pares = [(self.numeros[i], self.numeros[i+1]) 
                     for i in range(len(self.numeros)-1)]
        
    def determinar_celda(self, x: float, y: float) -> Tuple[int, int]:
        # Determina la celda de la matriz a la que pertenece un par (x,y).
        # Args:
        #   x (float): Primer número del par.
        #   y (float): Segundo número del par.
        # Returns:
        #   Tuple[int, int]: Índices de la celda en la matriz.
        # Calculamos la posición horizontal dividiendo x entre el tamaño del intervalo.
        celda_x = int(x / self.intervalo)
        # Calculamos la posición vertical dividiendo y entre el tamaño del intervalo.
        celda_y = int(y / self.intervalo)
        # Si el número cae justo en el límite, lo ajustamos para que caiga en la última celda.
        if celda_x == self.k: celda_x = self.k - 1
        if celda_y == self.k: celda_y = self.k - 1
        return celda_x, celda_y
    
    def calcular_frecuencias_observadas(self) -> None:
        # Calcula las frecuencias observadas para cada celda de la matriz.
        # Este método:
        # 1. Inicializa la matriz de frecuencias con ceros.
        # 2. Para cada par (x,y), determina su celda.
        # 3. Incrementa el contador en esa celda.
        # Creamos una matriz de 5x5 llena de ceros.
        self.frecuencias_obs = np.zeros((self.k, self.k))
        # Para cada par de números, incrementamos el contador en su celda correspondiente.
        for x, y in self.pares:
            celda_x, celda_y = self.determinar_celda(x, y)
            self.frecuencias_obs[celda_x][celda_y] += 1
            
    def calcular_estadistico(self) -> float:
        # Calcula el estadístico chi-cuadrado según la fórmula de Coss Bu.
        # Returns:
        #   float: Valor del estadístico chi-cuadrado.
        # Calculamos la frecuencia esperada: (N-1)/(k²).
        fe = (self.n - 1) / (self.k * self.k)
        # Calculamos la suma de las diferencias cuadradas entre lo observado y lo esperado.
        suma_diferencias = sum(((self.frecuencias_obs[i][j] - fe) ** 2) 
                             for i in range(self.k) for j in range(self.k))
        # Calculamos el estadístico chi-cuadrado: (k²/(N-1)) * Σ(FO-FE)².
        chi_cuadrado = (self.k * self.k / (self.n - 1)) * suma_diferencias
        return chi_cuadrado
    
    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba con todos los resultados y cálculos.
        # El reporte incluye:
        # - Hipótesis nula y alternativa
        # - Parámetros de la prueba
        # - Matriz de frecuencias observadas
        # - Matriz de diferencias cuadradas
        # - Cálculo del estadístico chi-cuadrado
        # - Decisión estadística
        # Returns:
        #   str: Reporte formateado de la prueba.
        # Creamos el encabezado del reporte con líneas decorativas.
        reporte = "\n" + "="*80
        reporte += "\nPRUEBA DE SERIES - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "="*80
        
        # Agregamos las hipótesis que estamos probando.
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\n- Hipótesis nula   (H₀) : Los números consecutivos son independientes (no presentan dependencia)."
        reporte += "\n- Hipótesis alter. (H₁) : Los números consecutivos presentan dependencia (no son independientes)."
        
        # Agregamos los parámetros que usamos en la prueba.
        reporte += "\n\nPARÁMETROS DE LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {self.n}"
        reporte += f"\n- Número de intervalos   (k) : {self.k}"
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}"
        reporte += f"\n- Total de pares         (m) : {len(self.pares)}"
        
        # Calculamos y mostramos la frecuencia esperada.
        fe = (self.n - 1) / (self.k * self.k)
        reporte += "\n\nCÁLCULO DE FRECUENCIAS ESPERADAS:"
        reporte += f"\nFE = (N-1)/k² = ({self.n}-1)/{self.k}² = {fe:.2f}"
        
        # Creamos los intervalos para mostrar en las matrices.
        intervalos = [round((i+1)*self.intervalo, 1) for i in range(self.k)]
        ancho = 9  # Definimos un ancho fijo para que las columnas se alineen.
        
        # Generamos la matriz de frecuencias observadas.
        reporte += "\n\nFrecuencia Observada (FO):"
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos])
        suma_fo = 0
        for i in range(self.k):
            fila = f"{intervalos[i]:>{ancho}.1f}"
            for j in range(self.k):
                valor_fo = int(self.frecuencias_obs[i][j])
                suma_fo += valor_fo
                fila += f"{valor_fo:>{ancho}d}"
            reporte += "\n" + fila
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos])
        
        # Generamos la matriz de diferencias cuadradas.
        reporte += "\n\nDIFERENCIA ENTRE LA FRECUENCIA OBSERVADA Y ESPERADA:"
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos])
        suma_diferencias = 0
        terminos_diff = []
        for i in range(self.k):
            fila = f"{intervalos[i]:>{ancho}.1f}"
            for j in range(self.k):
                diferencia_cuadrada = (self.frecuencias_obs[i][j] - fe) ** 2
                suma_diferencias += diferencia_cuadrada
                terminos_diff.append(f"({int(self.frecuencias_obs[i][j])}-{fe:.2f})²={diferencia_cuadrada:.4f}")
                fila += f"{diferencia_cuadrada:>{ancho}.4f}"
            reporte += "\n" + fila
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos])
        
        # Mostramos el cálculo detallado de la suma de diferencias.
        reporte += "\n\nCÁLCULO DE LA SUMA DE DIFERENCIAS CUADRADAS:"
        reporte += "\nSuma = " + " + ".join(terminos_diff)
        reporte += f"\nSuma = {suma_diferencias:.5f}"
        
        # Calculamos el estadístico chi-cuadrado y el valor crítico.
        chi_cuadrado = self.calcular_estadistico()
        gl = (self.k - 1) ** 2
        valor_critico = chi2.ppf(0.95, gl)
        
        # Mostramos el cálculo del estadístico.
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO CHI-CUADRADA:"
        reporte += "\nχ² = (k²/(N-1)) * Σ(FO-FE)²"
        reporte += f"\nχ² = ({self.k}²/{self.n-1}) * Σ(FO-{fe:.2f})²"
        reporte += f"\nχ² = {chi_cuadrado:.5f}"
        
        # Mostramos el valor crítico y los grados de libertad.
        reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
        reporte += f"\nGrados de libertad = (k-1)² = ({self.k}-1)² = {gl}"
        reporte += f"\nValor crítico χ²(α={self.alpha}, gl={gl}) = {valor_critico:.5f}"
        
        # Mostramos la decisión final basada en la comparación.
        reporte += "\n\nDECISIÓN:"
        if chi_cuadrado > valor_critico:
            reporte += f"\nComo χ² = {chi_cuadrado:.5f} > {valor_critico:.5f}"
            reporte += "\nSe rechaza H₀: Los números consecutivos son dependientes ( presentan dependencia)."
            reporte += "\nConclusión: Existe evidencia de dependencia entre números consecutivos."
        else:
            reporte += f"\nComo χ² = {chi_cuadrado:.5f} ≤ {valor_critico:.5f}"
            reporte += "\nNo se rechaza H₀: Los números consecutivos son independientes (no presentan dependencia)."
            reporte += "\nConclusión: No hay evidencia suficiente de dependencia entre números consecutivos."
        
        # Agregamos una línea decorativa al final del reporte.
        reporte += "\n" + "="*80
        return reporte
    
    def realizar_prueba(self, numeros: List[float]) -> None:
        # Ejecuta la prueba completa de series.
        # Este método:
        # 1. Carga los números pseudoaleatorios.
        # 2. Forma los pares consecutivos.
        # 3. Calcula las frecuencias observadas.
        # 4. Genera y muestra el reporte.
        self.cargar_numeros_pseudoaleatorios(numeros)
        self.formar_pares_consecutivos()
        self.calcular_frecuencias_observadas()
        print(self.generar_reporte())

# Este bloque se ejecuta solo si el archivo se ejecuta directamente.
if __name__ == "__main__":
    # Parámetros del GCM para generar números pseudoaleatorios.
    parametros = [
        {"m": 32057, "X0": 20855, "a": 9600}
    ]
    
    # Aplicar la prueba a cada conjunto de parámetros.
    for params in parametros:
        print(f"\nProbando con m={params['m']}, X0={params['X0']}, a={params['a']}")
        print("="*80)
        
        # Generar números pseudoaleatorios usando el GCM.
        gcm = GCM(params['m'], params['X0'], params['a'])
        numeros = [gcm.generar_numero() for _ in range(10000)]
        
        # Crear y ejecutar la prueba de series.
        prueba = PruebaSeries()
        prueba.realizar_prueba(numeros) 