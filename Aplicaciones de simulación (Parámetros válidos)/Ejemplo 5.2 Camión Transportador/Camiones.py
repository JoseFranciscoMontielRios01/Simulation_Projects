import math  # Importamos math para operaciones matemáticas como raíz cuadrada.
import random  # Importamos random para generación de números aleatorios.
from typing import List, Tuple, Dict, Any  # Importamos tipos para mejor documentación del código.
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

class Camiones:  # Clase para la simulación de camiones.
    def __init__(self, m: int, X0: int, a: int):  # Constructor con parámetros del GCM.
        self.m = m  # Módulo del GCM.
        self.X0 = X0  # Semilla inicial.
        self.a = a  # Multiplicador.
        self.Xn = X0  # Valor actual del generador.
        
    def generar_numero(self) -> float:  # Método para generar un número pseudoaleatorio.
        self.Xn = (self.a * self.Xn) % self.m  # Fórmula del GCM.
        return self.Xn / self.m  # Normalizamos el número al intervalo [0,1].
        
    def generar_hasta_periodo(self) -> List[float]:  # Método para generar todos los números posibles.
        numeros = []  # Lista para almacenar los números generados.
        numeros_generados = set()  # Conjunto para detectar ciclos.
        self.Xn = self.X0  # Reiniciamos el generador.
        
        while True:  # Bucle hasta encontrar un ciclo.
            numero = self.generar_numero()  # Generamos un nuevo número.
            if numero in numeros_generados:  # Si el número ya existe, hemos encontrado un ciclo.
                break
            numeros.append(numero)  # Agregamos el número a la lista.
            numeros_generados.add(numero)  # Agregamos el número al conjunto de control.
            
        return numeros  # Retornamos la lista completa de números generados.

@dataclass
class ConfiguracionSimulacion:  # Clase para almacenar la configuración de la simulación.
    def __init__(self, capacidad_camion: float = 1000.0, n_tinas: int = 5,  # Constructor con valores por defecto.
                 costo_excedente: float = 200.0, costo_nuevo_camion: float = 60000.0,
                 dias_anuales: int = 260):
        self.capacidad_camion = capacidad_camion  # Capacidad máxima del camión en kg.
        self.n_tinas = n_tinas  # Número de tinas por día.
        self.costo_excedente = costo_excedente  # Costo por exceder la capacidad.
        self.costo_nuevo_camion = costo_nuevo_camion  # Costo de comprar un nuevo camión.
        self.dias_anuales = dias_anuales  # Días laborables por año.

