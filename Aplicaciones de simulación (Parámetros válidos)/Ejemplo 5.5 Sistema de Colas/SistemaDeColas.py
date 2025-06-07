import heapq
from collections import deque
from typing import Dict, List, Tuple
import random

class GCM:
    def __init__(self, semilla: int, a: int, m: int):
        self.actual = semilla
        self.a = a
        self.m = m
    
    def siguiente(self) -> float:
        self.actual = (self.a * self.actual) % self.m
        return self.actual / self.m

class Evento:
    def __init__(self, tiempo: float, tipo: str):
        self.tiempo = tiempo
        self.tipo = tipo
    
    def __lt__(self, other):
        return self.tiempo < other.tiempo

# FUNCIONES CORREGIDAS (IGUALES AL DOCUMENTO)
def generar_camiones_iniciales(r: float) -> int:  # Función para generar número de camiones al inicio del turno.
    if r < 0.50: return 0  # 50% de probabilidad de 0 camiones.
    elif r < 0.75: return 1  # 25% de probabilidad de 1 camión.
    elif r < 0.90: return 2  # 15% de probabilidad de 2 camiones.
    else: return 3  # 10% de probabilidad de 3 camiones.

def generar_tiempo_entre_llegadas(r: float) -> int:  # Función para generar tiempo entre llegadas de camiones.
    if r < 0.02: return 20  # 2% de probabilidad de 20 minutos.
    elif r < 0.10: return 25  # 8% de probabilidad de 25 minutos.
    elif r < 0.22: return 30  # 12% de probabilidad de 30 minutos.
    elif r < 0.47: return 35  # 25% de probabilidad de 35 minutos.
    elif r < 0.67: return 40  # 20% de probabilidad de 40 minutos.
    elif r < 0.82: return 45  # 15% de probabilidad de 45 minutos.
    elif r < 0.92: return 50  # 10% de probabilidad de 50 minutos.
    elif r < 0.97: return 55  # 5% de probabilidad de 55 minutos.
    else: return 60  # 3% de probabilidad de 60 minutos.

def generar_tiempo_servicio(k: int, r: float) -> int:  # Función para generar tiempo de servicio según tamaño del equipo.
    if k == 3:  # Distribución para equipo de 3 personas.
        if r < 0.05: return 20  # 5% de probabilidad de 20 minutos.
        elif r < 0.15: return 25  # 10% de probabilidad de 25 minutos.
        elif r < 0.35: return 30  # 20% de probabilidad de 30 minutos.
        elif r < 0.60: return 35  # 25% de probabilidad de 35 minutos.
        elif r < 0.72: return 40  # 12% de probabilidad de 40 minutos.
        elif r < 0.82: return 45  # 10% de probabilidad de 45 minutos.
        elif r < 0.90: return 50  # 8% de probabilidad de 50 minutos.
        elif r < 0.96: return 55  # 6% de probabilidad de 55 minutos.
        else: return 60  # 4% de probabilidad de 60 minutos.
    elif k == 4:  # Distribución para equipo de 4 personas.
        if r < 0.05: return 15  # 5% de probabilidad de 15 minutos.
        elif r < 0.20: return 20  # 15% de probabilidad de 20 minutos.
        elif r < 0.40: return 25  # 20% de probabilidad de 25 minutos.
        elif r < 0.60: return 30  # 20% de probabilidad de 30 minutos.
        elif r < 0.75: return 35  # 15% de probabilidad de 35 minutos.
        elif r < 0.87: return 40  # 12% de probabilidad de 40 minutos.
        elif r < 0.95: return 45  # 8% de probabilidad de 45 minutos.
        elif r < 0.99: return 50  # 4% de probabilidad de 50 minutos.
        else: return 55  # 1% de probabilidad de 55 minutos.
    elif k == 5:  # Distribución para equipo de 5 personas.
        if r < 0.10: return 10  # 10% de probabilidad de 10 minutos.
        elif r < 0.28: return 15  # 18% de probabilidad de 15 minutos.
        elif r < 0.50: return 20  # 22% de probabilidad de 20 minutos.
        elif r < 0.68: return 25  # 18% de probabilidad de 25 minutos.
        elif r < 0.78: return 30  # 10% de probabilidad de 30 minutos.
        elif r < 0.86: return 35  # 8% de probabilidad de 35 minutos.
        elif r < 0.92: return 40  # 6% de probabilidad de 40 minutos.
        elif r < 0.97: return 45  # 5% de probabilidad de 45 minutos.
        else: return 50  # 3% de probabilidad de 50 minutos.
    else:  # k == 6, distribución para equipo de 6 personas.
        if r < 0.12: return 5  # 12% de probabilidad de 5 minutos.
        elif r < 0.27: return 10  # 15% de probabilidad de 10 minutos.
        elif r < 0.53: return 15  # 26% de probabilidad de 15 minutos.
        elif r < 0.68: return 20  # 15% de probabilidad de 20 minutos.
        elif r < 0.80: return 25  # 12% de probabilidad de 25 minutos.
        elif r < 0.88: return 30  # 8% de probabilidad de 30 minutos.
        elif r < 0.94: return 35  # 6% de probabilidad de 35 minutos.
        elif r < 0.98: return 40  # 4% de probabilidad de 40 minutos.
        else: return 45  # 2% de probabilidad de 45 minutos.

