import math  # Importa el módulo math para operaciones matemáticas.
import random  # Importa el módulo random para generación de números aleatorios.
from typing import List  # Importa List para tipado de listas.

class GCM_Primos:
    def __init__(self, m: int = 32057, X0: int = 20855, a: int = 9600):
        # Constructor del Generador Congruencial Multiplicativo con parámetros fijos.
        self.m = m  # Módulo del GCM, valor primo que determina el período máximo del generador.
        self.X0 = X0  # Semilla inicial, valor de inicio para la generación de números pseudoaleatorios.
        self.a = a  # Multiplicador, constante que determina la secuencia de números generados.
        self.periodo = self.m - 1  # Período teórico del generador, igual a m-1 para un GCM con m primo.
        self._X = self.X0  # Valor actual de la secuencia, inicializado con la semilla X0.

    def imprimir_parametros(self) -> None:
        # Muestra en pantalla los parámetros fundamentales del generador.
        print(f"=== Parámetros del GCM ===")  # Encabezado para la sección de parámetros.
        print(f"Valor para 'm' (módulo)           : {self.m}")  # Muestra el valor del módulo m.
        print(f"Valor para 'X0' (semilla inicial) : {self.X0}")  # Muestra el valor de la semilla inicial.
        print(f"Valor para 'a' (multiplicador)    : {self.a}")  # Muestra el valor del multiplicador.
        print(f"Período teórico                   : {self.periodo}")  # Muestra el período teórico del generador.
        print()  # Línea en blanco para mejor legibilidad.

    def _siguiente_valor_xn(self, xi: int) -> int:
        # Calcula el siguiente valor en la secuencia usando la fórmula X_{n+1} = (a * X_n) mod m.
        return (self.a * xi) % self.m  # Aplica la fórmula del GCM: Xn+1 = (a * Xn) mod m.

    def generar_numero_aleatorio(self) -> float:
        # Avanza la secuencia en una iteración y devuelve el valor uniforme en el intervalo [0,1).
        self._X = self._siguiente_valor_xn(self._X)  # Genera el siguiente valor en la secuencia.
        return self._X / self.m  # Convierte el valor a un número uniforme en [0,1) dividiendo entre m.

    def imprimir_todas_iteraciones(self) -> None:
        # Imprime todas las iteraciones del generador con su número uniforme correspondiente.
        print(f"=== Todas las iteraciones del GCM ===")  # Encabezado para la sección de iteraciones.
        
        numeros_generados = []  # Lista para almacenar todos los números generados en el período.
        
        xi = self.X0  # Inicializa xi con la semilla inicial.
        numeros_generados.append(xi)  # Almacena la semilla inicial en la lista.
        print(f"Iteración = 0 | Núm. uniforme = {xi/self.m:.5f}")  # Muestra la semilla inicial y su valor uniforme.
        
        for i in range(1, self.periodo + 1):  # Itera desde 1 hasta el período teórico.
            xi = self._siguiente_valor_xn(xi)  # Genera el siguiente valor en la secuencia.
            uniforme = xi / self.m  # Calcula el número uniforme correspondiente.
            numeros_generados.append(xi)  # Almacena el número generado en la lista.
            print(f"Iteración = {i} | Núm. uniforme = {uniforme:.5f}")  # Muestra la iteración y su número uniforme.
            
            if xi == self.X0:  # Verifica si se ha completado el período (la semilla reaparece).
                print(f"\nSemilla X0 reapareció en iteración {i}, período = {i}")  # Muestra cuando se completa el período.
                break  # Termina el ciclo al completar el período.
        
        print("\nVerificación del período:")  # Encabezado para la sección de verificación.
        print(f"Período teórico: {self.periodo}")  # Muestra el período teórico esperado.
        print(f"Período real: {i}")  # Muestra el período real observado.
        print(f"¿Período completo?: {'Sí' if i == self.periodo else 'No'}")  # Verifica si el período es completo.
        print(f"Total de números generados: {len(numeros_generados)}")  # Muestra el total de números generados.
        print(f"¿Se generaron 32057 números?: {'Sí' if len(numeros_generados) == 32057 else 'No'}")  # Verifica si se generaron todos los números.
        print(f"¿Se usaron todos los números?: {'Sí' if len(numeros_generados) == 32057 else 'No'}")  # Verifica si se usaron todos los números.

    def _factorizar_n(self, n: int) -> List[int]:
        # Factoriza un número n en sus factores primos únicos usando el método de división por prueba.
        factores = []  # Lista para almacenar los factores primos únicos.
        num = n  # Copia del número a factorizar.

        if num % 2 == 0:  # Verifica si el número es divisible por 2.
            factores.append(2)  # Agrega 2 como factor primo.
            while num % 2 == 0:  # Divide por 2 hasta que no sea divisible.
                num //= 2  # División entera por 2.

        factor = 3  # Comienza con el siguiente número primo (3).
        while factor * factor <= num:  # Itera hasta la raíz cuadrada del número.
            if num % factor == 0:  # Verifica si el número es divisible por el factor actual.
                factores.append(factor)  # Agrega el factor a la lista.
                while num % factor == 0:  # Divide por el factor hasta que no sea divisible.
                    num //= factor  # División entera por el factor.
            factor += 2  # Avanza al siguiente número impar.

        if num > 1:  # Si queda un residuo mayor que 1, es un factor primo.
            factores.append(num)  # Agrega el último factor primo.

        return factores  # Retorna la lista de factores primos únicos.

    def _generar_raiz_primitiva_aleatoria(self, m: int) -> int:
        # Encuentra una raíz primitiva módulo m mediante prueba aleatoria de candidatos.
        phi = m - 1  # Calcula φ(m) = m-1 (porque m es primo).
        factores = self._factorizar_n(phi)  # Factoriza φ(m) en sus factores primos únicos.

        while True:  # Ciclo infinito hasta encontrar una raíz primitiva.
            candidato = random.randint(2, m - 1)  # Genera un candidato aleatorio entre 2 y m-1.
            es_raiz = True  # Bandera para verificar si el candidato es raíz primitiva.
            for f in factores:  # Itera sobre los factores primos de φ(m).
                if pow(candidato, phi // f, m) == 1:  # Verifica si el candidato^(φ/f) mod m = 1.
                    es_raiz = False  # Si se cumple, el candidato no es raíz primitiva.
                    break  # Termina la verificación para este candidato.
            if es_raiz:  # Si el candidato es raíz primitiva.
                return candidato  # Retorna la raíz primitiva encontrada.

if __name__ == "__main__":
    generador = GCM_Primos()  # Crea una instancia del generador con parámetros por defecto.
    generador.imprimir_parametros()  # Muestra los parámetros del generador.
    generador.imprimir_todas_iteraciones()  # Muestra todas las iteraciones del generador.
