# Importamos numpy para realizar operaciones matemáticas y manejo de matrices.
import numpy as np
# Importamos la función chi2 que nos ayudará a calcular valores de la distribución chi-cuadrada.
from scipy.stats import chi2
# Importamos herramientas para definir tipos de datos que usaremos en el código.
from typing import List, Tuple

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

class PruebaSeries:
    def __init__(self):
        # Inicializa la prueba de series con los parámetros necesarios.
        self.numeros: List[float] = [] #Lista que almacenará los 400 números pseudoaleatorios.
        self.n: int = 0 #Tamaño de la muestra (N = 400 números).
        self.k: int = 5 #Número de intervalos en cada dimensión (k = 5 según Coss Bu).
        self.intervalo: float = 1.0 / self.k #Tamaño de cada intervalo (1/5 = 0.2).
        self.pares: List[Tuple[float, float]] = [] #Lista que almacenará los pares consecutivos (399 pares).
        self.frecuencias_obs: np.ndarray = np.zeros((self.k, self.k)) #Matriz 5x5 para frecuencias observadas.
        self.alpha: float = 0.05 #Nivel de significancia para la prueba estadística.
        
    def cargar_numeros_pseudoaleatorios(self, numeros: List[float]) -> None:
        # Carga los números pseudoaleatorios y realiza los cálculos iniciales.
        try:
            self.numeros = numeros #Asigna la lista de 400 números.
            self.n = len(self.numeros) #Actualiza el tamaño de la muestra (N = 400).
            self.intervalo = 1.0 / self.k #Calcula el tamaño del intervalo (0.2).
            self.formar_pares_consecutivos() #Forma los pares consecutivos.
            self.calcular_frecuencias_observadas() #Calcula las frecuencias observadas.
        except Exception as e:
            print(f"Error al cargar los números: {str(e)}")
            raise
    
    def formar_pares_consecutivos(self) -> None:
        # Forma pares consecutivos de números para la prueba.
        # Para cada número en la lista (excepto el último), crea un par con el siguiente número.
        # Esto nos da N-1 pares en total (399 pares).
        self.pares = [(self.numeros[i], self.numeros[i+1]) 
                     for i in range(len(self.numeros)-1)]
        
    def determinar_celda(self, x: float, y: float) -> Tuple[int, int]:
        # Determina la celda de la matriz a la que pertenece un par (x,y).
        # Args:
        #   x (float): Primer número del par.
        #   y (float): Segundo número del par.
        # Returns:
        #   Tuple[int, int]: Índices de la celda en la matriz 5x5.
        celda_x = int(x / self.intervalo) #Calcula la posición horizontal (0-4).
        celda_y = int(y / self.intervalo) #Calcula la posición vertical (0-4).
        if celda_x == self.k: celda_x = self.k - 1 #Ajusta si el número cae en el límite.
        if celda_y == self.k: celda_y = self.k - 1 #Ajusta si el número cae en el límite.
        return celda_x, celda_y
    
    def calcular_frecuencias_observadas(self) -> None:
        # Calcula las frecuencias observadas para cada celda de la matriz 5x5.
        self.frecuencias_obs = np.zeros((self.k, self.k)) #Inicializa matriz de frecuencias.
        for x, y in self.pares: #Para cada par de números.
            celda_x, celda_y = self.determinar_celda(x, y) #Determina su celda.
            self.frecuencias_obs[celda_x][celda_y] += 1 #Incrementa el contador en esa celda.
            
    def calcular_estadistico(self) -> float:
        # Calcula el estadístico chi-cuadrado según la fórmula de Coss Bu.
        # Fórmula: χ² = (k²/(N-1)) * Σ(FO-FE)²
        # Donde:
        # - k = 5 (número de intervalos)
        # - N = 400 (tamaño de la muestra)
        # - FO = frecuencia observada
        # - FE = frecuencia esperada = (N-1)/k²
        fe = (self.n - 1) / (self.k * self.k) #Calcula la frecuencia esperada.
        suma_diferencias = sum(((self.frecuencias_obs[i][j] - fe) ** 2) 
                             for i in range(self.k) for j in range(self.k)) #Suma de diferencias cuadradas.
        chi_cuadrado = (self.k * self.k / (self.n - 1)) * suma_diferencias #Calcula el estadístico.
        return chi_cuadrado
    
    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba con todos los resultados y cálculos.
        reporte = "\n" + "="*80 #Línea separadora.
        reporte += "\nPRUEBA DE SERIES - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "="*80 #Línea separadora.
        
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\n- Hipótesis nula   (H₀) : Los números consecutivos son independientes (no presentan dependencia)."
        reporte += "\n- Hipótesis alter. (H₁) : Los números consecutivos presentan dependencia (no son independientes)."
        
        reporte += "\n\nPARÁMETROS DE LA PRUEBA:"
        reporte += f"\n- Tamaño de muestra      (N) : {self.n}" #Tamaño de la muestra (400 números).
        reporte += f"\n- Número de intervalos   (k) : {self.k}" #Número de intervalos (5).
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}" #Nivel de significancia (0.05).
        reporte += f"\n- Total de pares         (m) : {len(self.pares)}" #Total de pares (399).
        
        fe = (self.n - 1) / (self.k * self.k) #Calcula la frecuencia esperada.
        reporte += "\n\nCÁLCULO DE FRECUENCIAS ESPERADAS:"
        reporte += f"\nFE = (N-1)/k² = ({self.n}-1)/{self.k}² = {fe:.2f}" #Muestra el cálculo.
        
        intervalos = [round((i+1)*self.intervalo, 1) for i in range(self.k)] #Genera los intervalos.
        ancho = 9 #Ancho fijo para alinear columnas.
        
        reporte += "\n\nFrecuencia Observada (FO):"
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos]) #Encabezado de columnas.
        suma_fo = 0 #Contador para la suma de frecuencias observadas.
        for i in range(self.k):
            fila = f"{intervalos[i]:>{ancho}.1f}" #Etiqueta de fila.
            for j in range(self.k):
                valor_fo = int(self.frecuencias_obs[i][j]) #Valor de frecuencia observada.
                suma_fo += valor_fo #Acumula la suma.
                fila += f"{valor_fo:>{ancho}d}" #Agrega el valor a la fila.
            reporte += "\n" + fila #Agrega la fila al reporte.
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos]) #Pie de columnas.
        
        reporte += "\n\nDIFERENCIA ENTRE LA FRECUENCIA OBSERVADA Y ESPERADA:"
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos]) #Encabezado de columnas.
        suma_diferencias = 0 #Contador para la suma de diferencias.
        terminos_diff = [] #Lista para almacenar los términos de la suma.
        for i in range(self.k):
            fila = f"{intervalos[i]:>{ancho}.1f}" #Etiqueta de fila.
            for j in range(self.k):
                diferencia_cuadrada = (self.frecuencias_obs[i][j] - fe) ** 2 #Calcula la diferencia cuadrada.
                suma_diferencias += diferencia_cuadrada #Acumula la suma.
                terminos_diff.append(f"({int(self.frecuencias_obs[i][j])}-{fe:.2f})²={diferencia_cuadrada:.4f}") #Guarda el término.
                fila += f"{diferencia_cuadrada:>{ancho}.4f}" #Agrega el valor a la fila.
            reporte += "\n" + fila #Agrega la fila al reporte.
        reporte += "\n" + " "*ancho + "".join([f"{x:>{ancho}.1f}" for x in intervalos]) #Pie de columnas.
        
        reporte += "\n\nCÁLCULO DE LA SUMA DE DIFERENCIAS CUADRADAS:"
        reporte += "\nSuma = " + " + ".join(terminos_diff) #Muestra los términos.
        reporte += f"\nSuma = {suma_diferencias:.5f}" #Muestra la suma total.
        
        chi_cuadrado = self.calcular_estadistico() #Calcula el estadístico chi-cuadrado.
        gl = (self.k - 1) ** 2 #Calcula los grados de libertad (16).
        valor_critico = chi2.ppf(0.95, gl) #Obtiene el valor crítico.
        
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO CHI-CUADRADA:"
        reporte += "\nχ² = (k²/(N-1)) * Σ(FO-FE)²" #Fórmula del estadístico.
        reporte += f"\nχ² = ({self.k}²/{self.n-1}) * Σ(FO-{fe:.2f})²" #Sustitución de valores.
        reporte += f"\nχ² = {chi_cuadrado:.5f}" #Resultado final.
        
        reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
        reporte += f"\nGrados de libertad = (k-1)² = ({self.k}-1)² = {gl}" #Cálculo de grados de libertad.
        reporte += f"\nValor crítico χ²(α={self.alpha}, gl={gl}) = {valor_critico:.5f}" #Valor crítico.
        
        reporte += "\n\nDECISIÓN:"
        if chi_cuadrado > valor_critico: #Compara el estadístico con el valor crítico.
            reporte += f"\nComo χ² = {chi_cuadrado:.5f} > {valor_critico:.5f}" #Muestra la comparación.
            reporte += "\nSe rechaza H₀: Los números consecutivos son dependientes (presentan dependencia)."
            reporte += "\nConclusión: Existe evidencia de dependencia entre números consecutivos."
        else:
            reporte += f"\nComo χ² = {chi_cuadrado:.5f} ≤ {valor_critico:.5f}" #Muestra la comparación.
            reporte += "\nNo se rechaza H₀: Los números consecutivos son independientes (no presentan dependencia)."
            reporte += "\nConclusión: No hay evidencia suficiente de dependencia entre números consecutivos."
        
        reporte += "\n" + "="*80 #Línea separadora.
        return reporte #Retorna el reporte formateado.
    
    def realizar_prueba(self, numeros: List[float]) -> None:
        # Ejecuta la prueba completa de series.
        self.cargar_numeros_pseudoaleatorios(numeros) #Carga los números.
        self.formar_pares_consecutivos() #Forma los pares.
        self.calcular_frecuencias_observadas() #Calcula frecuencias.
        print(self.generar_reporte()) #Genera y muestra el reporte.

if __name__ == "__main__":
    # Crear y ejecutar la prueba con los 400 números proporcionados.
    prueba = PruebaSeries()
    prueba.realizar_prueba(numeros) 