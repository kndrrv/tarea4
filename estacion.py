from persona import Persona
from typing import Optional

class Estacion:
    def __init__(self, id: int, exclusiva_prioridad: bool = False):
        # inicialización de la estación
        self.__id = id  # identificador único de la estación
        self.__exclusiva_prioridad = exclusiva_prioridad  # si es exclusiva para alta prioridad
        self.__persona_actual = None  # persona siendo atendida actualmente
        self.__tiempo_fin_atencion = 0  # tiempo en que termina la atención actual
        self.__tiempo_total_servicio = 0  # acumulador del tiempo total de servicio
    
    # getters
    def get_id(self) -> int:
        return self.__id
    
    def es_exclusiva_prioridad(self) -> bool:
        return self.__exclusiva_prioridad
    
    def get_persona_actual(self) -> Optional[Persona]:
        return self.__persona_actual
    
    def get_tiempo_fin_atencion(self) -> float:
        return self.__tiempo_fin_atencion
    
    def get_tiempo_total_servicio(self) -> float:
        return self.__tiempo_total_servicio
    
    # métodos operativos
    def esta_disponible(self, tiempo_actual: float) -> bool:
        # verifica si la estación está disponible en el tiempo actual
        return self.__persona_actual is None or tiempo_actual >= self.__tiempo_fin_atencion
    
    def puede_atender(self, persona: Persona) -> bool:
        # verifica si esta estación puede atender a la persona según las reglas
        if self.__exclusiva_prioridad:
            # si es exclusiva, solo recibe personas de alta prioridad o si no hay nadie con prioridad
            return persona.es_alta_prioridad()
        else:
            # estación genérica puede atender a cualquiera
            return True
    
    def atender_persona(self, persona: Persona, tiempo_actual: float) -> None:
        # asigna una persona a esta estación
        self.__persona_actual = persona
        persona.set_tiempo_inicio_atencion(tiempo_actual)
        self.__tiempo_fin_atencion = tiempo_actual + persona.get_tiempo_servicio()
        persona.set_tiempo_fin_atencion(self.__tiempo_fin_atencion)
        persona.set_estacion_asignada(self)
        # acumular tiempo de servicio para estadísticas
        self.__tiempo_total_servicio += persona.get_tiempo_servicio()
    
    def liberar(self, tiempo_actual: float) -> Optional[Persona]:
        # libera la estación y retorna la persona que terminó
        if self.esta_disponible(tiempo_actual) and self.__persona_actual is not None:
            persona_terminada = self.__persona_actual
            self.__persona_actual = None
            return persona_terminada
        return None
    
    def __str__(self) -> str:
        # representación en texto de la estación
        tipo = "EXCLUSIVA" if self.__exclusiva_prioridad else "GENÉRICA"
        estado = "OCUPADA" if self.__persona_actual else "LIBRE"
        return f"Estación {self.__id} ({tipo}) - {estado}"


