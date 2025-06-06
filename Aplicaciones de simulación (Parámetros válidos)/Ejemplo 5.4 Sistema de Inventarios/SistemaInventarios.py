import numpy as np
from typing import List, Tuple

class GCM:
    def __init__(self, m: int = 32057, X0: int = 20855, a: int = 9600):
        self.m = m  # Módulo del GCM, valor primo que determina el período máximo del generador.
        self.X0 = X0  # Semilla inicial, valor de inicio para la generación de números pseudoaleatorios.
        self.a = a  # Multiplicador, constante que determina la secuencia de números generados.
        self.Xn = X0  # Valor actual del generador, se actualiza en cada iteración.
        self.numeros = []  # Lista para almacenar todos los números generados en el período completo.
        self._generar_hasta_periodo()  # Genera todos los números del período al inicializar el generador.
    
    def _generar_hasta_periodo(self) -> None:
        self.Xn = self.X0  # Inicializa Xn con la semilla X0 para comenzar la generación.
        self.numeros = [self.X0]  # Almacena la semilla inicial en la lista de números generados.
        numeros_generados = set([self.X0])  # Conjunto para verificar números únicos generados.
        
        while True:
            self.Xn = (self.a * self.Xn) % self.m  # Fórmula del GCM: Xn+1 = (a * Xn) mod m.
            if self.Xn in numeros_generados:  # Verifica si el número generado ya existe (período completo).
                break
            numeros_generados.add(self.Xn)  # Agrega el nuevo número al conjunto de números únicos.
            self.numeros.append(self.Xn)  # Almacena el número generado en la lista.
        
        print(f"\nVerificación del GCM:")
        print(f"Parámetros: m={self.m}, X0={self.X0}, a={self.a}")  # Muestra los parámetros utilizados.
        print(f"Números generados: {len(self.numeros)}")  # Muestra la cantidad total de números generados.
        print(f"Deberían ser: {self.m}")  # Muestra el período teórico (m-1).
        print(f"¿Se generaron todos?: {'Sí' if len(self.numeros) == self.m else 'No'}")  # Verifica si se generó el período completo.
        print(f"Números únicos generados: {len(numeros_generados)}")  # Muestra la cantidad de números únicos.
        print(f"Período del GCM: {len(self.numeros)}")  # Muestra el período real del generador.
        
        # Muestra los últimos 5 números generados y sus valores uniformes.
        print("\nÚltimos 5 números generados:")
        print("Xn\t\tNúm. uniforme")
        print("-" * 30)
        for xn in self.numeros[-5:]:
            print(f"{xn}\t\t{xn/self.m:.5f}")  # Calcula el número uniforme dividiendo Xn entre m.
    
    def generar_numero_aleatorio(self) -> float:
        if not self.numeros:  # Verifica si hay números disponibles.
            self._generar_hasta_periodo()  # Regenera los números si es necesario.
        return self.numeros.pop(0) / self.m  # Retorna el siguiente número uniforme [0,1).

# Parámetros fijos del sistema de inventarios.
q = 200  # Cantidad fija a ordenar cuando se realiza un pedido.
R = 100  # Nivel de reorden, punto en el que se debe realizar un nuevo pedido.
inventario_inicial = 150  # Inventario inicial del sistema.

# Factores estacionales por mes (mes 1 a 12) que afectan la demanda.
factores_estacionales = [1.20, 1.00, 0.90, 0.80, 0.80, 0.70, 0.80, 0.90, 1.00, 1.20, 1.30, 1.40]

# Tiempos de entrega predefinidos para cada orden (Tabla 5.11).
tiempos_entrega = [1, 3, 2]  # Tiempos de entrega para órdenes 1, 2 y 3 respectivamente.

def redondear(valor):
    return int(valor + 0.5)  # Función para redondear tradicionalmente (sumando 0.5 y truncando).

