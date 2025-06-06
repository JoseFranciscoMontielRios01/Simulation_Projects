import numpy as np  # Importamos numpy para operaciones matemáticas.
from typing import List, Dict, Tuple  # Importamos tipos para mejor documentación del código.
from dataclasses import dataclass  # Importamos dataclass para crear clases de datos.

class GCM:
    def __init__(self, m: int, X0: int, a: int):  # Constructor de la clase con parámetros del GCM.
        self.m = m  # Módulo del GCM (32057).
        self.X0 = X0  # Semilla inicial (20855).
        self.a = a  # Multiplicador (9600).
        self.Xn = X0  # Valor actual del generador.
        
    def generar_numero(self) -> float:  # Método para generar un número pseudoaleatorio.
        self.Xn = (self.a * self.Xn) % self.m  # Fórmula del GCM: Xn+1 = (a*Xn) mod m.
        return self.Xn / self.m  # Normalizamos el número al intervalo [0,1].
        
    def generar_hasta_periodo(self) -> List[float]:  # Método para generar todos los números posibles.
        numeros = []  # Lista para almacenar los números generados.
        numeros_generados = set()  # Conjunto para detectar ciclos.
        self.Xn = self.X0  # Reiniciamos el generador a la semilla inicial.
        
        while True:  # Bucle hasta encontrar un ciclo.
            numero = self.generar_numero()  # Generamos un nuevo número.
            if numero in numeros_generados:  # Si el número ya existe, hemos encontrado un ciclo.
                break
            numeros.append(numero)  # Agregamos el número a la lista.
            numeros_generados.add(numero)  # Agregamos el número al conjunto de control.
            
        return numeros  # Retornamos la lista completa de números generados.

@dataclass
class ConfiguracionJuego:  # Clase para almacenar la configuración del juego.
    def __init__(self, capital_inicial: float = 1000.0, meta: float = 2000.0, 
                 apuesta_inicial: float = 100.0):  # Constructor con valores por defecto.
        self.capital_inicial = capital_inicial  # Dinero inicial del jugador.
        self.meta = meta  # Meta a alcanzar.
        self.apuesta_inicial = apuesta_inicial  # Apuesta inicial en cada volado.