class SimulacionCamiones:  # Clase principal de la simulación.
    def __init__(self, config: ConfiguracionSimulacion):  # Constructor con la configuración.
        self.config = config  # Guardamos la configuración.
        self.gcm = GCM(m=32057, X0=20855, a=9600)  # Inicializamos el GCM con parámetros óptimos.
        self.numeros = self.gcm.numeros  # Obtenemos la lista de números generados.
        self.indice_actual = 0  # Índice para recorrer la lista de números.
        self.costos_anuales = []  # Lista para almacenar los costos anuales.
        self.detalles_corridas = []  # Lista para almacenar los detalles de cada corrida.
        self.excesos = 0  # Contador de excesos de peso.
        
        total_numeros = len(self.numeros)  # Total de números disponibles.
        if total_numeros < 32056:  # Verificamos si tenemos suficientes números.
            raise ValueError(f"No se generaron suficientes números. Se necesitan 32056 pero solo se generaron {total_numeros}")
        
        dias_por_anio = self.config.dias_anuales  # Días por año (260).
        tinas_por_dia = self.config.n_tinas  # Tinas por día (5).
        numeros_por_corrida = dias_por_anio * tinas_por_dia  # Números necesarios por corrida (1300).
        
        self.num_corridas = total_numeros // numeros_por_corrida  # Número de corridas completas posibles.
        
        numeros_sobrantes = total_numeros % numeros_por_corrida  # Números que sobran.
        
        self.tinas_extra_por_corrida = numeros_sobrantes // self.num_corridas  # Tinas extra por corrida.
        self.tinas_extra_ultima_corrida = numeros_sobrantes % self.num_corridas  # Tinas extra en la última corrida.
        
        print(f"\nDistribución de números:")  # Información de distribución.
        print(f"Total de números disponibles: {total_numeros}")  # Total de números.
        print(f"Números por corrida base: {numeros_por_corrida}")  # Números por corrida.
        print(f"Corridas completas: {self.num_corridas}")  # Número de corridas.
        print(f"Números sobrantes: {numeros_sobrantes}")  # Números sobrantes.
        print(f"Tinas extra por corrida: {self.tinas_extra_por_corrida}")  # Tinas extra por corrida.
        print(f"Tinas extra en última corrida: {self.tinas_extra_ultima_corrida}")  # Tinas extra en última corrida.
        
        numeros_a_usar = (self.num_corridas * numeros_por_corrida) + numeros_sobrantes  # Total de números a usar.
        print(f"\nVerificación de uso de números:")  # Verificación de uso.
        print(f"Números que se usarán: {numeros_a_usar}")  # Números a usar.
        print(f"Números disponibles: {total_numeros}")  # Números disponibles.
        print(f"¿Se usarán todos los números?: {'Sí' if numeros_a_usar == total_numeros else 'No'}")  # Verificación de uso completo.
        
        self.simular_corridas()  # Iniciamos la simulación.

    def simular_corridas(self) -> None:  # Método para simular todas las corridas.
        for i in range(self.num_corridas):  # Para cada corrida posible.
            self.simular_anio(i)  # Simulamos un año.

    def simular_anio(self, numero_anio: int) -> None:  # Método para simular un año completo.
        costo_anual = 0  # Inicializamos el costo anual.
        registro_dias = []  # Lista para registrar los días.
        dias_con_exceso = 0  # Contador de días con exceso.
        
        tinas_extra = self.tinas_extra_por_corrida  # Tinas extra para esta corrida.
        if numero_anio == self.num_corridas - 1:  # Si es la última corrida.
            tinas_extra += self.tinas_extra_ultima_corrida  # Agregamos las tinas extra de la última corrida.
        
        for dia in range(1, self.config.dias_anuales + 1):  # Para cada día del año.
            tinas_este_dia = self.config.n_tinas  # Número base de tinas.
            if tinas_extra > 0:  # Si hay tinas extra disponibles.
                tinas_este_dia += 1  # Agregamos una tina extra.
                tinas_extra -= 1  # Reducimos el contador de tinas extra.
            
            try:  # Intentamos simular el día.
                peso_total, excede, registro_tinas = self.simular_dia(tinas_este_dia)  # Simulamos el día.
                
                if excede:  # Si se excedió la capacidad.
                    costo_anual += self.config.costo_excedente  # Agregamos el costo.
                    dias_con_exceso += 1  # Incrementamos el contador.
                
                registro_dias.extend(registro_tinas)  # Agregamos el registro del día.
            except ValueError as e:  # Si hay un error.
                print(f"\nError en año {numero_anio + 1}, día {dia}:")  # Mostramos información del error.
                print(f"Índice actual: {self.indice_actual}")  # Índice actual.
                print(f"Números disponibles: {len(self.numeros)}")  # Números disponibles.
                print(f"Tinas requeridas: {tinas_este_dia}")  # Tinas requeridas.
                raise e  # Relanzamos el error.
        
        self.costos_anuales.append(costo_anual)  # Guardamos el costo anual.
        
        self.detalles_corridas.append({  # Guardamos los detalles de la corrida.
            "numero_anio": numero_anio,
            "registro_dias": registro_dias,
            "costo_anual": costo_anual,
            "dias_con_exceso": dias_con_exceso
        })

    def simular_dia(self, tinas_este_dia: int = None) -> Tuple[float, bool, List[List[Any]]]:  # Método para simular un día.
        if tinas_este_dia is None:  # Si no se especifica el número de tinas.
            tinas_este_dia = self.config.n_tinas  # Usamos el valor por defecto.
            
        if self.indice_actual + tinas_este_dia > len(self.numeros):  # Si no hay suficientes números.
            self.indice_actual = 0  # Reiniciamos el índice.
            
        peso_acumulado = 0  # Inicializamos el peso acumulado.
        registro_tinas = []  # Lista para registrar las tinas.
        excede = False  # Flag para exceso de peso.
        
        for tina in range(1, tinas_este_dia + 1):  # Para cada tina del día.
            R = self.numeros[self.indice_actual] / self.gcm.m  # Obtenemos el número aleatorio normalizado.
            self.indice_actual += 1  # Avanzamos el índice.
            
            if R < 0.5:  # Si R < 0.5, usamos la primera fórmula.
                peso = 190 + math.sqrt(800 * R)  # Fórmula para pesos bajos.
            else:  # Si R >= 0.5, usamos la segunda fórmula.
                peso = 230 - math.sqrt(800 * (1 - R))  # Fórmula para pesos altos.
                
            peso_acumulado += peso  # Acumulamos el peso.
            
            if peso_acumulado > self.config.capacidad_camion:  # Si se excede la capacidad.
                excede = True  # Marcamos el exceso.
            
            registro_tinas.append([  # Registramos la tina.
                tina,
                f"{R:.5f}",
                f"{peso:.0f}",
                f"{peso_acumulado:.0f}",
                "Sí" if excede else "No"
            ])
        
        return peso_acumulado, excede, registro_tinas  # Retornamos los resultados del día.

    def ejecutar_simulacion(self) -> None:  # Método para ejecutar la simulación completa.
        print("\nIniciando simulación...")  # Mensaje de inicio.
        self.simular_corridas()  # Simulamos todas las corridas.
        self._generar_reporte()  # Generamos el reporte.

    def _generar_reporte(self) -> None:  # Método para generar el reporte detallado.
        for corrida in self.detalles_corridas:  # Para cada corrida.
            print("\n" + "="*100)  # Línea separadora superior.
            print(f"Corrida {corrida['numero_anio'] + 1}")  # Número de corrida.
            print("="*100)
            # Ajustamos el formato de los encabezados para que coincida con los datos
            print(f"{'N°':<4} {'Tina':<6} {'N° uniforme':<12} {'Peso tina':<8} {'Peso Acum.':<10} {'¿Se excede?':<8}")
            print("-"*100)  # Línea separadora del encabezado.
            
            tinas_por_dia = []  # Lista para agrupar tinas por día.
            tinas_actuales = []  # Lista para las tinas del día actual.
            dia_actual = 1  # Contador de días.
            
            for registro in corrida["registro_dias"]:  # Para cada registro.
                if len(tinas_actuales) == 0:  # Si es la primera tina del día.
                    tinas_actuales.append([dia_actual] + registro)  # Agregamos el número de día.
                else:
                    tinas_actuales.append([""] + registro)  # Agregamos espacio en blanco.
                
                if registro[4] == "Sí" or len(tinas_actuales) == self.config.n_tinas:  # Si se excede o se completó el día.
                    tinas_por_dia.extend(tinas_actuales)  # Agregamos las tinas del día.
                    tinas_actuales = []  # Reiniciamos la lista.
                    dia_actual += 1  # Avanzamos al siguiente día.
            
            for tina in tinas_por_dia:  # Imprimimos cada tina.
                # Formateamos cada columna según su tipo de dato y alineación
                dia = f"{str(tina[0]):<4}"  # Día (puede ser número o string vacío)
                num_tina = f"{str(tina[1]):<6}"  # Número de tina
                num_unif = f"{float(tina[2]):.5f}"  # Número uniforme
                peso = f"{float(tina[3]):.2f}"  # Peso de la tina
                peso_acum = f"{float(tina[4]):.2f}"  # Peso acumulado
                excede = f"{str(tina[5]):<8}"  # ¿Se excede?
                
                # Imprimimos con espacios adicionales entre columnas para mejor separación.
                print(f"{dia}    {num_tina}    {num_unif}    {peso}    {peso_acum}    {excede}")
            
            # Imprimimos los encabezados nuevamente al final de la corrida.
            print("-"*100)  # Línea separadora antes de repetir encabezados.
            print(f"{'N°':<4} {'Tina':<6} {'N° uniforme':<12} {'Peso tina':<8} {'Peso Acum.':<10} {'¿Se excede?':<8}")
            print("="*100)  # Línea separadora inferior.
            print()  # Línea en blanco entre corridas.
        
        total_corridas = len(self.detalles_corridas)  # Total de corridas.
        total_dias = total_corridas * self.config.dias_anuales  # Total de días simulados.
        
        dias_con_exceso = sum(corrida["dias_con_exceso"] for corrida in self.detalles_corridas)  # Días con exceso.
        
        prob_exceso = dias_con_exceso / total_dias  # Probabilidad de exceso.
        
        todos_los_pesos = []  # Lista para todos los pesos.
        pesos_fuera_rango = 0  # Contador de pesos fuera de rango.
        for corrida in self.detalles_corridas:  # Para cada corrida.
            for registro in corrida["registro_dias"]:  # Para cada registro.
                peso = float(registro[3])  # Obtenemos el peso.
                todos_los_pesos.append(peso)  # Agregamos el peso a la lista.
                if peso < 190 or peso > 230:  # Si está fuera del rango.
                    pesos_fuera_rango += 1  # Incrementamos el contador.
        
        media_pesos = sum(todos_los_pesos) / len(todos_los_pesos)  # Calculamos la media.
        varianza_pesos = sum((x - media_pesos) ** 2 for x in todos_los_pesos) / len(todos_los_pesos)  # Calculamos la varianza.
        
        prob_analitica = 0.99693  # Probabilidad analítica teórica.
        error_absoluto = abs(prob_exceso - prob_analitica)  # Error absoluto.
        error_relativo = (error_absoluto / prob_analitica) * 100  # Error relativo.
        
        print("\nValidación de la Distribución")  # Sección de validación.
        print("="*60)
        print(f"Media teórica: 210.00 kg")  # Media teórica.
        print(f"Media simulada: {media_pesos:.2f} kg")  # Media simulada.
        print(f"Varianza teórica: 66.67")  # Varianza teórica.
        print(f"Varianza simulada: {varianza_pesos:.2f}")  # Varianza simulada.
        print(f"Pesos fuera del rango [190, 230]: {pesos_fuera_rango} ({pesos_fuera_rango/len(todos_los_pesos)*100:.2f}%)")  # Pesos fuera de rango.
        
        print("\nAnálisis de Convergencia")  # Sección de convergencia.
        print("="*60)
        print(f"Probabilidad analítica: {prob_analitica:.5f}")  # Probabilidad analítica.
        print(f"Probabilidad simulada: {prob_exceso:.5f}")  # Probabilidad simulada.
        print(f"Error absoluto: {error_absoluto:.5f}")  # Error absoluto.
        print(f"Error relativo: {error_relativo:.2f}%")  # Error relativo.
        
        print("\nTabla de frecuencias")  # Tabla de frecuencias.
        print("="*80)
        print(f"{'Capacidad':<20} {'Número de veces':>15} {'Porcentaje decimal':>20} {'Porcentaje exacto':>10}")  # Encabezados.
        print("-"*80)
        print(f"{'Excedida':<20} {dias_con_exceso:>15} {prob_exceso:>20.3f} {prob_exceso*100:>10.0f}%")  # Fila de excedida.
        print(f"{'No excedida':<20} {total_dias - dias_con_exceso:>15} {(1-prob_exceso):>20.3f} {(1-prob_exceso)*100:>10.0f}%")  # Fila de no excedida.
        print(f"{'Total':<20} {total_dias:>15} {1.000:>20.3f} {100:>10}%")  # Fila de total.
        
        print("\nParámetros de costos")  # Sección de costos.
        print("="*60)
        print(f"Costo por tina\t\t${self.config.costo_excedente}")  # Costo por tina.
        print(f"día\t\t\t1")  # Días.
        print(f"días * semana\t\t5")  # Días por semana.
        print(f"semana * año\t\t52")  # Semanas por año.
        
        costo_promedio = sum(corrida["costo_anual"] for corrida in self.detalles_corridas) / total_corridas  # Costo promedio.
        costo_anual_esperado = dias_con_exceso * self.config.costo_excedente / total_corridas  # Costo anual esperado.
        
        print("\nCostos")  # Sección de costos.
        print("="*60)
        print(f"Costo total de pagar otra compañía\t${costo_anual_esperado:.2f}")  # Costo de contratar.
        print(f"Costo de un nuevo camión\t\t${self.config.costo_nuevo_camion:.2f}")  # Costo de comprar.
        
        print("\nConclusión:")  # Sección de conclusión.
        if costo_anual_esperado >= self.config.costo_nuevo_camion:  # Si es más caro contratar.
            print("Es más rentable comprar un nuevo camión. ")  # Recomendación de comprar.
        else:
            print("Es más rentable contratar otra compañía. ")  # Recomendación de contratar.

        print("\nParámetros del Generador Congruencial Multiplicativo (GCM)")  # Parámetros del GCM.
        print("="*60)
        print(f"Módulo (m): {self.gcm.m}")  # Módulo.
        print(f"Semilla (X₀): {self.gcm.X0}")  # Semilla.
        print(f"Multiplicador (a): {self.gcm.a}")  # Multiplicador.
        print(f"Período del GCM: {len(self.numeros)}")  # Período.
        print("="*60)

def main():  # Función principal.
    config = ConfiguracionSimulacion(  # Creamos la configuración.
        capacidad_camion=1000,  # Capacidad del camión en kg.
        n_tinas=5,  # Número de tinas por día.
        costo_excedente=200,  # Costo por exceder la capacidad.
        costo_nuevo_camion=60000,  # Costo de un nuevo camión.
        dias_anuales=260  # Días laborables por año.
    )
    
    simulacion = SimulacionCamiones(config)  # Creamos la simulación.
    simulacion.ejecutar_simulacion()  # Ejecutamos la simulación.

if __name__ == "__main__":  # Punto de entrada del programa.
    main()  # Llamamos a la función principal. 