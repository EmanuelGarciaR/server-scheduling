# Entrega 1: Definición del Problema y Algoritmos Exactos Básicos

## 1. Definición del Problema

### Descripción del caso de uso
El problema a resolver consiste en el **Scheduling de Servidores** (planificación de tareas). El objetivo es asignar un conjunto de tareas computacionales a múltiples servidores de forma que se minimice el tiempo total requerido para completar todas las tareas. Este tiempo total máximo se conoce como **makespan**.

### Entradas
- **Número de servidores**: Cantidad de servidores disponibles en el clúster.
- **Lista de tareas**: Colección de objetos donde cada tarea tiene:
  - `id`: Identificador único.
  - `task_time`: Tiempo de ejecución requerido.
  - `priority` (opcional): Nivel de prioridad.
  - `predecessor_id` (opcional): ID de otra tarea que debe terminar antes de que esta pueda comenzar.

### Salidas
- **Asignación de tareas**: Lista de servidores con las tareas asignadas a cada uno y sus tiempos de inicio/fin.
- **Makespan resultante**: La carga máxima final entre todos los servidores (tiempo de finalización global).
- **Tiempo de cómputo**: Tiempo que tardó el algoritmo en encontrar la solución.

### Restricciones
- **Dependencias**: Una tarea no puede iniciar hasta que su predecesor (si lo tiene) haya finalizado.
- **Capacidad**: Aunque en este escenario los servidores se consideran de capacidad teóricamente infinita (en cuanto a memoria o carga acumulada temporal), no se puede exceder la capacidad máxima si esta estuviera restringida.
- **Objetivo**: Minimizar el *makespan* global.

### Casos de prueba
Para validar las soluciones, se usan tres escenarios con parámetros reales extraídos de los archivos JSON:
- **Small (`small.json`)**: 5 tareas y 3 servidores. Makespan óptimo esperado: 24.
- **Medium (`medium.json`)**: 20 tareas y 5 servidores. Makespan óptimo esperado: 176.
- **Large (`large.json`)**: 100 tareas y 10 servidores. Makespan óptimo esperado: 511.

---

## 2. Solución por Fuerza Bruta

La implementación en `backend/algorithms/brute_force.py` resuelve el problema explorando exhaustivamente el espacio de soluciones. Enumera absolutamente todas las formas posibles de asignar las tareas a los servidores y luego simula cada combinación para encontrar la que arroja el menor makespan.

### Funcionamiento paso a paso
1. **Generación de combinaciones**: Utiliza la función `product` de `itertools` para generar todas las tuplas posibles de longitud $n$ (tareas) con valores entre $0$ y $m-1$ (servidores). Cada tupla representa un vector de asignación.
2. **Simulación (`simulate`)**: Para cada vector generado, se iteran las tareas en orden (ya pre-ordenadas por `dependency_level`). 
3. **Manejo de dependencias**: Al simular, se calcula el inicio real de la tarea como `max(server.total_load, predecesor_finish_time)`.
4. **Actualización del óptimo**: Si la simulación produce un makespan menor al `best_makespan` global, se actualiza la mejor asignación.
5. **Reconstrucción**: Al finalizar el ciclo, se corre `simulate(best_assignment)` una última vez para reflejar la mejor distribución en los objetos `Server` originales.

### Fragmento de Código (Core Logic)
```python
    # Enumeración exhaustiva: itertools.product genera todas las tuplas
    # de longitud n con valores en {0, 1, ..., m-1}.
    for assignment in product(range(m), repeat=n):
        makespan = simulate(assignment)

        if makespan < best_makespan:
            best_makespan = makespan
            best_assignment = assignment

    # Reconstruir la mejor solución encontrada sobre los servidores reales.
    simulate(best_assignment)
```

---

## 3. Análisis de Complejidad — Fuerza Bruta

### Complejidad Temporal
- **Generación de vectores**: Existen $m^n$ formas distintas de asignar $n$ tareas a $m$ servidores.
- **Simulación**: Para cada una de las $m^n$ combinaciones, la función `simulate` itera sobre las $n$ tareas, tomando un tiempo $O(n)$.
- **Complejidad total**: $O(m^n \cdot n)$. Es un tiempo exponencial, lo que lo hace impráctico para cualquier caso que supere las $\sim15$ tareas.