class SimulacionVolados:  # Clase principal de la simulación.
    def __init__(self, config: ConfiguracionJuego):  # Constructor con la configuración.
        self.config = config  # Guardamos la configuración.
        self.gcm = GCM(m=32057, X0=20855, a=9600)  # Inicializamos el GCM con parámetros óptimos.
        self.numeros = self.gcm.generar_hasta_periodo()  # Generamos todos los números posibles.
        self.indice_actual = 0  # Índice para recorrer la lista de números.
        self.detalles_corridas = []  # Lista para almacenar los detalles de cada corrida.
        self.exitos = 0  # Contador de éxitos (alcanzar la meta).
        self.quiebras = 0  # Contador de quiebras (perder todo el dinero).

    def simular_volado(self, capital: float, apuesta: float) -> Tuple[float, float, str, str, float]:  # Simula un volado individual.
        if self.indice_actual >= len(self.numeros):  # Verificamos si hay números disponibles.
            return None, None, None, None, None
            
        r = self.numeros[self.indice_actual]  # Obtenemos el siguiente número pseudoaleatorio.
        self.indice_actual += 1  # Avanzamos el índice.
        
        resultado = "Águila" if r < 0.5 else "Sol"  # Determinamos el resultado del volado.
        
        nuevo_capital = capital + apuesta if resultado == "Águila" else capital - apuesta  # Calculamos el nuevo capital.
        
        meta_alcanzada = "Sí" if nuevo_capital >= self.config.meta else "No"  # Verificamos si se alcanzó la meta.
        
        return nuevo_capital, apuesta, resultado, meta_alcanzada, r  # Retornamos todos los datos del volado.

    def simular_corrida(self, numero_corrida: int) -> None:  # Simula una corrida completa del juego.
        capital = self.config.capital_inicial  # Inicializamos el capital.
        apuesta = self.config.apuesta_inicial  # Inicializamos la apuesta.
        registro_pasos = []  # Lista para registrar cada paso de la corrida.
        paso = 1  # Contador de pasos.
        
        while capital >= apuesta and capital < self.config.meta:  # Mientras haya dinero para apostar y no se alcance la meta.
            resultado = self.simular_volado(capital, apuesta)  # Simulamos un volado.
            if resultado[0] is None:  # Si se acabaron los números, terminamos.
                break
                
            nuevo_capital, apuesta_actual, resultado_volado, meta_alcanzada, numero_pseudo = resultado  # Desempaquetamos el resultado.
            
            registro_pasos.append([  # Registramos el paso actual.
                paso,
                f"{capital:.2f}",
                f"{apuesta:.2f}",
                f"{numero_pseudo:.5f}",
                "Sí" if resultado_volado == "Águila" else "No",
                f"{nuevo_capital:.2f}",
                meta_alcanzada
            ])
            
            capital = nuevo_capital  # Actualizamos el capital.
            if resultado_volado == "Sol":  # Si perdió, aplicamos la estrategia de Martingala.
                nueva_apuesta = min(2 * apuesta, capital)  # Duplicamos la apuesta sin exceder el capital.
                apuesta = nueva_apuesta if nueva_apuesta >= self.config.apuesta_inicial else self.config.apuesta_inicial  # Mantenemos la apuesta inicial como mínimo.
            else:
                apuesta = self.config.apuesta_inicial  # Si ganó, reiniciamos la apuesta.
            paso += 1  # Avanzamos al siguiente paso.
        
        self.detalles_corridas.append({  # Guardamos los detalles de la corrida.
            "numero_corrida": numero_corrida,
            "registro_pasos": registro_pasos,
            "capital_final": capital,
            "exito": capital >= self.config.meta,
            "quiebra": capital < apuesta
        })
        
        if capital >= self.config.meta:  # Actualizamos contadores.
            self.exitos += 1
        elif capital < apuesta:
            self.quiebras += 1

    def ejecutar_simulacion(self) -> None:  # Ejecuta la simulación completa.
        numero_corrida = 1  # Inicializamos el contador de corridas.
        while self.indice_actual < len(self.numeros):  # Mientras haya números disponibles.
            self.simular_corrida(numero_corrida)  # Simulamos una corrida.
            numero_corrida += 1  # Avanzamos a la siguiente corrida.
            
        self._generar_reporte()  # Generamos el reporte final.

    def _formatear_tabla(self, datos: List[List], headers: List[str]) -> str:  # Formatea una tabla para mostrar datos.
        anchos = [8, 12, 8, 12, 8, 12, 8]  # Definimos el ancho de cada columna.
        
        header_line = "  ".join(f"{h:<{ancho}}" for h, ancho in zip(headers, anchos))  # Creamos la línea de encabezados.
        
        filas = []  # Lista para almacenar las filas formateadas.
        for fila in datos:  # Procesamos cada fila de datos.
            fila_formateada = []  # Lista para la fila actual.
            for i, (cell, ancho) in enumerate(zip(fila, anchos)):  # Procesamos cada celda.
                if i == 0 and not cell:  # Si es la primera columna y está vacía.
                    fila_formateada.append(" " * ancho)  # Agregamos espacios.
                else:
                    fila_formateada.append(f"{str(cell):<{ancho}}")  # Formateamos la celda.
            filas.append("  ".join(fila_formateada))  # Unimos las celdas de la fila.
        
        return f"{header_line}\n" + "\n".join(filas)  # Retornamos la tabla completa.

    def _generar_reporte(self) -> None:  # Genera el reporte detallado de la simulación.
        for corrida in self.detalles_corridas:  # Procesamos cada corrida.
            print("\nDetalle de la corrida", corrida["numero_corrida"])  # Imprimimos el número de corrida.
            print("="*90)  # Línea separadora.
            
            headers = [  # Definimos los encabezados de la tabla.
                "N°",
                "Cant.Ant",
                "Apuesta",
                "N° Pseudo",
                "¿Ganó?",
                "Cant.Post",
                "¿Es la meta?"
            ]
            
            print(self._formatear_tabla(corrida["registro_pasos"], headers))  # Imprimimos la tabla de la corrida.
            print()  # Línea en blanco entre corridas.
        
        total_corridas = len(self.detalles_corridas)  # Calculamos el total de corridas.
        prob_ganar = self.exitos / total_corridas  # Probabilidad de ganar.
        prob_quiebra = self.quiebras / total_corridas  # Probabilidad de quiebra.
        
        total_volados = sum(len(corrida["registro_pasos"]) for corrida in self.detalles_corridas)  # Total de volados realizados.
        volados_ganados = sum(1 for corrida in self.detalles_corridas 
                            for paso in corrida["registro_pasos"] 
                            if paso[4] == "Sí")  # Total de volados ganados.
        prob_volado_ganado = volados_ganados / total_volados if total_volados > 0 else 0  # Probabilidad de ganar un volado.
        
        print("\nValidación de la Distribución")  # Sección de validación.
        print("="*60)
        print(f"Probabilidad teórica de ganar un volado: 0.50000")  # Probabilidad teórica.
        print(f"Probabilidad simulada de ganar un volado: {prob_volado_ganado:.5f}")  # Probabilidad simulada.
        print(f"Error absoluto: {abs(prob_volado_ganado - 0.5):.5f}")  # Error absoluto.
        print(f"Error relativo: {abs(prob_volado_ganado - 0.5)/0.5*100:.2f}%")  # Error relativo.
        
        print("\nTabla de frecuencias finales")  # Tabla de frecuencias.
        print("="*60)
        print(self._formatear_tabla(
            [
                ["Ganar:", self.exitos],
                ["Quiebra:", self.quiebras],
                ["Total:", total_corridas]
            ],
            ["Evento:", "Frecuencia:"]
        ))
        
        print("\nTabla de probabilidades")  # Tabla de probabilidades.
        print("="*60)
        print("Evento:                Decimal:    Porcentaje:")
        print("-"*60)
        print(f"Prob.Ganar:           {prob_ganar:.9f}    {prob_ganar*100:.0f}%")  # Probabilidad de ganar.
        print(f"Prob.Quiebra:         {prob_quiebra:.9f}    {prob_quiebra*100:.0f}%")  # Probabilidad de quiebra.
        print(f"Prob.Volado.Ganado:   {prob_volado_ganado:.9f}    {prob_volado_ganado*100:.0f}%")  # Probabilidad de ganar un volado.

        print("\nEstadísticas adicionales")  # Estadísticas adicionales.
        print("="*60)
        print(f"Total de volados realizados: {total_volados}")  # Total de volados.
        print(f"Volados ganados: {volados_ganados}")  # Volados ganados.
        print(f"Volados perdidos: {total_volados - volados_ganados}")  # Volados perdidos.
        print(f"Promedio de volados por corrida: {total_volados/total_corridas:.2f}")  # Promedio de volados.
        print(f"Período del GCM: {len(self.numeros)}")  # Período del generador.

        print("\nParámetros del Generador Congruencial Multiplicativo (GCM)")  # Parámetros del GCM.
        print("="*60)
        print(f"Módulo (m): {self.gcm.m}")  # Módulo.
        print(f"Semilla (X₀): {self.gcm.X0}")  # Semilla.
        print(f"Multiplicador (a): {self.gcm.a}")  # Multiplicador.
        print("="*60)

def main():  # Función principal.
    config = ConfiguracionJuego(  # Creamos la configuración del juego.
        capital_inicial=30.0,  # Capital inicial de $30.
        meta=50.0,  # Meta de $50.
        apuesta_inicial=10.0  # Apuesta inicial de $10.
    )
    
    simulacion = SimulacionVolados(config)  # Creamos la simulación.
    simulacion.ejecutar_simulacion()  # Ejecutamos la simulación.

if __name__ == "__main__":  # Punto de entrada del programa.
    main()  # Llamamos a la función principal. 