def simular_turno(k: int, gen_llegadas: GCM, gen_servicio: GCM) -> Dict[str, float]:
    reloj = 0  # Inicializamos el reloj de simulación (11:00 PM = minuto 0).
    cola = deque()  # Cola FIFO para camiones en espera.
    equipo_libre = True  # Estado del equipo (libre/ocupado).
    en_descanso = False  # Estado de descanso del equipo.
    eventos = []  # Lista de eventos pendientes (cola de prioridad).
    acumulado_espera = 0  # Tiempo total de espera de camiones.
    tiempo_fin_turno = 0  # Tiempo de finalización del turno.
    
    n_inicial = generar_camiones_iniciales(gen_llegadas.siguiente())  # Generamos camiones iniciales.
    for _ in range(n_inicial):  # Programamos llegadas iniciales.
        heapq.heappush(eventos, Evento(0, "llegada"))  # Agregamos eventos de llegada al tiempo 0.
    
    t_prox = generar_tiempo_entre_llegadas(gen_llegadas.siguiente())  # Generamos primera llegada futura.
    heapq.heappush(eventos, Evento(t_prox, "llegada"))  # Programamos primera llegada.
    heapq.heappush(eventos, Evento(240, "inicio_descanso"))  # Programamos descanso a las 3 AM (240 min).
    
    while eventos:  # Bucle principal de simulación.
        evento = heapq.heappop(eventos)  # Extraemos el próximo evento.
        reloj = evento.tiempo  # Actualizamos el reloj.
        tiempo_fin_turno = max(tiempo_fin_turno, reloj)  # Actualizamos tiempo final.
        
        if evento.tipo == "llegada":  # Procesamos llegada de camión.
            if equipo_libre and not en_descanso:  # Si el equipo está libre y no en descanso.
                t_servicio = generar_tiempo_servicio(k, gen_servicio.siguiente())  # Generamos tiempo de servicio.
                heapq.heappush(eventos, Evento(reloj + t_servicio, "fin_servicio"))  # Programamos fin de servicio.
                equipo_libre = False  # Marcamos equipo como ocupado.
            else:  # Si el equipo está ocupado o en descanso.
                cola.append(reloj)  # Agregamos camión a la cola.
            
            if reloj <= 510:  # Si es antes de 7:30 AM (510 min).
                t_prox = generar_tiempo_entre_llegadas(gen_llegadas.siguiente())  # Generamos próxima llegada.
                heapq.heappush(eventos, Evento(reloj + t_prox, "llegada"))  # Programamos llegada.
        
        elif evento.tipo == "fin_servicio":  # Procesamos fin de servicio.
            if cola and not en_descanso:  # Si hay camiones en cola y no en descanso.
                t_llegada = cola.popleft()  # Extraemos primer camión de la cola.
                acumulado_espera += reloj - t_llegada  # Acumulamos tiempo de espera.
                t_servicio = generar_tiempo_servicio(k, gen_servicio.siguiente())  # Generamos tiempo de servicio.
                heapq.heappush(eventos, Evento(reloj + t_servicio, "fin_servicio"))  # Programamos fin de servicio.
            else:  # Si no hay camiones en cola o está en descanso.
                equipo_libre = True  # Marcamos equipo como libre.
        
        elif evento.tipo == "inicio_descanso":  # Procesamos inicio de descanso.
            if not equipo_libre:  # Si el equipo está ocupado.
                heapq.heappush(eventos, Evento(reloj + 1, "inicio_descanso"))  # Posponemos descanso.
            else:  # Si el equipo está libre.
                en_descanso = True  # Marcamos equipo en descanso.
                heapq.heappush(eventos, Evento(reloj + 30, "fin_descanso"))  # Programamos fin de descanso.
        
        elif evento.tipo == "fin_descanso":  # Procesamos fin de descanso.
            en_descanso = False  # Marcamos fin de descanso.
            if cola:  # Si hay camiones en cola.
                t_llegada = cola.popleft()  # Extraemos primer camión.
                acumulado_espera += reloj - t_llegada  # Acumulamos tiempo de espera.
                t_servicio = generar_tiempo_servicio(k, gen_servicio.siguiente())  # Generamos tiempo de servicio.
                heapq.heappush(eventos, Evento(reloj + t_servicio, "fin_servicio"))  # Programamos fin de servicio.
                equipo_libre = False  # Marcamos equipo como ocupado.
    
    horas_operacion = tiempo_fin_turno / 60  # Convertimos minutos a horas de operación.
    minutos_extra = max(0, tiempo_fin_turno - 510)  # Calculamos minutos extra después de 7:30 AM.
    
    salario_normal = k * 8 * 25  # Cálculo de salario normal: k personas * 8 horas * $25/hora.
    salario_extra = k * (minutos_extra / 60) * 37.5  # Cálculo de salario extra: k personas * horas extra * $37.5/hora.
    costo_espera = (acumulado_espera / 60) * 100  # Cálculo de costo de espera: horas de espera * $100/hora.
    costo_operacion = 500 * horas_operacion  # Cálculo de costo de operación: horas de operación * $500/hora.
    
    return {  # Retornamos diccionario con todos los costos.
        "salario_normal": salario_normal,  # Salario normal del turno.
        "salario_extra": salario_extra,  # Salario extra por tiempo adicional.
        "costo_espera": costo_espera,  # Costo por tiempo de espera de camiones.
        "costo_operacion": costo_operacion,  # Costo de operación del almacén.
        "costo_total": salario_normal + salario_extra + costo_espera + costo_operacion,  # Costo total del turno.
        "horas_operacion": horas_operacion  # Horas totales de operación.
    }

