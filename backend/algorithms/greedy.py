"""
Algoritmo Greedy (Voraz) para el problema de Scheduling de Servidores.

Complejidad Temporal: O(n * m)
    - n = número de tareas
    - m = número de servidores
    - Para cada una de las n tareas, se evalúan los m servidores para encontrar el mejor.

Complejidad Espacial: O(n)
    - Se utiliza un diccionario auxiliar (task_dict) para almacenar las n tareas
      y así buscar los predecesores en tiempo O(1).

Descripción:
    Toma decisiones locales óptimas en cada paso con la esperanza de encontrar
    un buen óptimo global. Para cada tarea (las cuales ya vienen pre-ordenadas
    por dependency_level desde el scheduler principal), evalúa todos los servidores.
    
    Elige el servidor que permita que la tarea comience lo más pronto posible,
    respetando que no puede iniciar hasta que su predecesor haya terminado.
    En caso de empate (varios servidores pueden empezar al mismo tiempo),
    elige el servidor con menor carga total acumulada para balancear el trabajo.

    Es un enfoque heurístico: muy rápido pero NO garantiza la solución óptima
    (makespan mínimo) a diferencia de Fuerza Bruta o Backtracking.
"""

def greedy(tasks, servers):
    """
    Asigna tareas a servidores de forma voraz.

    Parámetros:
        tasks   – Lista de objetos Task, pre-ordenados por dependency_level.
        servers – Lista de objetos Server disponibles.

    Retorna:
        servers – Los mismos servidores con las tareas asignadas.
    """
    # Diccionario para buscar rápidamente el objeto predecesor en O(1)
    task_dict = {t.get_id(): t for t in tasks}

    for task in tasks:
        # 1. Determinar cuándo termina el predecesor de esta tarea (si lo tiene)
        pred_finish_time = 0.0
        if task.predecessor_id:
            pred_task = task_dict.get(task.predecessor_id)
            if pred_task:
                pred_finish_time = pred_task.finish_time
        
        # 2. Elegir el mejor servidor para esta tarea.
        #    Criterio primario: el servidor que permita el menor tiempo de inicio real
        #                       (el inicio real es max(carga_del_servidor, fin_del_predecesor)).
        #    Criterio secundario (desempate): el servidor con menor carga total.
        server = min(servers, key=lambda s: (max(s.total_load, pred_finish_time), s.total_load))
        
        # 3. Calcular el tiempo de inicio real y asignar la tarea
        start_time = max(server.total_load, pred_finish_time)
        server.add_task(task, start_time=start_time)
        
    return servers