# Importamos la función chi2 para calcular valores críticos de la distribución chi-cuadrada.
from scipy.stats import chi2  # Para obtener valores críticos de χ².
# Importamos herramientas para definir tipos de datos que usaremos en el código.
from typing import List, Dict, Union  # Para indicar tipos de listas, diccionarios y uniones de tipos
# Importamos Counter para contar frecuencias de dígitos en cada número.
from collections import Counter  # Para contar apariciones de cada dígito.

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

class PruebaPoker:
    # Implementa la Prueba de Póker para validar números pseudoaleatorios.
    # Analiza los primeros cinco dígitos decimales de cada número y clasifica en categorías de póker.
    # Luego calcula el estadístico chi-cuadrada comparando frecuencias observadas y esperadas.
    
    def __init__(self):
        # Inicializa la prueba de póker con los parámetros necesarios.
        self.numeros: List[float] = []
        self.n: int = 0
        self.probabilidades: Dict[str, float] = {
            "Todos diferentes": 0.3024,
            "Un par":           0.5040,
            "Dos pares":        0.1080,
            "Tercia":           0.0720,
            "Full":             0.0090,
            "Póker":            0.0045,
            "Quintilla":        0.0001
        }
        self.frecuencias_obs: Dict[str, int] = {cat: 0 for cat in self.probabilidades}
        self.frecuencias_esperadas: Dict[str, float] = {}
        self.alpha: float = 0.05
        self.categorias_combinadas: Dict[str, Dict[str, Union[float, int]]] = {}
        self.estadistico_chi: float = 0.0
        self.valor_critico: float = 0.0
        self.decision: str = ""

    def clasificar(self, numero: float) -> str:
        # Clasifica un número en una categoría de póker basado en sus 5 dígitos decimales.
        cadena = f"{numero:.5f}"[2:7]
        conteo = Counter(cadena)
        frecuencias = sorted(conteo.values(), reverse=True)
        
        patrones = {
            (5,):             "Quintilla",
            (4, 1):           "Póker",
            (3, 2):           "Full",
            (3, 1, 1):        "Tercia",
            (2, 2, 1):        "Dos pares",
            (2, 1, 1, 1):     "Un par",
            (1, 1, 1, 1, 1):  "Todos diferentes"
        }
        
        return patrones.get(tuple(frecuencias), "Todos diferentes")

    def calcular_frecuencias_observadas(self) -> None:
        # Calcula las frecuencias observadas para cada categoría de póker.
        self.frecuencias_obs = {cat: 0 for cat in self.probabilidades}
        for numero in self.numeros:
            categoria = self.clasificar(numero)
            self.frecuencias_obs[categoria] += 1

    def calcular_frecuencias_esperadas(self) -> None:
        # Calcula las frecuencias esperadas multiplicando probabilidad por tamaño de muestra.
        self.frecuencias_esperadas = {
            cat: prob * self.n
            for cat, prob in self.probabilidades.items()
        }

    def combinar_categorías(self) -> None:
        # Combina categorías de baja frecuencia en una sola categoría.
        self.categorias_combinadas = {}
        
        for cat in ["Todos diferentes", "Un par", "Dos pares", "Tercia"]:
            self.categorias_combinadas[cat] = {
                "observada": self.frecuencias_obs[cat],
                "esperada":  self.frecuencias_esperadas[cat]
            }
        
        suma_obs = (
            self.frecuencias_obs["Full"] +
            self.frecuencias_obs["Póker"] +
            self.frecuencias_obs["Quintilla"]
        )
        
        suma_esp = (
            self.frecuencias_esperadas["Full"] +
            self.frecuencias_esperadas["Póker"] +
            self.frecuencias_esperadas["Quintilla"]
        )
        
        self.categorias_combinadas["Full+Póker+Quintilla"] = {
            "observada": suma_obs,
            "esperada":  suma_esp
        }

    def calcular_chi_cuadrada(self) -> None:
        # Calcula el estadístico χ² sumando las contribuciones de cada categoría.
        chi_sum = 0.0
        for frec in self.categorias_combinadas.values():
            oi = frec["observada"]
            ei = frec["esperada"]
            if ei > 0:
                chi_sum += (oi - ei) ** 2 / ei
        self.estadistico_chi = chi_sum

    def obtener_valor_critico(self) -> None:
        # Calcula el valor crítico de la distribución χ² para α y grados de libertad.
        gl = len(self.categorias_combinadas) - 1
        self.valor_critico = chi2.ppf(1 - self.alpha, df=gl)

    def tomar_decision(self) -> None:
        # Toma la decisión final comparando χ² calculado con χ² crítico.
        if self.estadistico_chi <= self.valor_critico:
            self.decision = "No se rechaza H₀: Los números provienen de una distribución uniforme."
        else:
            self.decision = "Se rechaza H₀: Los números no provienen de una distribución uniforme."

    def _validar_entradas(self) -> None:
        # Valida que los parámetros de entrada sean correctos.
        if not (0 < self.alpha < 1):
            raise ValueError("El nivel de significancia (alpha) debe estar entre 0 y 1.")
        if self.n == 0:
            raise ValueError("La lista de números pseudoaleatorios no puede estar vacía.")
        if not all(0 <= x <= 1 for x in self.numeros):
            raise ValueError("Los números pseudoaleatorios deben estar entre 0 y 1.")

    def _verificar_frecuencias_esperadas(self) -> bool:
        # Verifica que todas las frecuencias esperadas sean ≥ 5.
        return all(frec >= 5 for frec in self.frecuencias_esperadas.values())

    def generar_reporte(self) -> str:
        # Genera un reporte detallado de la prueba del póker.
        reporte = "\n" + "=" * 80 
        reporte += "\nPRUEBA DE PÓKER - VALIDACIÓN DE NÚMEROS PSEUDOALEATORIOS"
        reporte += "\n" + "=" * 80
    
        reporte += "\n\nHIPÓTESIS:"
        reporte += "\n- Hipótesis nula   (H₀) : Los números consecutivos son independientes y uniformemente distribuidos."
        reporte += "\n- Hipótesis alter. (H₁) : Los números consecutivos no son independientes o no uniformemente distribuidos."
    
        reporte += "\n\nPARÁMETROS:"
        reporte += f"\n- Nivel de significancia (α) : {self.alpha}"
        reporte += f"\n- Tamaño de la muestra      (N) : {self.n}"
        reporte += f"\n- Grados de libertad         : {len(self.categorias_combinadas) - 1}"
    
        reporte += "\n\nFRECUENCIAS OBSERVADAS Y ESPERADAS:"
        reporte += "\n" + "-" * 80
        reporte += "\n" + f"{'Categoría':<25}{'Observada (FO)':<15}{'Esperada (FE)':<15}{'(FO-FE)²/FE':<15}"
        reporte += "\n" + "-" * 80
    
        for categoria, frecs in self.categorias_combinadas.items():
            oi = frecs["observada"]
            ei = frecs["esperada"]
            diferencia = (oi - ei) ** 2 / ei if ei > 1e-9 else 0
            reporte += "\n" + f"{categoria:<25}{oi:<15}{ei:<15.4f}{diferencia:<15.4f}"
    
        reporte += "\n\nCÁLCULO DEL ESTADÍSTICO CHI-CUADRADA:"
        reporte += "\nχ² = Σ (FOi - FEi)² / FEi"
        reporte += "\nContribución de cada categoría:"
    
        for categoria, frecs in self.categorias_combinadas.items():
            oi = frecs["observada"]
            ei = frecs["esperada"]
            contribucion = (oi - ei) ** 2 / ei if ei > 1e-9 else 0
            reporte += "\n" + f"{categoria}: ({oi} - {ei:.4f})²/{ei:.4f} = {contribucion:.4f}"
        reporte += "\n" + f"\nχ² calculado = {self.estadistico_chi:.9f}"
    
        gl = len(self.categorias_combinadas) - 1
        reporte += "\n\nCÁLCULO DEL VALOR CRÍTICO:"
        reporte += "\n" + f"Grados de libertad = (número de categorías - 1) = {gl}"
        reporte += "\n" + f"Valor crítico χ²(α={self.alpha}, gl={gl}) = {self.valor_critico:.9f}"
    
        reporte += "\n\nDECISIÓN:"
        if self.estadistico_chi <= self.valor_critico:
            reporte += "\n" + f"Como χ² = {self.estadistico_chi:.9f} ≤ {self.valor_critico:.9f}"
            reporte += "\nNo se rechaza H₀: Los números son independientes y uniformemente distribuidos."
        else:
            reporte += "\n" + f"Como χ² = {self.estadistico_chi:.9f} > {self.valor_critico:.9f}"
            reporte += "\nSe rechaza H₀: Los números no son independientes o no uniformemente distribuidos."
    
        reporte += "\n" + "=" * 80 
        return reporte

    def realizar_prueba(self, numeros: List[float]) -> None:
        # Ejecuta el flujo completo de la prueba del póker.
        self.numeros = numeros
        self.n = len(self.numeros)
        self._validar_entradas()
        
        self.calcular_frecuencias_observadas()
        self.calcular_frecuencias_esperadas()
        
        if not self._verificar_frecuencias_esperadas():
            print("ADVERTENCIA: Algunas frecuencias esperadas son < 5")
        
        self.combinar_categorías()
        self.calcular_chi_cuadrada()
        self.obtener_valor_critico()
        self.tomar_decision()
        print(self.generar_reporte())

# Bloque principal: ejecuta la prueba cuando el script se corre directamente.
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
        
        # Crear y ejecutar la prueba de póker.
        prueba = PruebaPoker()
        prueba.realizar_prueba(numeros)
