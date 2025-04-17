class Persona:
    def __init__(self, tiempo_llegada: float, prioridad: int, tiempo_servicio: float):
        # inicialización de la persona con sus atributos
        self.__tiempo_llegada = tiempo_llegada  # tiempo de llegada al sistema
        self.__prioridad = prioridad  # 0 es alta prioridad, 1 es baja prioridad
        self.__tiempo_servicio = tiempo_servicio  # tiempo que toma ser atendido
        self.__tiempo_inicio_atencion = -1  # cuando comienza a ser atendido
        self.__tiempo_fin_atencion = -1  # cuando termina de ser atendido
        self.__estacion_asignada = None  # estación donde fue atendido
    
    # getters para acceder a los atributos privados
    def get_tiempo_llegada(self) -> float:
        return self.__tiempo_llegada
    
    def get_prioridad(self) -> int:
        return self.__prioridad
    
    def get_tiempo_servicio(self) -> float:
        return self.__tiempo_servicio
    
    def get_tiempo_inicio_atencion(self) -> float:
        return self.__tiempo_inicio_atencion
    
    def get_tiempo_fin_atencion(self) -> float:
        return self.__tiempo_fin_atencion
    
    def get_estacion_asignada(self):
        return self.__estacion_asignada
    
    # setters para modificar los atributos privados
    def set_tiempo_inicio_atencion(self, tiempo: float):
        self.__tiempo_inicio_atencion = tiempo
    
    def set_tiempo_fin_atencion(self, tiempo: float):
        self.__tiempo_fin_atencion = tiempo
    
    def set_estacion_asignada(self, estacion):
        self.__estacion_asignada = estacion
    
    # métodos para cálculos
    def get_tiempo_espera(self) -> float:
        # tiempo de espera = cuando empieza a ser atendido - cuando llegó
        if self.__tiempo_inicio_atencion < 0:
            return 0
        return self.__tiempo_inicio_atencion - self.__tiempo_llegada
    
    def es_alta_prioridad(self) -> bool:
        # retorna true si es de alta prioridad (0)
        return self.__prioridad == 0
    
    def __str__(self) -> str:
        # representación en texto de la persona
        prioridad_str = "ALTA" if self.es_alta_prioridad() else "BAJA"
        return f"Persona[llegada = {self.__tiempo_llegada:.2f}, prioridad = {prioridad_str}, servicio = {self.__tiempo_servicio:.2f}]"