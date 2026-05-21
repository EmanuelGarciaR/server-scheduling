# Entrega 2: Heurística Voraz y Backtracking

## 1. Solución Greedy

La solución implementada en `backend/algorithms/greedy.py` emplea una heurística voraz (greedy). Su filosofía es tomar la mejor decisión *local* en el momento presente, con la esperanza de que estas buenas decisiones individuales conduzcan a un buen resultado global. 

### Criterio Greedy Utilizado
El algoritmo toma las tareas secuencialmente (las cuales ya vienen ordenadas por nivel de dependencia). Para cada tarea, evalúa todos los servidores disponibles y elige aquel que cumpla el siguiente **criterio primario**: 
- **Minimizar el tiempo de inicio efectivo**: El inicio real está condicionado tanto por cuándo se desocupa el servidor como por cuándo termina el predecesor de la tarea. Por ende, se minimiza `max(carga_del_servidor, fin_del_predecesor)`.
- **Criterio secundario (desempate)**: Si varios servidores permiten iniciar al mismo tiempo, escoge el que tenga menor carga total acumulada (`total_load`), lo que ayuda a mantener el balance general.

### Fragmento de Código (Decisión Voraz)
```python
        # 2. Elegir el mejor servidor para esta tarea.
        #    Criterio primario: min(max(s.total_load, pred_finish_time))
        #    Criterio secundario: s.total_load
        server = min(
            servers, 
            key=lambda s: (max(s.total_load, pred_finish_time), s.total_load)
        )
        
        # 3. Calcular el tiempo de inicio real y asignar la tarea
        start_time = max(server.total_load, pred_finish_time)
        server.add_task(task, start_time=start_time)
```

### Análisis de Complejidad — Greedy
- **Temporal**: El bucle principal se ejecuta $n$ veces (una por cada tarea). En el interior del bucle, la función `min()` recorre la lista de $m$ servidores para encontrar el óptimo local. Buscar al predecesor toma $O(1)$ gracias al uso de un diccionario auxiliar `task_dict`. Por consiguiente, la complejidad temporal es exactamente **$O(n \cdot m)$**.
- **Espacial**: Ocupa **$O(n)$** adicional para el diccionario auxiliar `task_dict` utilizado para búsquedas rápidas.

### Análisis Crítico: ¿Es Greedy Óptimo?
**No**, la estrategia Greedy no garantiza encontrar el *makespan* mínimo para este problema. Al tomar decisiones irreversibles basadas únicamente en el estado local, Greedy puede quedarse atrapado en "óptimos locales".

**Contraejemplo concreto:**
Supongamos que tenemos $m=2$ servidores y $n=3$ tareas sin dependencias, en el siguiente orden:
- Tarea 1: tiempo = 2
- Tarea 2: tiempo = 2
- Tarea 3: tiempo = 3

*Ejecución Greedy:*
1. Evalúa T1 (2). Ambos servidores en 0. Asigna a Servidor 1. (Cargas: S1=2, S2=0).
2. Evalúa T2 (2). Servidor 2 inicia antes (0). Asigna a Servidor 2. (Cargas: S1=2, S2=2).
3. Evalúa T3 (3). Empate en inicio (2). Asigna a Servidor 1. (Cargas: S1=5, S2=2).
**Makespan de Greedy:** 5.

*Acomodo Óptimo Real:*
- Servidor 1 procesa T3 (carga = 3).
- Servidor 2 procesa T1 y T2 (carga = 2 + 2 = 4).
**Makespan Óptimo:** 4.

---

## 2. Solución Backtracking

La solución en `backend/algorithms/backtracking.py` mejora a la Fuerza Bruta y la versión Recursiva incorporando **podas (pruning)** al árbol de exploración. 

### Exploración del Espacio de Solución
Al igual que el algoritmo recursivo puro, intenta colocar secuencialmente la tarea actual en todos los servidores posibles. La diferencia radical es que lleva registro de la mejor solución (cota superior o *upper bound*) encontrada hasta el momento (`best_makespan`).

### Condiciones de Poda Utilizadas
1. **Poda por Cota (Bound Pruning)**:
   Antes de hacer la llamada recursiva, verifica si asignar la tarea actual provocaría que el `finish_time` en ese servidor iguale o supere el `best_makespan` ya conocido. Si es así, **toda esa rama se descarta inmediatamente** (`continue`).
2. **Poda por Simetría**:
   Mantiene un conjunto `tried_loads` en cada nivel de la recursión. Si dos o más servidores tienen idéntica carga actual, asignar la tarea a uno u otro generará sub-árboles exactamente idénticos (simétricos). Se prueba solo en uno de ellos y se ignoran los demás.

### Complejidad: Peor Caso vs Caso Promedio
- **Peor Caso**: Si la poda no entra en efecto (por ejemplo, si el árbol está ordenado de forma adversa y la cota superior tarda en ajustarse), la complejidad degenera a la de una búsqueda exhaustiva: **$O(m^n)$**.
- **Caso Promedio (con poda)**: En la práctica, las podas reducen drásticamente el espacio de búsqueda. Aunque sigue siendo asintóticamente exponencial, el algoritmo es capaz de resolver instancias significativamente mayores que Fuerza Bruta pura en fracciones de segundo.

---

## 3. Comparativa Parcial (Exactos vs Voraz)

La siguiente tabla resume los resultados empíricos obtenidos de `results.json` para los primeros 4 algoritmos:

| Técnica | Complejidad Temporal | Complejidad Espacial | ¿Óptima? | Tiempo `small` (n=5) | Tiempo `medium` (n=20) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fuerza Bruta** | $O(m^n \cdot n)$ | $O(n)$ | Sí | $\approx 0.00193$ s | TIMEOUT |
| **Recursiva** | $O(m^n)$ | $O(n)$ | Sí | $\approx 0.00160$ s | TIMEOUT |
| **Backtracking** | $O(m^n)$ (peor caso) | $O(n)$ | Sí | $\approx 0.00010$ s | TIMEOUT |
| **Greedy** | $O(n \cdot m)$ | $O(n)$ | No | $\approx 0.00002$ s | $\approx 0.00008$ s |

### Discusión de Compromisos (Trade-offs)
Los resultados exponen un compromiso fundamental entre el tiempo de cómputo y la calidad de la solución:
- **Tiempos Extraordinarios vs Optimalidad**: Mientras Backtracking resuelve el caso pequeño $19$ veces más rápido que Fuerza Bruta gracias a sus podas (0.00010s vs 0.00193s), ambos garantizan el makespan óptimo perfecto (24). Sin embargo, ambos fallan escalar (TIMEOUT) cuando $n=20$ debido al crecimiento exponencial.
- **Escalabilidad**: Greedy demostró ser el único capaz de procesar rápidamente (0.00008s) el escenario de $n=20$, pero su makespan final (209) dista significativamente del óptimo matemático (176). Greedy es la alternativa viable cuando el problema rebasa el límite de cómputo, aceptando un margen de ineficiencia operativa.
