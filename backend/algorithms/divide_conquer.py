"""
Divide y Vencerás para el problema de Scheduling de Servidores.

Complejidad Temporal: O(n log n)
    - n = número de tareas
    - En cada nivel de recursión se procesan todas las tareas del subproblema.
    - La profundidad de recursión es O(log n) por la división a la mitad.

Complejidad Espacial: O(n log n) por las copias de sublistas en la recursión.

Descripción:
    Aplica el paradigma de Divide y Vencerás al problema de planificación:

    1. DIVIDIR: Separar la lista de tareas en dos mitades.
       Como las tareas llegan pre-ordenadas por dependency_level, la mitad
       izquierda siempre contiene predecesores antes que sus dependientes.

    2. CONQUISTAR: Resolver recursivamente cada mitad, asignando las tareas
       de la sublista izquierda primero (garantizando que los predecesores
       ya tengan finish_time calculado antes de procesar sus dependientes).

    3. COMBINAR: La combinación es implícita — ambos subproblemas operan
       sobre los mismos servidores compartidos, por lo que al resolver la
       mitad izquierda los servidores acumulan carga que la mitad derecha
       observa al momento de asignar sus tareas.

    El caso base asigna una única tarea al servidor que minimice su tiempo
    de inicio efectivo, considerando tanto la carga del servidor como
    las restricciones de dependencia.

    Dentro de cada nivel se aplica una optimización por prioridad: las tareas
    con mayor prioridad se procesan primero (dentro del mismo dependency_level),
    asegurando que ocupen los servidores más libres.
"""


def divide_conquer(tasks, servers):
    """
    Asigna tareas a servidores usando Divide y Vencerás.

    Parámetros:
        tasks   – Lista de objetos Task, pre-ordenados por dependency_level.
        servers – Lista de objetos Server disponibles.

    Retorna:
        servers – Los mismos servidores con las tareas asignadas.
    """
    if not tasks:
        return servers

    # Diccionario para búsqueda rápida de predecesores.
    task_dict = {t.get_id(): t for t in tasks}

    # Función recursiva que implementa el patrón Divide y Vencerás.
    
    # Recibe una sublista de tareas y las asigna a los servidores
    # compartidos, respetando dependencias y prioridades.
    # --------------------------------------------------------------------------
    def _schedule(task_list):
        # ── Caso base 1: sublista vacía ──
        if not task_list:
            return

        # ── Caso base 2: una sola tarea ──
        # Asignarla directamente al servidor que permita el inicio más temprano.
        if len(task_list) == 1:
            task = task_list[0]

            # Restricción de dependencia: no iniciar antes de que el
            # predecesor haya terminado.
            pred_finish = 0.0
            if task.predecessor_id:
                pred = task_dict.get(task.predecessor_id)
                if pred:
                    pred_finish = pred.finish_time

            # Elegir el servidor que permita el inicio más temprano.
            # Criterio: min(max(carga_servidor, fin_predecesor)).
            # Desempate por carga total para balancear la distribución.
            server = min(
                servers,
                key=lambda s: (max(s.total_load, pred_finish), s.total_load)
            )

            start_time = max(server.total_load, pred_finish)
            server.add_task(task, start_time=start_time)
            return

        # ── Paso DIVIDIR ──
        # Partir la lista por la mitad. Gracias al orden por dependency_level,
        # los predecesores siempre estarán en la mitad izquierda o ya habrán
        # sido procesados en una llamada anterior.
        mid = len(task_list) // 2
        left_half = task_list[:mid]
        right_half = task_list[mid:]

        # ── Paso CONQUISTAR ──
        # Primero resolvemos la mitad izquierda: sus tareas se asignan a los
        # servidores, actualizando total_load y finish_time de cada tarea.
        _schedule(left_half)

        # Luego resolvemos la mitad derecha: estas tareas ven las cargas
        # actualizadas por la mitad izquierda, respetando así las dependencias
        # entre ambas mitades.
        _schedule(right_half)

        # ── Paso COMBINAR ──
        # La combinación es implícita: ambas mitades operan sobre los
        # mismos objetos Server, por lo que las asignaciones se acumulan
        # automáticamente. No se requiere un paso de merge explícito.

    # --------------------------------------------------------------------------
    # Optimización por prioridad: dentro del mismo dependency_level,
    # ordenar por prioridad descendente (mayor prioridad primero).
    # Esto asegura que las tareas más importantes se asignen antes,
    # cuando los servidores tienen más capacidad disponible.
    # --------------------------------------------------------------------------
    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t.dependency_level, -(t.priority or 0))
    )

    # Iniciar la recursión con la lista completa ordenada.
    _schedule(sorted_tasks)

    return servers
