# Entrega 3: Divide y Vencerás y Conclusiones Finales

## 1. Solución Divide y Vencerás

El algoritmo `divide_conquer.py` aplica el paradigma de Divide y Vencerás particionando la lista de tareas recursivamente hasta llegar a problemas triviales de una sola tarea. Al igual que Greedy, es una solución heurística (aproximada), pero el particionamiento le permite gestionar dependencias asegurando que los subproblemas se resuelvan en el orden correcto.

### Fases del Algoritmo (Reflejado en el Código)

Antes de iniciar la recursión, el algoritmo prepara el terreno ordenando las tareas. Esto es clave porque garantiza que los predecesores siempre queden en la mitad izquierda al momento de dividir.

```python
    # Pre-procesamiento: Ordenamiento por prioridad
    sorted_tasks = sorted(
        tasks,
        key=lambda t: (t.dependency_level, -(t.priority or 0))
    )
    _schedule(sorted_tasks) # Llamada a la función recursiva
```

Dentro de la función interna recursiva `_schedule(task_list)`, podemos identificar explícitamente las tres fases clásicas:

#### A. Fase de División
Se divide el arreglo a la mitad. Como las tareas vienen ordenadas, se asegura matemáticamente que ningún elemento en la mitad derecha `right_half` es predecesor de un elemento en `left_half`.
```python
        # ── Paso DIVIDIR ──
        mid = len(task_list) // 2
        left_half = task_list[:mid]
        right_half = task_list[mid:]
```

#### B. Fase de Conquista
Se resuelven los subproblemas recursivamente. El orden estricto de ejecución (primero izquierda, luego derecha) es lo que respeta la restricción de `dependency_level`.
```python
        # ── Paso CONQUISTAR ──
        _schedule(left_half)   # Se procesan los predecesores primero
        _schedule(right_half)  # Se procesan los dependientes
```
El **caso base** de esta conquista ocurre cuando `len(task_list) == 1`. En ese instante, se realiza la misma decisión de tipo *greedy* para la tarea individual: encontrar el servidor disponible más temprano.
```python
        # ── Caso base: una sola tarea ──
        if len(task_list) == 1:
            task = task_list[0]
            # ...
            server = min(servers, key=lambda s: (max(s.total_load, pred_finish), s.total_load))
            server.add_task(task, start_time=max(server.total_load, pred_finish))
            return
```

#### C. Fase de Combinación
```python
        # ── Paso COMBINAR ──
        # (Sin código explícito)
```
En este problema particular, el paso de "Combinar" es **implícito** y toma tiempo $O(1)$. No hace falta hacer un `merge` de resultados (como en *MergeSort*) porque ambas ramas operan, por referencia, sobre la misma lista global de objetos `Server`. Cuando `left_half` termina, los servidores tienen su `total_load` actualizado. Cuando entra `right_half`, los servidores conservan dicha carga.

### Aplicación del Teorema Maestro

El Teorema Maestro se utiliza para calcular la complejidad de la función recursiva `_schedule(n)`.
La recurrencia se define como:
$$T(n) = aT(n/b) + f(n)$$

Donde:
- $a = 2$ (se hacen dos llamadas recursivas).
- $b = 2$ (el problema se divide a la mitad).
- $f(n) = O(m)$ (donde $m$ son los servidores, evaluados en el caso base mediante `min()`. Al no depender de $n$, se considera $O(1)$ constante respecto al crecimiento de $n$).

Calculamos $n^{\log_b a} = n^{\log_2 2} = n^1 = O(n)$.
Como $f(n) = O(1)$, estamos en el **Caso 1** del Teorema Maestro: $f(n)$ es polinomialmente menor que $n^{\log_b a}$.
Por lo tanto, la complejidad de la recursión pura es **$T(n) = \Theta(n)$**. Multiplicado por el costo en cada hoja, es $O(n \cdot m)$.

Sin embargo, recordemos que antes de iniciar la recursión se realiza un `sorted_tasks = sorted(...)`, cuyo costo es $O(n \log n)$. 
**Complejidad Total**: $O(n \log n + n \cdot m)$. El docstring lo abstrae a $O(n \log n)$.

