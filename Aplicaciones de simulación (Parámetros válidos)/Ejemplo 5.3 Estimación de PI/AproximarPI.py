import math  # Importamos math para operaciones matemáticas como raíz cuadrada.
import random  # Importamos random para generación de números aleatorios.
from typing import List, Tuple  # Importamos tipos para mejor documentación del código.
from dataclasses import dataclass  # Importamos dataclass para crear clases de datos.

class GCM:  # Clase para el Generador Congruencial Multiplicativo.
    def __init__(self, m: int = 32057, X0: int = 20855, a: int = 9600):  # Constructor con parámetros por defecto.
        self.m = m  # Módulo del GCM (32057).
        self.X0 = X0  # Semilla inicial (20855).
        self.a = a  # Multiplicador (9600).
        self.Xn = X0  # Valor actual del generador.
        self.numeros = []  # Lista para almacenar todos los números generados.
        self._generar_hasta_periodo()  # Generamos todos los números al inicializar.
    
    def _generar_hasta_periodo(self) -> None:  # Método privado para generar números hasta el período completo.
        self.Xn = self.X0  # Reiniciamos el generador a la semilla inicial.
        self.numeros = [self.X0]  # Incluimos X0 en la lista de números.
        numeros_generados = set([self.X0])  # Conjunto para detectar ciclos.
        
        while True:  # Bucle hasta encontrar un ciclo.
            self.Xn = (self.a * self.Xn) % self.m  # Fórmula del GCM: Xn+1 = (a*Xn) mod m.
            if self.Xn in numeros_generados:  # Si el número ya existe, hemos encontrado un ciclo.
                break
            numeros_generados.add(self.Xn)  # Agregamos el número al conjunto de control.
            self.numeros.append(self.Xn)  # Agregamos el número a la lista.
        
        print(f"\nVerificación del GCM:")  # Imprimimos información de verificación.
        print(f"Parámetros: m={self.m}, X0={self.X0}, a={self.a}")  # Mostramos los parámetros usados.
        print(f"Números generados: {len(self.numeros)}")  # Total de números generados.
        print(f"Deberían ser: {self.m}")  # Número esperado de números.
        print(f"¿Se generaron todos?: {'Sí' if len(self.numeros) == self.m else 'No'}")  # Verificación de completitud.
        print(f"Números únicos generados: {len(numeros_generados)}")  # Cantidad de números únicos.
        print(f"Período del GCM: {len(self.numeros)}")  # Longitud del período.
    
    def generar_numero_aleatorio(self) -> float:  # Método para generar un número aleatorio normalizado.
        if not self.numeros:  # Si no hay números generados.
            self._generar_hasta_periodo()  # Los generamos.
        return self.numeros.pop(0) / self.m  # Retornamos el siguiente número normalizado.

@dataclass
class ConfiguracionSimulacion:  # Clase para almacenar la configuración de la simulación.
    def __init__(self, epsilon: float = 0.0001, nivel_confianza: float = 0.95):  # Constructor con valores por defecto.
        self.epsilon = epsilon  # Error máximo permitido.
        self.nivel_confianza = nivel_confianza  # Nivel de confianza deseado.
        self.Z_alpha_2 = 1.96  # Valor crítico para 95% de confianza.