def main():  # Función principal del programa.
    a = 9600  # Multiplicador del GCM.
    m = 32057  # Módulo del GCM.
    semilla_base = 20855  # Semilla base para generadores.
    
    resultados = {k: {  # Diccionario para almacenar resultados por tamaño de equipo.
        "salario_normal": 0,  # Inicializamos contadores en 0.
        "salario_extra": 0,
        "costo_espera": 0,
        "costo_operacion": 0,
        "costo_total": 0,
        "horas_operacion": 0
    } for k in range(3, 7)}  # Para equipos de 3 a 6 personas.
    
    for k in range(3, 7):  # Iteramos sobre cada tamaño de equipo.
        for turno in range(60):  # Simulamos 60 turnos.
            semilla_llegadas = (semilla_base + k*1000 + turno) % m  # Calculamos semilla para llegadas.
            semilla_servicios = (semilla_base + k*1000 + turno + 10000) % m  # Calculamos semilla para servicios.
            
            gen_llegadas = GCM(semilla_llegadas, a, m)  # Creamos generador para llegadas.
            gen_servicios = GCM(semilla_servicios, a, m)  # Creamos generador para servicios.
            
            res_turno = simular_turno(k, gen_llegadas, gen_servicios)  # Simulamos un turno.
            
            for key in resultados[k]:  # Acumulamos resultados.
                resultados[k][key] += res_turno[key]
        
        for key in resultados[k]:  # Calculamos promedios.
            resultados[k][key] /= 60.0  # Dividimos entre 60 turnos.
    
    print("\nResultados de simulación (promedio 60 turnos)")  # Imprimimos encabezado.
    print("Tamaño | Salario Normal | Salario Extra | Costo Espera | Operación | Total")  # Imprimimos columnas.
    print("-------+----------------+---------------+--------------+-----------+---------")  # Imprimimos separador.
    
    for k in range(3, 7):  # Iteramos sobre cada tamaño de equipo.
        r = resultados[k]  # Obtenemos resultados para este tamaño.
        print(f"{k:6} | ${r['salario_normal']:>14.2f} | ${r['salario_extra']:>13.2f} | "  # Imprimimos fila de resultados.
              f"${r['costo_espera']:>11.2f} | ${r['costo_operacion']:>8.2f} | "
              f"${r['costo_total']:>8.2f}")
    
    k_optimo = min(resultados, key=lambda k: resultados[k]["costo_total"])  # Encontramos tamaño óptimo.
    print(f"\nEl tamaño óptimo del equipo es: {k_optimo} personas")  # Imprimimos resultado.
    print(f"Costo promedio por turno: ${resultados[k_optimo]['costo_total']:.2f}")  # Imprimimos costo óptimo.

if __name__ == "__main__":  # Punto de entrada del programa.
    main()  # Ejecutamos la función principal.