### Complejidad Espacial
- No se guardan todas las combinaciones en memoria simultáneamente, sino que `product` las genera como un iterador. Solo se guardan el vector actual y `best_assignment`, que tienen un tamaño $n$.
- **Complejidad total**: $O(n)$, muy eficiente en memoria a costa del tiempo de CPU.

### Mediciones Empíricas
Al ejecutar `runner.py`, los resultados reales para Fuerza Bruta fueron:
- **Small (n=5, m=3)**: Tiempo promedio de $\approx 0.0019$ segundos. Alcanzó el makespan óptimo perfecto (24).
- **Medium (n=20, m=5)**: TIMEOUT. Se descarta la ejecución porque $5^{20}$ evaluaciones tomarían más tiempo del factible computacionalmente.
- **Large (n=100, m=10)**: TIMEOUT ($10^{100}$ combinaciones).

*(Refiérase a la gráfica `execution_time_vs_tasks.png` generada en Chart 1, donde se observa cómo los algoritmos exactos colapsan antes de llegar a la escala de medium).*

---

## 4. Solución Recursiva

La solución implementada en `backend/algorithms/recursive.py` realiza la misma búsqueda exhaustiva, pero utilizando la pila de llamadas (call stack) para construir el árbol de decisiones de manera recursiva, evaluando rama por rama sin necesidad de generar vectores mediante `itertools`. A diferencia del backtracking, no aplica podas (pruning).

### Identificación de los casos
- **Caso Recursivo**: En la función anidada `solve(idx)`, se toma la tarea en la posición `idx` y se intenta iterativamente asignarla a cada uno de los $m$ servidores. Por cada asignación temporal, se hace la llamada recursiva `solve(idx + 1)` para resolver el subproblema de las tareas restantes.
- **Caso Base**: Ocurre cuando `idx == n` (todas las tareas han sido procesadas). En ese momento, se calcula y retorna la carga máxima actual de los servidores `max(s.total_load for s in servers)` junto con una lista vacía que representa el final del vector de asignación.

### Fragmento de Código (Recursión)
```python
        #  Caso recursivo: probar cada servidor 
        for j in range(m):
            server = servers[j]
            start_time = max(server.total_load, pred_finish)
            
            # Asignar temporalmente y recurrir
            server.add_task(task, start_time=start_time)
            sub_makespan, sub_assignment = solve(idx + 1)
            server.remove_task(task) # Deshacer asignación

            # Actualizar la mejor solución
            if sub_makespan < best_makespan:
                best_makespan = sub_makespan
                best_server_idx = j
                best_sub_assignment = sub_assignment

        return (best_makespan, [best_server_idx] + best_sub_assignment)
```

### Análisis de Complejidad (Recursiva)
- **Temporal**: El árbol de recursión tiene una profundidad de $n$ y cada nodo tiene un factor de ramificación de $m$ (prueba $m$ servidores). Por tanto, se exploran $m^n$ hojas. A diferencia de iterar $O(n)$ en cada hoja como en fuerza bruta, aquí el cálculo se hace incrementalmente. La complejidad temporal es $O(m^n)$.
- **Espacial**: Ocupa $O(n)$ correspondiente a la profundidad máxima de la pila de llamadas del sistema (call stack) más el espacio para almacenar la mejor ruta encontrada.

### Tabla Comparativa: Fuerza Bruta vs Recursiva
Basado en las mediciones empíricas de `results.json`:

| Algoritmo | Tiempo `small` (n=5) | Tiempo `medium` (n=20) | ¿Makespan óptimo? |
| :--- | :--- | :--- | :--- |
| Fuerza Bruta | ~0.001932 s | TIMEOUT | Sí (24) |
| Recursivo | ~0.001608 s | TIMEOUT | Sí (24) |

*Ambos logran garantizar matemáticamente la respuesta makespan óptimo, pero sufren del mismo explosión combinatoria. La versión recursiva fue fraccionalmente más rápida en Python para el set `small` debido a que evita regenerar completamente el estado desde cero en cada validación.*
