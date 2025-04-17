from persona import Persona
from typing import List
import numpy as np
import random

def generar_personas(tiempo_total: float, lambda_llegadas: float, 
                    prob_prioridad: float, lambda_servicio: float) -> List[Persona]:
    # genera una lista de personas según los parámetros dados
    personas = []
    tiempo_actual = 0.0
    
    while tiempo_actual < tiempo_total:
        # tiempo entre llegadas sigue una distribución exponencial
        tiempo_entre_llegadas = np.random.exponential(1 / lambda_llegadas)
        tiempo_actual += tiempo_entre_llegadas
        
        if tiempo_actual >= tiempo_total:
            break
        
        # montecarlo para asignar prioridad
        prioridad = 0 if random.random() < prob_prioridad else 1
        
        # tiempo de servicio también exponencial
        tiempo_servicio = np.random.exponential(1 / lambda_servicio)
        
        personas.append(Persona(tiempo_actual, prioridad, tiempo_servicio))
    
    return personas
