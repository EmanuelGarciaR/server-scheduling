def greedy(tasks, servers):
    for task in tasks:
        server = min(servers, key=lambda s: s.total_load)
        server.add_task(task)
    return servers