def demanda_base(r):
    # Función para determinar la demanda base según la Tabla 5.9.
    if r < 0.010: return 35  # Si r < 0.010, la demanda base es 35.
    elif r < 0.025: return 36  # Si 0.010 ≤ r < 0.025, la demanda base es 36.
    elif r < 0.045: return 37  # Si 0.025 ≤ r < 0.045, la demanda base es 37.
    elif r < 0.065: return 38  # Si 0.045 ≤ r < 0.065, la demanda base es 38.
    elif r < 0.087: return 39  # Si 0.065 ≤ r < 0.087, la demanda base es 39.
    elif r < 0.110: return 40  # Si 0.087 ≤ r < 0.110, la demanda base es 40.
    elif r < 0.135: return 41  # Si 0.110 ≤ r < 0.135, la demanda base es 41.
    elif r < 0.162: return 42  # Si 0.135 ≤ r < 0.162, la demanda base es 42.
    elif r < 0.190: return 43  # Si 0.162 ≤ r < 0.190, la demanda base es 43.
    elif r < 0.219: return 44  # Si 0.190 ≤ r < 0.219, la demanda base es 44.
    elif r < 0.254: return 45  # Si 0.219 ≤ r < 0.254, la demanda base es 45.
    elif r < 0.299: return 46  # Si 0.254 ≤ r < 0.299, la demanda base es 46.
    elif r < 0.359: return 47  # Si 0.299 ≤ r < 0.359, la demanda base es 47.
    elif r < 0.424: return 48  # Si 0.359 ≤ r < 0.424, la demanda base es 48.
    elif r < 0.494: return 49  # Si 0.424 ≤ r < 0.494, la demanda base es 49.
    elif r < 0.574: return 50  # Si 0.494 ≤ r < 0.574, la demanda base es 50.
    elif r < 0.649: return 51  # Si 0.574 ≤ r < 0.649, la demanda base es 51.
    elif r < 0.719: return 52  # Si 0.649 ≤ r < 0.719, la demanda base es 52.
    elif r < 0.784: return 53  # Si 0.719 ≤ r < 0.784, la demanda base es 53.
    elif r < 0.844: return 54  # Si 0.784 ≤ r < 0.844, la demanda base es 54.
    elif r < 0.894: return 55  # Si 0.844 ≤ r < 0.894, la demanda base es 55.
    elif r < 0.934: return 56  # Si 0.894 ≤ r < 0.934, la demanda base es 56.
    elif r < 0.964: return 57  # Si 0.934 ≤ r < 0.964, la demanda base es 57.
    elif r < 0.980: return 58  # Si 0.964 ≤ r < 0.980, la demanda base es 58.
    elif r < 0.995: return 59  # Si 0.980 ≤ r < 0.995, la demanda base es 59.
    else: return 60  # Si r ≥ 0.995, la demanda base es 60.

def simular_anio(gcm: GCM, anio: int) -> List[List]:
    # Estado inicial del sistema.
    inventario_actual = inventario_inicial  # Inventario al inicio del año.
    faltante_pendiente = 0  # Cantidad de unidades faltantes pendientes de surtir.
    orden_pendiente = False  # Indica si hay una orden pendiente de entrega.
    mes_llegada_pedido = None  # Mes en que llegará el próximo pedido.
    num_orden = 1  # Número de la próxima orden a realizar.
    resultados = []  # Lista para almacenar los resultados de cada mes.

    # Simulación mes a mes.
    for mes in range(1, 13):
        # Paso 1: Recepción de órdenes al inicio del mes.
        if mes == mes_llegada_pedido:  # Si es el mes de llegada del pedido.
            inventario_actual += q  # Se recibe la cantidad ordenada q.
            orden_pendiente = False  # Se actualiza el estado de la orden.
            mes_llegada_pedido = None  # Se reinicia el mes de llegada.
            if faltante_pendiente > 0:  # Si hay faltantes pendientes.
                if inventario_actual >= faltante_pendiente:  # Si hay suficiente inventario.
                    inventario_actual -= faltante_pendiente  # Se surten los faltantes.
                    faltante_pendiente = 0  # Se reinicia el faltante pendiente.
        
        # Paso 2: Calcular demanda con redondeo tradicional.
        r = gcm.generar_numero_aleatorio()  # Genera número aleatorio para la demanda.
        demanda_base_val = demanda_base(r)  # Obtiene la demanda base según la tabla.
        demanda_ajustada = redondear(demanda_base_val * factores_estacionales[mes-1])  # Ajusta la demanda por el factor estacional.
        
        # Paso 3: Actualizar inventario.
        if inventario_actual >= demanda_ajustada:  # Si hay suficiente inventario.
            inventario_final = inventario_actual - demanda_ajustada  # Se actualiza el inventario.
            faltante_mes = 0  # No hay faltantes en el mes.
        else:
            inventario_final = 0  # Se agota el inventario.
            faltante_mes = demanda_ajustada - inventario_actual  # Se calcula el faltante.
            faltante_pendiente += faltante_mes  # Se acumula el faltante pendiente.
        
        # Paso 4: Calcular inventario promedio con redondeo.
        if faltante_mes == 0:  # Si no hay faltantes.
            inventario_promedio = redondear((inventario_actual + inventario_final) / 2)  # Promedio simple.
        else:
            inventario_promedio = redondear((inventario_actual ** 2) / (2 * demanda_ajustada))  # Fórmula para faltantes.
        
        # Paso 5: Decisión de ordenar (solo si no hay orden pendiente).
        orden = ""  # Inicializa la variable de orden.
        if inventario_final < R and not orden_pendiente and num_orden <= 3:  # Condiciones para ordenar.
            tiempo_entrega = tiempos_entrega[num_orden-1]  # Obtiene el tiempo de entrega.
            mes_llegada_pedido = mes + tiempo_entrega  # Calcula el mes de llegada.
            orden_pendiente = True  # Marca que hay orden pendiente.
            orden = str(num_orden)  # Guarda el número de orden.
            num_orden += 1  # Incrementa el contador de órdenes.
        
        # Almacenar resultados del mes.
        resultados.append([
            mes,  # Número del mes.
            inventario_actual,  # Inventario al inicio del mes.
            r,  # Número aleatorio generado.
            demanda_ajustada,  # Demanda ajustada por estacionalidad.
            inventario_final,  # Inventario al final del mes.
            faltante_mes if faltante_mes > 0 else "",  # Faltantes del mes (si hay).
            orden,  # Número de orden realizada (si se realizó).
            inventario_promedio  # Inventario promedio del mes.
        ])
        
        # Preparar siguiente mes.
        inventario_actual = inventario_final  # El inventario final se convierte en el inicial del siguiente mes.
    
    return resultados  # Retorna los resultados de todo el año.