class SimulacionPI:  # Clase principal de la simulación.
    def __init__(self, config: ConfiguracionSimulacion):  # Constructor con la configuración.
        self.config = config  # Guardamos la configuración.
        self.gcm = GCM(m=32057, X0=20855, a=9600)  # Inicializamos el GCM con parámetros óptimos.
        self.numeros = self.gcm.numeros  # Obtenemos la lista de números generados.
        self.indice_actual = 0  # Índice para recorrer la lista de números.
        self.puntos_dentro = 0  # Contador de puntos dentro del círculo (x).
        self.puntos_totales = 0  # Contador de puntos totales (n).
        self.estimacion_pi = 0  # Estimación actual de π.
        self.error_actual = float('inf')  # Error actual.
        self.iteraciones = []  # Lista para almacenar las iteraciones.
        
        # Calculamos el número de pares disponibles (período completo)
        self.num_pares = len(self.numeros) // 2  # Número de pares de números disponibles.
        print(f"\nNúmero de pares disponibles (período completo): {self.num_pares}")
        
        # Calculamos el tamaño muestral mínimo según la fórmula de Coss Bu.
        self.tamano_muestra = self._calcular_tamano_muestra()
        print(f"Tamaño muestral mínimo (ε={self.config.epsilon}, {self.config.nivel_confianza*100}% conf): n ≥ {self.tamano_muestra}")
        print(f"Usaremos todos los pares disponibles del GCM para mayor precisión.")

    def _calcular_tamano_muestra(self) -> int:  # Método para calcular el tamaño muestral mínimo.
        # Usamos la fórmula: n ≥ (4π(1 - π/4) * Z_α/2²) / ε²
        pi_aprox = math.pi  # Usamos π real para mejor precisión.
        p = pi_aprox / 4  # Probabilidad teórica.
        varianza = p * (1 - p)  # Varianza de la distribución.
        n = (4 * varianza * self.config.Z_alpha_2**2) / (self.config.epsilon**2)
        return math.ceil(n)  # Redondeamos hacia arriba.

    def simular_punto(self) -> Tuple[float, float]:  # Método para simular un punto aleatorio.
        if self.indice_actual + 2 > len(self.numeros):  # Si no hay suficientes números.
            self.indice_actual = 0  # Reiniciamos el índice.
            
        R1 = self.numeros[self.indice_actual] / self.gcm.m  # Primer número aleatorio uniforme.
        self.indice_actual += 1  # Avanzamos el índice.
        R2 = self.numeros[self.indice_actual] / self.gcm.m  # Segundo número aleatorio uniforme.
        self.indice_actual += 1  # Avanzamos el índice.
        
        return R1, R2  # Retornamos los números aleatorios uniformes.

    def ejecutar_simulacion(self) -> None:  # Método para ejecutar la simulación completa.
        print("\nIniciando simulación de Monte Carlo para aproximar π...")
        print("\n" + " " * 40 + "Tabla de iteraciones")
        print("i\tR1\t\tR2\t\tD=√(R1²+R2²)\t¿D < 1?")
        print("-" * 80)
        
        for i in range(1, self.num_pares + 1):  # Iteramos hasta usar todos los pares disponibles del período.
            R1, R2 = self.simular_punto()  # Generamos dos números aleatorios uniformes.
            # Calculamos la distancia usando la fórmula: d = √(R₁² + R₂²)
            distancia = math.sqrt(R1**2 + R2**2)  # Donde R₁ y R₂ son números aleatorios uniformes en [0,1].
            esta_dentro = distancia <= 1  # Verificamos si está dentro del círculo.
            
            if esta_dentro:  # Si está dentro del círculo.
                self.puntos_dentro += 1  # Incrementamos el contador x.
            
            self.puntos_totales += 1  # Incrementamos el contador n.
            
            # Guardamos la iteración.
            self.iteraciones.append({
                'i': i,
                'R1': R1,
                'R2': R2,
                'distancia': distancia,
                'esta_dentro': esta_dentro
            })
            
            # Imprimimos la iteración con formato alineado.
            print(f"{i}\t{R1:.5f}\t\t{R2:.5f}\t\t{distancia:.9f}\t{'Sí' if esta_dentro else 'No'}")
        
        # Imprimimos los encabezados nuevamente al final de las iteraciones.
        print("-" * 80)
        print("i\tR1\t\tR2\t\tD=√(R1²+R2²)\t¿D < 1?")
        
        self._generar_reporte()  # Generamos el reporte final.

    def _generar_reporte(self) -> None:  # Método para generar el reporte final.
        # Calculamos la aproximación de π usando la fórmula π^ = 4 * (x/n)
        self.estimacion_pi = 4 * (self.puntos_dentro / self.puntos_totales)
        
        # Calculamos el intervalo de confianza según Coss Bu
        p = math.pi / 4  # Probabilidad teórica.
        error_std = math.sqrt(4 * p * (1 - p) / self.puntos_totales)
        ic_inf = self.estimacion_pi - self.config.Z_alpha_2 * error_std
        ic_sup = self.estimacion_pi + self.config.Z_alpha_2 * error_std
        
        error_absoluto = abs(self.estimacion_pi - math.pi)
        error_relativo = (error_absoluto / math.pi) * 100
        
        print("\n" + " " * 30 + "Tabla de resultados")
        print("=" * 60)
        print(f"Acumulación (x):\t{self.puntos_dentro}")
        print(f"Total (i):\t\t{self.puntos_totales}")
        print(f"Estimación de π:\t{self.estimacion_pi:.6f}")
        print(f"Intervalo 95%:\t\t[{ic_inf:.6f}, {ic_sup:.6f}]")
        print(f"Error absoluto:\t\t{error_absoluto:.6f}")
        print(f"Error relativo:\t\t{error_relativo:.6f}%")
        print("=" * 60)
        
        print("\nParámetros del Generador Congruencial Multiplicativo (GCM)")
        print("=" * 60)
        print(f"Módulo (m): {self.gcm.m}")
        print(f"Semilla (X₀): {self.gcm.X0}")
        print(f"Multiplicador (a): {self.gcm.a}")
        print(f"Período del GCM: {len(self.numeros)}")
        print("=" * 60)

def main():  # Función principal.
    config = ConfiguracionSimulacion(  # Creamos la configuración.
        epsilon=0.0001,  # Error máximo permitido.
        nivel_confianza=0.95  # Nivel de confianza deseado.
    )
    
    simulacion = SimulacionPI(config)  # Creamos la simulación.
    simulacion.ejecutar_simulacion()  # Ejecutamos la simulación.

if __name__ == "__main__":  # Punto de entrada del programa.
    main()  # Llamamos a la función principal. 