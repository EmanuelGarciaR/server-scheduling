"""
Recursivo (Búsqueda Exhaustiva Recursiva) para Scheduling de Servidores.

Complejidad Temporal: O(m^n)
    - m = número de servidores
    - n = número de tareas
    - Explora TODAS las ramas sin poda (a diferencia de backtracking).

Complejidad Espacial: O(n) por la profundidad de la pila de recursión.

Descripción:
    Implementa una búsqueda exhaustiva puramente recursiva. Para cada tarea
    (procesada en orden de dependencia), se prueba asignarla a cada uno
    de los m servidores. La recursión retorna el mejor makespan alcanzable
    desde ese punto en adelante, junto con el vector de asignación óptimo.

    A diferencia de Backtracking, este algoritmo NO aplica ninguna poda:
    explora absolutamente todas las ramas del árbol de decisión. Esto lo
    hace conceptualmente más simple pero computacionalmente más costoso.

    A diferencia de Fuerza Bruta, la enumeración se realiza de forma
    recursiva (usando la pila de llamadas) en lugar de iterativa
    (usando itertools.product).

    Respeta dependencias (predecessor_id) y prioridades (priority).
"""


def recursive(tasks, servers):
    """
    Asigna tareas a servidores mediante búsqueda exhaustiva recursiva.

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

    # --------------------------------------------------------------------------
    # Función recursiva principal.
    #
    #   idx: índice de la tarea actual a asignar.
    #
    # Retorna:
    #   (mejor_makespan, mejor_vector_asignación)
    #
    # En cada nivel de recursión, se intenta asignar tasks[idx] a cada
    # servidor, se recurre para las tareas restantes, y se selecciona
    # la asignación que produce el menor makespan global.
    # --------------------------------------------------------------------------
    def solve(idx):
        #  Caso base: todas las tareas fueron asignadas 
        # El makespan actual es la carga máxima entre todos los servidores.
        if idx == n:
            makespan = max(s.total_load for s in servers)
            return (makespan, [])

        task = tasks[idx]

        # Restricción de dependencia: obtener el finish_time del predecesor.
        pred_finish = 0.0
        if task.predecessor_id:
            pred = task_dict.get(task.predecessor_id)
            if pred:
                pred_finish = pred.finish_time

        # Variables para rastrear la mejor opción en este nivel.
        best_makespan = float('inf')
        best_sub_assignment = []
        best_server_idx = 0

        #  Caso recursivo: probar cada servidor 
        for j in range(m):
            server = servers[j]

            # Calcular el tiempo de inicio real para esta tarea en este servidor.
            start_time = max(server.total_load, pred_finish)

            # Asignar la tarea temporalmente al servidor j.
            server.add_task(task, start_time=start_time)

            # Recurrir: resolver el subproblema con las tareas restantes.
            # La recursión retorna el mejor makespan alcanzable desde idx+1
            # en adelante, dado que tasks[idx] está en el servidor j.
            sub_makespan, sub_assignment = solve(idx + 1)

            # Deshacer la asignación para probar el siguiente servidor.
            server.remove_task(task)

            # Actualizar la mejor solución si esta rama es mejor.
            if sub_makespan < best_makespan:
                best_makespan = sub_makespan
                best_server_idx = j
                best_sub_assignment = sub_assignment

        # Retornar el mejor makespan y prepend la elección de este nivel.
        return (best_makespan, [best_server_idx] + best_sub_assignment)

    # Ejecutar la recursión desde la primera tarea.
    _, best_assignment = solve(0)

    # Reconstruir la solución óptima sobre los servidores reales.
    #
    # Es necesario reconstruir porque durante solve() se hacen y deshacen
    # múltiples asignaciones. Al finalizar, los servidores están vacíos.
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
