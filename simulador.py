from sistema import SistemaColas
from generador import generar_personas
from typing import Tuple

class Simulador:
    def __init__(self, 
                num_estaciones: int, 
                tiene_estacion_exclusiva: bool,
                tiempo_total: float = 480,  # 8 horas = 480 minutos
                lambda_llegadas: float = 0.5,  # tasa media de llegadas por minuto
                lambda_servicio: float = 0.25,  # tasa media de servicio por minuto
                prob_prioridad: float = 0.3):  # probabilidad de que tenga prioridad
        # inicialización del simulador con sus parámetros
        self.__num_estaciones = num_estaciones
        self.__tiene_estacion_exclusiva = tiene_estacion_exclusiva
        self.__tiempo_total = tiempo_total
        self.__lambda_llegadas = lambda_llegadas
        self.__lambda_servicio = lambda_servicio
        self.__prob_prioridad = prob_prioridad
        self.__sistema = SistemaColas(num_estaciones, tiene_estacion_exclusiva)
        self.__personas = []
    
    def ejecutar_simulacion(self) -> Tuple[float, int, float]:
        # realiza la simulación completa y retorna las estadísticas
        print(f"Iniciando simulación {'con' if self.__tiene_estacion_exclusiva else 'sin'} estación exclusiva...")
        
        # generar personas que llegarán durante el día
        self.__personas = generar_personas(
            self.__tiempo_total, 
            self.__lambda_llegadas, 
            self.__prob_prioridad, 
            self.__lambda_servicio
        )
        
        # ordenar personas por tiempo de llegada (por si acaso)
        self.__personas.sort(key=lambda p: p.get_tiempo_llegada())
        
        print(f"Generadas {len(self.__personas)} personas para la simulación")
        
        # simular el paso de tiempo minuto a minuto
        tiempo_actual = 0.0
        indice_persona = 0
        
        while tiempo_actual <= self.__tiempo_total:
            # procesar llegadas de personas
            while indice_persona < len(self.__personas) and self.__personas[indice_persona].get_tiempo_llegada() <= tiempo_actual:
                self.__sistema.agregar_persona(self.__personas[indice_persona])
                indice_persona += 1
            
            # asignar personas a estaciones disponibles
            self.__sistema.asignar_personas_a_estaciones(tiempo_actual)
            
            # avanzar el tiempo hasta el próximo evento
            tiempo_actual = self.__calcular_tiempo_proximo_evento(tiempo_actual, indice_persona)
        
        # guardar tiempo total para estadísticas
        self.__sistema.set_tiempo_total(self.__tiempo_total)
        
        # calcular estadísticas finales
        return self.__sistema.calcular_estadisticas()
    
    def __calcular_tiempo_proximo_evento(self, tiempo_actual: float, indice_persona: int) -> float:
        # determina cuándo ocurrirá el próximo evento relevante
        eventos = []
        
        # próxima llegada de cliente
        if indice_persona < len(self.__personas):
            eventos.append(self.__personas[indice_persona].get_tiempo_llegada())
        
        # próxima liberación de estación
        for estacion in self.__sistema.get_estaciones():
            if estacion.get_persona_actual() is not None:
                eventos.append(estacion.get_tiempo_fin_atencion())
        
        # si no hay más eventos, terminar simulación
        if not eventos:
            return self.__tiempo_total + 1
        
        # avanzar al tiempo del próximo evento
        return min(eventos)


def ejecutar_comparacion():
    # parámetros de simulación
    num_estaciones = 0
    while num_estaciones < 1 or num_estaciones > 3:
        try:
            num_estaciones = int(input("Ingrese número de estaciones (1-3): "))
        except ValueError:
            print("Por favor ingrese un número válido entre 1 y 3.")
    
    # ejecutar ambas variantes
    # variante 1: todas las estaciones genéricas
    simulador_1 = Simulador(num_estaciones, False)
    tiempo_espera_1, max_cola_1, ocupacion_1 = simulador_1.ejecutar_simulacion()
    
    # variante 2: una estación exclusiva para prioridad
    if num_estaciones > 1:  # solo si hay más de 1 estación
        simulador_2 = Simulador(num_estaciones, True)
        tiempo_espera_2, max_cola_2, ocupacion_2 = simulador_2.ejecutar_simulacion()
        
        # mostrar resultados
        print("\nResultados de la simulación:")
        print(f"Simulación con estaciones genéricas: Tiempo espera promedio: {tiempo_espera_1:.2f} min, "
              f"Longitud máxima cola: {max_cola_1}, Ocupación: {ocupacion_1:.2f}%")
        print(f"Simulación con 1 estación exclusiva para prioridad: Tiempo espera promedio: {tiempo_espera_2:.2f} min, "
              f"Longitud máxima cola: {max_cola_2}, Ocupación: {ocupacion_2:.2f}%")
    else:
        # mostrar resultados
        print("\nResultados de la simulación:")
        print(f"Simulación con estaciones genéricas: Tiempo espera promedio: {tiempo_espera_1:.2f} min, "
              f"Longitud máxima cola: {max_cola_1}, Ocupación: {ocupacion_1:.2f}%")


if __name__ == "__main__":
    ejecutar_comparacion()