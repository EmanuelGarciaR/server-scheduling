"""
Fuerza Bruta para el problema de Scheduling de Servidores.

Complejidad Temporal: O(m^n * n)
    - m = número de servidores
    - n = número de tareas
    - Se generan m^n asignaciones posibles y cada una se evalúa en O(n).

Complejidad Espacial: O(n)
    - Almacena el vector de asignación actual y el mejor encontrado.

Descripción:
    Enumera todas las posibles formas de asignar n tareas
    a m servidores. Para cada combinación, simula la planificación completa
    (respetando dependencias) y calcula el makespan resultante.
    Al finalizar, reconstruye la asignación que produjo el menor makespan.

    Garantiza encontrar la SOLUCIÓN ÓPTIMA, pero su costo exponencial lo
    hace impráctico para instancias grandes (n > ~15).
"""

from itertools import product


def brute_force(tasks, servers):
    """
    Asigna tareas a servidores evaluando TODAS las combinaciones posibles.

    Parámetros:
        tasks   – Lista de objetos Task, pre-ordenados por dependency_level.
        servers – Lista de objetos Server disponibles.

    Retorna:
        servers – Los mismos servidores, con la asignación óptima aplicada.
    """
    n = len(tasks)
    m = len(servers)

    # Caso trivial: sin tareas no hay nada que asignar.
    if n == 0:
        return servers

    # Diccionario de búsqueda rápida: id → Task.
    # Permite encontrar el finish_time de cualquier predecesor en O(1).
    task_dict = {t.get_id(): t for t in tasks}

    # Variables para rastrear la mejor solución global.
    best_makespan = float('inf')
    best_assignment = None

    # Función auxiliar: dado un vector de asignación, simula la planificación
    # completa y retorna el makespan resultante.
    def simulate(assignment):
        """
        Reconstruye una planificación a partir de un vector de asignación.

        assignment[i] = j  →  la tarea i se asigna al servidor j.

        Como las tareas ya están ordenadas por dependency_level, al iterar
        en orden garantizamos que cada predecesor ya fue procesado antes
        de su dependiente, por lo que pred.finish_time estará actualizado.
        """
        # 1. Limpiar el estado de todos los servidores.
        for s in servers:
            s.clear()

        # 2. Resetear los tiempos de cada tarea para evitar residuos
        #    de simulaciones anteriores.
        for t in tasks:
            t.start_time = 0.0
            t.finish_time = 0.0

        # 3. Asignar cada tarea respetando dependencias.
        for i, task in enumerate(tasks):
            server = servers[assignment[i]]

            # Buscar cuándo termina el predecesor (si existe).
            predecesor_finish_time = 0.0
            if task.predecessor_id:
                pred = task_dict.get(task.predecessor_id)
                if pred:
                    predecesor_finish_time = pred.finish_time

            # El inicio real = max(servidor libre, predecesor terminado).
            start = max(server.total_load, predecesor_finish_time)
            server.add_task(task, start_time=start)

        # 4. Makespan = la carga máxima entre todos los servidores.
        return max(s.total_load for s in servers)

    # Enumeración exhaustiva: itertools.product genera todas las tuplas
    # de longitud n con valores en {0, 1, ..., m-1}.
    # Cada tupla representa una asignación completa de tareas a servidores.
    for assignment in product(range(m), repeat=n):
        makespan = simulate(assignment)

        if makespan < best_makespan:
            best_makespan = makespan
            best_assignment = assignment


    # Reconstruir la mejor solución encontrada sobre los servidores reales.
    simulate(best_assignment)

    return servers