def main():
    # Inicializar el GCM con los parámetros definidos.
    gcm = GCM()
    
    # Calcular cuántos años podemos simular.
    numeros_por_anio = 12  # 12 meses por año.
    anios_posibles = len(gcm.numeros) // numeros_por_anio  # División entera para obtener años completos.
    numeros_sobrantes = len(gcm.numeros) % numeros_por_anio  # Números que sobran después de los años completos.
    
    print(f"\nPodemos simular {anios_posibles} años completos con el GCM")  # Muestra años posibles.
    print(f"Nos sobran {numeros_sobrantes} números")  # Muestra números sobrantes.
    
    # Simular cada año.
    for anio in range(1, anios_posibles + 1):
        print(f"\nAño {anio}")  # Muestra el año actual.
        print("=" * 95)  # Línea separadora.
        print(f"{'Mes':<5}{'Inv Inicial':<12}{'Núm Aleat':<12}{'Demanda Aj':<12}{'Inv Final':<12}{'Faltante':<10}{'Orden':<8}{'Inv Prom':<10}")  # Encabezados.
        print("-" * 95)  # Línea separadora.
        
        resultados = simular_anio(gcm, anio)  # Simula el año actual.
        
        for res in resultados:  # Imprime resultados de cada mes.
            print(f"{res[0]:<5}{res[1]:<12}{res[2]:<12.5f}{res[3]:<12}{res[4]:<12}{res[5]!s:<10}{res[6]!s:<8}{res[7]:<10}")
        
        # Cálculo de costos anuales.
        costo_ordenar = sum(1 for res in resultados if res[6]) * 100  # $100 por cada orden realizada.
        costo_inventario = sum([res[7] for res in resultados]) * (20/12)  # $20 por unidad por año (dividido entre 12 meses).
        costo_faltante = sum([res[5] if isinstance(res[5], int) else 0 for res in resultados]) * 50  # $50 por unidad faltante.
        
        print(f"\nCostos del año {anio}:")  # Muestra los costos del año.
        print(f"Costo de ordenar: ${costo_ordenar}")  # Costo de realizar órdenes.
        print(f"Costo de inventario: ${redondear(costo_inventario)}")  # Costo de mantener inventario.
        print(f"Costo de faltante: ${costo_faltante}")  # Costo de faltantes.
        print(f"Total: ${costo_ordenar + redondear(costo_inventario) + costo_faltante}")  # Costo total del año.
    
    # Mostrar estadísticas finales.
    print(f"\nNúmeros generados en total: {len(gcm.numeros) + (anios_posibles * 12)}")  # Total de números generados.
    print(f"Números usados en la simulación: {anios_posibles * 12}")  # Números utilizados.
    print(f"Números restantes en el GCM: {len(gcm.numeros)}")  # Números que quedaron sin usar.
    print(f"¿Se usaron todos los números?: {'Sí' if len(gcm.numeros) == 0 else 'No'}")  # Verificación de uso completo.

if __name__ == "__main__":
    main()  # Ejecuta la simulación principal.