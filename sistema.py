from persona import Persona
from estacion import Estacion
from typing import List, Optional, Tuple
import numpy as np
import random

class SistemaColas:
    def __init__(self, num_estaciones: int, tiene_estacion_exclusiva: bool):
        # inicialización del sistema
        self.__estaciones: List[Estacion] = []
        self.__cola_prioridad: List[Persona] = []  # cola para personas con alta prioridad
        self.__cola_normal: List[Persona] = []  # cola para personas con baja prioridad
        self.__personas_atendidas: List[Persona] = []  # historial de personas atendidas
        self.__max_longitud_cola = 0  # longitud máxima alcanzada por las colas
        self.__tiempo_total = 0  # tiempo total de simulación
        
        # crear estaciones según configuración
        for i in range(num_estaciones):
            es_exclusiva = tiene_estacion_exclusiva and i == 0
            self.__estaciones.append(Estacion(i, es_exclusiva))
    
    # getters
    def get_estaciones(self) -> List[Estacion]:
        return self.__estaciones
    
    def get_cola_prioridad(self) -> List[Persona]:
        return self.__cola_prioridad
    
    def get_cola_normal(self) -> List[Persona]:
        return self.__cola_normal
    
    def get_personas_atendidas(self) -> List[Persona]:
        return self.__personas_atendidas
    
    def get_max_longitud_cola(self) -> int:
        return self.__max_longitud_cola
    
    # métodos operativos
    def agregar_persona(self, persona: Persona) -> None:
        # agrega una persona a la cola correspondiente
        if persona.es_alta_prioridad():
            self.__cola_prioridad.append(persona)
        else:
            self.__cola_normal.append(persona)
        
        # actualizar longitud máxima de cola
        longitud_actual = len(self.__cola_prioridad) + len(self.__cola_normal)
        if longitud_actual > self.__max_longitud_cola:
            self.__max_longitud_cola = longitud_actual
    
    def hay_persona_esperando(self) -> bool:
        # verifica si hay personas esperando en alguna cola
        return len(self.__cola_prioridad) > 0 or len(self.__cola_normal) > 0
    
    def asignar_personas_a_estaciones(self, tiempo_actual: float) -> None:
        # intenta asignar personas a estaciones disponibles
        for estacion in self.__estaciones:
            if not estacion.esta_disponible(tiempo_actual):
                continue
            
            # liberar la estación si tenía a alguien
            persona_terminada = estacion.liberar(tiempo_actual)
            if persona_terminada:
                self.__personas_atendidas.append(persona_terminada)
            
            # buscar siguiente persona para atender
            persona_a_atender = self.__obtener_siguiente_persona(estacion)
            if persona_a_atender:
                estacion.atender_persona(persona_a_atender, tiempo_actual)
    
    def __obtener_siguiente_persona(self, estacion: Estacion) -> Optional[Persona]:
        # determina la siguiente persona a ser atendida según las reglas
        
        # si es estación exclusiva para prioridad
        if estacion.es_exclusiva_prioridad():
            if len(self.__cola_prioridad) > 0:
                return self.__cola_prioridad.pop(0)
            return None
        
        # para estaciones genéricas, primero atender prioritarios
        if len(self.__cola_prioridad) > 0:
            # verificar si hay alguna estación exclusiva disponible
            hay_estacion_exclusiva = any(e.es_exclusiva_prioridad() for e in self.__estaciones)
            
            # si hay estación exclusiva, las personas con prioridad deben ir ahí
            if hay_estacion_exclusiva:
                return None
            return self.__cola_prioridad.pop(0)
        
        # si no hay prioritarios, atender personas normales
        if len(self.__cola_normal) > 0:
            return self.__cola_normal.pop(0)
        
        return None
    
    def calcular_estadisticas(self) -> Tuple[float, int, float]:
        # calcula las estadísticas finales de la simulación
        if not self.__personas_atendidas:
            return 0, 0, 0
        
        # calcular tiempo promedio de espera
        tiempo_espera_total = sum(p.get_tiempo_espera() for p in self.__personas_atendidas)
        tiempo_promedio_espera = tiempo_espera_total / len(self.__personas_atendidas)
        
        # calcular tasa de ocupación
        tiempo_total_servicio = sum(e.get_tiempo_total_servicio() for e in self.__estaciones)
        tiempo_total_disponible = self.__tiempo_total * len(self.__estaciones)
        ocupacion = (tiempo_total_servicio / tiempo_total_disponible) * 100 if tiempo_total_disponible > 0 else 0
        
        return tiempo_promedio_espera, self.__max_longitud_cola, ocupacion
    
    def set_tiempo_total(self, tiempo: float) -> None:
        self.__tiempo_total = tiempo

