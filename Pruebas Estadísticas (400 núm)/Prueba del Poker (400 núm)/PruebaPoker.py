# Importamos la función chi2 para calcular valores críticos de la distribución chi-cuadrada.
from scipy.stats import chi2 #Para obtener valores críticos de χ² con nivel de significancia α.
# Importamos herramientas para definir tipos de datos que usaremos en el código.
from typing import List, Dict, Union #Para indicar tipos de listas, diccionarios y uniones de tipos.
# Importamos Counter para contar frecuencias de dígitos en cada número.
from collections import Counter #Para contar apariciones de cada dígito en los números.

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

class PruebaPoker:
    def __init__(self):
        # Inicializa la prueba de póker con los parámetros necesarios.
        self.numeros: List[float] = [] #Lista que almacenará los 400 números pseudoaleatorios.
        self.n: int = 0 #Tamaño de la muestra (N = 400 números).
        self.probabilidades: Dict[str, float] = {
            "Todos diferentes": 0.3024, #Probabilidad teórica de que los 5 dígitos sean diferentes.
            "Un par":           0.5040, #Probabilidad teórica de tener exactamente un par.
            "Dos pares":        0.1080, #Probabilidad teórica de tener dos pares diferentes.
            "Tercia":           0.0720, #Probabilidad teórica de tener tres dígitos iguales.
            "Full":             0.0090, #Probabilidad teórica de tener una tercia y un par.
            "Póker":            0.0045, #Probabilidad teórica de tener cuatro dígitos iguales.
            "Quintilla":        0.0001  #Probabilidad teórica de tener los cinco dígitos iguales.
        }
        self.frecuencias_obs: Dict[str, int] = {cat: 0 for cat in self.probabilidades} #Diccionario para frecuencias observadas.
        self.frecuencias_esperadas: Dict[str, float] = {} #Diccionario para frecuencias esperadas.
        self.alpha: float = 0.05 #Nivel de significancia para la prueba estadística.
        self.categorias_combinadas: Dict[str, Dict[str, Union[float, int]]] = {} #Diccionario para categorías combinadas.
        self.estadistico_chi: float = 0.0 #Valor del estadístico chi-cuadrado calculado.
        self.valor_critico: float = 0.0 #Valor crítico de la distribución chi-cuadrado.
        self.decision: str = "" #Decisión final de la prueba.

    def clasificar(self, numero: float) -> str:
        # Clasifica un número en una categoría de póker basado en sus 5 dígitos decimales.
        cadena = f"{numero:.5f}"[2:7] #Obtiene los 5 dígitos decimales del número.
        conteo = Counter(cadena) #Cuenta la frecuencia de cada dígito.
        frecuencias = sorted(conteo.values(), reverse=True) #Ordena las frecuencias de mayor a menor.
        
        patrones = {
            (5,):             "Quintilla", #Todos los dígitos son iguales.
            (4, 1):           "Póker", #Cuatro dígitos iguales y uno diferente.
            (3, 2):           "Full", #Tres dígitos iguales y dos iguales.
            (3, 1, 1):        "Tercia", #Tres dígitos iguales y dos diferentes.
            (2, 2, 1):        "Dos pares", #Dos pares de dígitos iguales y uno diferente.
            (2, 1, 1, 1):     "Un par", #Un par de dígitos iguales y tres diferentes.
            (1, 1, 1, 1, 1):  "Todos diferentes" #Todos los dígitos son diferentes.
        }
        
        return patrones.get(tuple(frecuencias), "Todos diferentes") #Retorna la categoría correspondiente.

    def calcular_frecuencias_observadas(self) -> None:
        # Calcula las frecuencias observadas para cada categoría de póker.
        self.frecuencias_obs = {cat: 0 for cat in self.probabilidades} #Inicializa contadores en cero.
        for numero in self.numeros: #Para cada número en la muestra.
            categoria = self.clasificar(numero) #Clasifica el número.
            self.frecuencias_obs[categoria] += 1 #Incrementa el contador de la categoría.

    def calcular_frecuencias_esperadas(self) -> None:
        # Calcula las frecuencias esperadas multiplicando probabilidad por tamaño de muestra.
        self.frecuencias_esperadas = {
            cat: prob * self.n #FE = P * N, donde P es la probabilidad teórica y N es el tamaño de la muestra.
            for cat, prob in self.probabilidades.items()
        }

    def combinar_categorías(self) -> None:
        # Combina categorías de baja frecuencia en una sola categoría.
        self.categorias_combinadas = {} #Inicializa el diccionario de categorías combinadas.
        
        for cat in ["Todos diferentes", "Un par", "Dos pares", "Tercia"]: #Categorías que se mantienen separadas.
            self.categorias_combinadas[cat] = {
                "observada": self.frecuencias_obs[cat], #Frecuencia observada de la categoría.
                "esperada":  self.frecuencias_esperadas[cat] #Frecuencia esperada de la categoría.
            }
        
        # Suma las frecuencias observadas de las categorías de baja frecuencia.
        suma_obs = (
            self.frecuencias_obs["Full"] +
            self.frecuencias_obs["Póker"] +
            self.frecuencias_obs["Quintilla"]
        )
        
        # Suma las frecuencias esperadas de las categorías de baja frecuencia.
        suma_esp = (
            self.frecuencias_esperadas["Full"] +
            self.frecuencias_esperadas["Póker"] +
            self.frecuencias_esperadas["Quintilla"]
        )
        
        # Crea una nueva categoría combinada.
        self.categorias_combinadas["Full+Póker+Quintilla"] = {
            "observada": suma_obs, #Frecuencia observada combinada.
            "esperada":  suma_esp  #Frecuencia esperada combinada.
        }

    def calcular_chi_cuadrada(self) -> None:
        # Calcula el estadístico χ² sumando las contribuciones de cada categoría.
        chi_sum = 0.0 #Inicializa la suma del estadístico.
        for frec in self.categorias_combinadas.values(): #Para cada categoría.
            oi = frec["observada"] #Frecuencia observada.
            ei = frec["esperada"] #Frecuencia esperada.
            if ei > 0: #Evita división por cero.
                chi_sum += (oi - ei) ** 2 / ei #Suma la contribución de la categoría al estadístico.
        self.estadistico_chi = chi_sum #Guarda el valor del estadístico.

    def obtener_valor_critico(self) -> None:
        # Calcula el valor crítico de la distribución χ² para α y grados de libertad.
        gl = len(self.categorias_combinadas) - 1 #Grados de libertad = número de categorías - 1.
        self.valor_critico = chi2.ppf(1 - self.alpha, df=gl) #Obtiene el valor crítico.

    def tomar_decision(self) -> None:
        # Toma la decisión final comparando χ² calculado con χ² crítico.
        if self.estadistico_chi <= self.valor_critico: #Si el estadístico es menor o igual al valor crítico.
            self.decision = "No se rechaza H₀: Los números provienen de una distribución uniforme." #No se rechaza la hipótesis nula.
        else: #Si el estadístico es mayor al valor crítico.
            self.decision = "Se rechaza H₀: Los números no provienen de una distribución uniforme." #Se rechaza la hipótesis nula.

    def _validar_entradas(self) -> None:
        # Valida que los parámetros de entrada sean correctos.
        if not (0 < self.alpha < 1): #Verifica que el nivel de significancia esté entre 0 y 1.
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1.")
        if self.n == 0: #Verifica que la lista de números no esté vacía.
            raise ValueError("La lista de números pseudoaleatorios no puede estar vacía.")
        if not all(0 <= x <= 1 for x in self.numeros): #Verifica que todos los números estén entre 0 y 1.
            raise ValueError("Los números pseudoaleatorios deben estar entre 0 y 1.")

    def _verificar_frecuencias_esperadas(self) -> bool:
        # Verifica que todas las frecuencias esperadas sean ≥ 5.
        return all(frec >= 5 for frec in self.frecuencias_esperadas.values()) #Retorna True si todas las frecuencias son ≥ 5.

    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba del póker.
        reporte = "\n" + "=" * 80 #Línea separadora.
        reporte += "\nPRUEBA DE PÓKER - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "=" * 80 #Línea separadora.
    
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\n- Hipótesis nula   (H₀) : Los números consecutivos son independientes y uniformemente distribuidos."
        reporte += "\n- Hipótesis alter. (H₁) : Los números consecutivos no son independientes o no uniformemente distribuidos."
    
        reporte += "\n\nPARÁMETROS:"
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}" #Nivel de significancia (0.05).
        reporte += f"\n- Tamaño de la muestra      (N) : {self.n}" #Tamaño de la muestra (400).
        reporte += f"\n- Grados de libertad         : {len(self.categorias_combinadas) - 1}" #Grados de libertad.
    
        reporte += "\n\nFRECUENCIAS OBSERVADAS Y ESPERADAS:"
        reporte += "\n" + "-" * 80 #Línea separadora.
        reporte += "\n" + f"{'Categoría':<25}{'Observada (FO)':<15}{'Esperada (FE)':<15}{'(FO-FE)²/FE':<15}" #Encabezado de columnas.
        reporte += "\n" + "-" * 80 #Línea separadora.
    
        for categoria, frecs in self.categorias_combinadas.items(): #Para cada categoría.
            oi = frecs["observada"] #Frecuencia observada.
            ei = frecs["esperada"] #Frecuencia esperada.
            diferencia = (oi - ei) ** 2 / ei if ei > 1e-9 else 0 #Calcula la contribución al estadístico.
            reporte += "\n" + f"{categoria:<25}{oi:<15}{ei:<15.4f}{diferencia:<15.4f}" #Agrega la fila al reporte.
    
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO CHI-CUADRADA:"
        reporte += "\nχ² = Σ (FOi - FEi)² / FEi" #Fórmula del estadístico.
        reporte += "\nContribución de cada categoría:" #Título de la sección.
    
        for categoria, frecs in self.categorias_combinadas.items(): #Para cada categoría.
            oi = frecs["observada"] #Frecuencia observada.
            ei = frecs["esperada"] #Frecuencia esperada.
            contribucion = (oi - ei) ** 2 / ei if ei > 1e-9 else 0 #Calcula la contribución.
            reporte += "\n" + f"{categoria}: ({oi} - {ei:.4f})²/{ei:.4f} = {contribucion:.4f}" #Muestra el cálculo.
        reporte += "\n" + f"\nχ² calculado = {self.estadistico_chi:.9f}" #Muestra el estadístico final.
    
        gl = len(self.categorias_combinadas) - 1 #Calcula los grados de libertad.
        reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
        reporte += "\n" + f"Grados de libertad = (número de categorías - 1) = {gl}" #Muestra los grados de libertad.
        reporte += "\n" + f"Valor crítico χ²(α={self.alpha}, gl={gl}) = {self.valor_critico:.9f}" #Muestra el valor crítico.
    
        reporte += "\n\nDECISIÓN:"
        if self.estadistico_chi <= self.valor_critico: #Si no se rechaza H₀.
            reporte += "\n" + f"Como χ² = {self.estadistico_chi:.9f} ≤ {self.valor_critico:.9f}" #Muestra la comparación.
            reporte += "\nNo se rechaza H₀: Los números son independientes y uniformemente distribuidos." #Muestra la decisión.
        else: #Si se rechaza H₀.
            reporte += "\n" + f"Como χ² = {self.estadistico_chi:.9f} > {self.valor_critico:.9f}" #Muestra la comparación.
            reporte += "\nSe rechaza H₀: Los números no son independientes o no uniformemente distribuidos." #Muestra la decisión.
    
        reporte += "\n" + "=" * 80 #Línea separadora.
        return reporte #Retorna el reporte formateado.

    def realizar_prueba(self, numeros: List[float]) -> None:
        # Ejecuta el flujo completo de la prueba del póker.
        self.numeros = numeros #Asigna la lista de números.
        self.n = len(self.numeros) #Actualiza el tamaño de la muestra.
        self._validar_entradas() #Valida los parámetros de entrada.
        
        self.calcular_frecuencias_observadas() #Calcula frecuencias observadas.
        self.calcular_frecuencias_esperadas() #Calcula frecuencias esperadas.
        
        if not self._verificar_frecuencias_esperadas(): #Verifica frecuencias esperadas.
            print("ADVERTENCIA: Algunas frecuencias esperadas son < 5") #Muestra advertencia si es necesario.
        
        self.combinar_categorías() #Combina categorías de baja frecuencia.
        self.calcular_chi_cuadrada() #Calcula el estadístico chi-cuadrado.
        self.obtener_valor_critico() #Obtiene el valor crítico.
        self.tomar_decision() #Toma la decisión final.
        print(self.generar_reporte()) #Genera y muestra el reporte.

if __name__ == "__main__":
    # Crear y ejecutar la prueba con los 400 números proporcionados.
    prueba = PruebaPoker()
    prueba.realizar_prueba(numeros)
