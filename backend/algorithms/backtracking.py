"""
Backtracking para el problema de Scheduling de Servidores.

Complejidad Temporal: O(m^n) en el peor caso, pero en la práctica mucho
                      menor gracias a la poda (pruning).
    - m = número de servidores
    - n = número de tareas

Complejidad Espacial: O(n) por la pila de recursión + vector de asignación.

Descripción:
    Explora el espacio de soluciones de forma recursiva, asignando una tarea
    a la vez a cada servidor posible. La diferencia clave frente a fuerza bruta
    es la PODA: si en cualquier punto de la recursión el makespan parcial ya
    iguala o supera la mejor solución conocida, se descarta esa rama entera
    sin explorarla.

    Adicionalmente se aplica una poda por simetría: si dos servidores tienen
    exactamente la misma carga, solo se prueba asignar la tarea a uno de ellos,
    ya que asignarla al otro produciría un resultado idéntico.

    Respeta dependencias (predecessor_id) y prioridades (priority).
"""


def backtracking(tasks, servers):
    """
    Asigna tareas a servidores usando backtracking con poda.

    Parámetros:
        tasks   – Lista de objetos Task, pre-ordenados por dependency_level.
        servers – Lista de objetos Server disponibles.

    Retorna:
        servers – Los mismos servidores, con la asignación óptima aplicada.
    """
    n = len(tasks)
    m = len(servers)

    if n == 0:
        return servers

    task_dict = {t.get_id(): t for t in tasks}

    # best_makespan: cota superior actual. Cualquier rama con makespan >=
    # a este valor se descarta inmediatamente.
    best_makespan = float('inf')

    # best_assignment[i] = índice del servidor asignado a la tarea i
    # en la mejor solución encontrada hasta el momento.
    best_assignment = [0] * n

    # current_assignment: vector de trabajo que se modifica en cada nivel
    # de la recursión.
    current_assignment = [0] * n

    # --------------------------------------------------------------------------
    # Función recursiva principal.
    #   idx: índice de la tarea actual que estamos intentando asignar.
    # --------------------------------------------------------------------------
    def solve(idx):
        nonlocal best_makespan

        #  Caso base: todas las tareas han sido asignadas 
        if idx == n:
            makespan = max(s.total_load for s in servers)
            if makespan < best_makespan:
                best_makespan = makespan
                # Guardar copia del vector de asignación actual.
                best_assignment[:] = current_assignment[:]
            return

        task = tasks[idx]

        # Calcular cuándo termina el predecesor (restricción de dependencia).
        pred_finish = 0.0
        if task.predecessor_id:
            pred = task_dict.get(task.predecessor_id)
            if pred:
                pred_finish = pred.finish_time

        # Conjunto de cargas ya probadas en este nivel de recursión.
        # Poda por simetría: si dos servidores tienen la misma carga,
        # asignar la tarea a cualquiera de los dos produce resultados
        # equivalentes, así que solo probamos uno.
        tried_loads = set()

        for j in range(m):
            server = servers[j]

            #  Poda por simetría 
            if server.total_load in tried_loads:
                continue
            tried_loads.add(server.total_load)

            # El inicio real respeta tanto la disponibilidad del servidor
            # como la finalización del predecesor.
            start_time = max(server.total_load, pred_finish)
            finish_time = start_time + task.task_time

            #  Poda por cota (bound) 
            # Si esta tarea ya produce un finish_time >= al mejor makespan
            # conocido, no tiene sentido seguir explorando esta rama.
            if finish_time >= best_makespan:
                continue

            #  Asignar la tarea (avanzar) 
            current_assignment[idx] = j
            server.add_task(task, start_time=start_time)

            #  Recursión: intentar asignar la siguiente tarea 
            solve(idx + 1)

            #  Deshacer la asignación (backtrack) 
            server.remove_task(task)

    # Iniciar la búsqueda recursiva desde la primera tarea.
    solve(0)

    # Reconstruir la mejor solución sobre los servidores reales.
    for s in servers:
        s.clear()
    for t in tasks:
        t.start_time = 0.0
        t.finish_time = 0.0

    for i, task in enumerate(tasks):
        server = servers[best_assignment[i]]

        pred_finish = 0.0
        if task.predecessor_id:
            pred = task_dict.get(task.predecessor_id)
            if pred:
                pred_finish = pred.finish_time

        start_time = max(server.total_load, pred_finish)
        server.add_task(task, start_time=start_time)

    return servers