---

## 2. Comparativa Final (Empírica)

Utilizando los datos consolidados en `results.json` con la prueba `medium` (n=20) y `large` (n=100), obtenemos la siguiente perspectiva sobre la escalabilidad de cada técnica.

| Técnica | Complejidad Temporal | Complejidad Espacial | ¿Óptima? | Tiempo n=20 | Tiempo n=100 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fuerza Bruta** | $O(m^n \cdot n)$ | $O(n)$ | Sí | TIMEOUT | TIMEOUT |
| **Recursiva** | $O(m^n)$ | $O(n)$ | Sí | TIMEOUT | TIMEOUT |
| **Backtracking** | $O(m^n)$ | $O(n)$ | Sí | TIMEOUT | TIMEOUT |
| **Greedy** | $O(n \cdot m)$ | $O(n)$ | No | $0.000082$ s | $0.000537$ s |
| **Divide y Vencerás**| $O(n \log n)$ | $O(n \log n)$ | No | $0.000108$ s | $0.000885$ s |

*Nota: Los valores TIMEOUT se dispararon automáticamente en el script `runner.py` para evitar que la máquina quedara colgada infinitamente evaluando miles de millones de combinaciones para n=20.*

---

## 3. Gráfica de Tiempos y Escalabilidad

Al analizar el gráfico **`execution_time_vs_tasks.png`** generado, la distinción de escalabilidad es evidente:

1. **Explosión Combinatoria**: Las curvas de `brute_force`, `recursive` y `backtracking` son completamente invisibles en la escala de $n=20$ y $n=100$. Esto prueba gráficamente la naturaleza intratable de los algoritmos de tiempo exponencial ($O(m^n)$) frente al crecimiento lineal de los datos.
2. **Escalabilidad Lineal-Logarítmica**: Las curvas verde (`greedy`) y azul (`divide_conquer`) cruzan la gráfica a lo largo del eje X, manteniendo tiempos por debajo del milisegundo incluso con $100$ tareas. Demuestran un comportamiento estable y una pendiente muy suave en escala logarítmica.

---

## 4. Conclusiones Generales

### Selección de Algoritmo por Escenario
1. **Divide y Vencerás / Greedy (Aproximados)**:
   - **Aplicación en el Mundo Real**: Son los algoritmos indicados para servicios en la nube de alta concurrencia (como orquestadores estilo Kubernetes o AWS Lambda), donde el número de tareas y servidores es inmenso y dinámico (ej. miles por minuto).
   - **Justificación**: Producen tiempos de latencia menores a 1 milisegundo ($0.0005$ s). Aunque el balance final (makespan) pueda ser un poco ineficiente (ej. 552 frente al ideal 511), el costo computacional ahorrado por no ejecutar un algoritmo exponencial es invaluable.

2. **Backtracking (Exactos)**:
   - **Aplicación en el Mundo Real**: Resultan ideales para simulaciones de supercómputo y tareas astronómicas de un solo disparo (ej. agendar el tiempo del Telescopio James Webb entre distintos proyectos científicos).
   - **Justificación**: En este contexto, el `n` suele ser pequeño (pocas tareas gigantescas), pero la eficiencia operativa cuesta millones de dólares diarios. Pagar el costo exponencial de ejecución vale la pena para garantizar matemáticamente que el clúster estará aprovechado con el `makespan` mínimo absoluto y cero desperdicio.

### Limitaciones Encontradas
1. **Intratabilidad**: La mayor limitación de la implementación de `backtracking` es que, a pesar de las optimizaciones de poda por simetría y cuota superior, sigue cediendo rápidamente ante el crecimiento exponencial (`n=20` probó ser un límite infranqueable para ser evaluado en segundos). 
2. **Dependencias secuenciales**: La necesidad de mantener el orden por dependencias neutraliza parte del poder del Teorema Maestro en el algoritmo "Divide y Vencerás", ya que las mitades no pueden resolverse de forma puramente independiente o en paralelo; la mitad derecha depende invariablemente de los resultados calculados sobre los servidores en la mitad izquierda.
