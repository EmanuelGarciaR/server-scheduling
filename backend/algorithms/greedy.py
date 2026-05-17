def greedy(tasks, servers):
    task_dict = {t.get_id(): t for t in tasks}

    for task in tasks:
        pred_finish_time = 0.0
        if task.predecessor_id:
            pred_task = task_dict.get(task.predecessor_id)
            if pred_task:
                pred_finish_time = pred_task.finish_time
        
        # Elegir el servidor que permita empezar la tarea lo más pronto posible.
        # Si hay empate, se elige el servidor con menor carga total para distribuir las tareas.
        server = min(servers, key=lambda s: (max(s.total_load, pred_finish_time), s.total_load))
        
        start_time = max(server.total_load, pred_finish_time)
        server.add_task(task, start_time=start_time)
        
    return servers