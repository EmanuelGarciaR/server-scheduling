"use client"

import { useState, useEffect } from "react"
import { TaskInput, Algorithm, ScheduleResult, fetchSchedule } from "@/lib/types_api"
import TaskCreationForm from "./TaskCreationForm"
import AlgorithmSelector from "./AlgorithmSelector"
import ServerGrid from "./ServerGrid"
import { useSimulation } from "../hooks/useSimulation"

export default function SchedulingDashboard() {
  const [tasks, setTasks] = useState<TaskInput[]>([])
  const [numServers, setNumServers] = useState<number>(2)
  const [algorithm, setAlgorithm] = useState<Algorithm>("greedy")

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<ScheduleResult | null>(null)

  const simulation = useSimulation(result ? result.max_load : 0)

  // Reset simulation when result changes
  useEffect(() => {
    if (result) {
      simulation.reset()
    }
  }, [result])

  const handleAddTask = (task: TaskInput) => {
    setTasks((prev) => [...prev, task])
  }

  const handleRemoveTask = (id: string) => {
    setTasks((prev) => prev.filter((t) => t.id !== id))
    // Also we should remove predecessor references if a task is deleted
    setTasks((prev) =>
      prev.map((t) => (t.predecessor_id === id ? { ...t, predecessor_id: null } : t))
    )
  }

  const handleRunSchedule = async () => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await fetchSchedule({
        algorithm,
        num_servers: numServers,
        tasks,
      })
      setResult(data)
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <AlgorithmSelector selected={algorithm} onSelect={setAlgorithm} />
      
      <TaskCreationForm
        tasks={tasks}
        onAddTask={handleAddTask}
        onRemoveTask={handleRemoveTask}
        numServers={numServers}
        onChangeNumServers={setNumServers}
      />

      <section className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-neutral-800 dark:text-neutral-200">
              Run Scheduler
            </h2>
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              Execute the <span className="font-semibold text-neutral-700 dark:text-neutral-300 capitalize">{algorithm.replace("_", " ")}</span> algorithm with {numServers} server{numServers > 1 ? "s" : ""} and {tasks.length} task{tasks.length !== 1 ? "s" : ""}.
            </p>
          </div>
          <button
            onClick={handleRunSchedule}
            disabled={isLoading || tasks.length === 0}
            className={`px-6 py-3 font-semibold rounded-lg transition-all ${
              isLoading || tasks.length === 0
                ? "bg-neutral-200 dark:bg-neutral-800 text-neutral-400 dark:text-neutral-600 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg active:scale-95"
            }`}
          >
            {isLoading ? "Running..." : "Run Schedule"}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
            <strong>Error:</strong> {error}
          </div>
        )}
        
        {result && !error && (
          <div className="mt-6 flex flex-col gap-6">
            <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg text-emerald-700 dark:text-emerald-400 text-sm">
              Success! Scheduler finished in {(result.execution_time * 1000).toFixed(2)}ms with a makespan of {result.max_load}.
            </div>
            
            <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-md font-semibold text-neutral-800 dark:text-neutral-200 mb-1">
                    Simulation ({simulation.simulationTime} / {result.max_load}u)
                  </h3>
                  <p className="text-xs text-neutral-500">Visualize task execution across servers</p>
                </div>
                
                <div className="flex items-center gap-3">
                  <div className="flex items-center bg-neutral-100 dark:bg-neutral-800 rounded-lg p-1">
                    {[1, 2, 4].map((speed) => (
                      <button
                        key={speed}
                        onClick={() => simulation.setSpeed(speed)}
                        className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                          simulation.speedMultiplier === speed
                            ? 'bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white shadow-sm'
                            : 'text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300'
                        }`}
                      >
                        {speed}x
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={simulation.isSimulating ? simulation.pause : simulation.play}
                    disabled={simulation.simulationTime >= result.max_load && !simulation.isSimulating}
                    className="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {simulation.isSimulating ? (
                      <span className="font-bold text-lg leading-none mb-1">||</span>
                    ) : (
                      <span className="ml-1 font-bold text-sm">▶</span>
                    )}
                  </button>
                  
                  <button
                    onClick={simulation.reset}
                    className="px-3 py-2 text-sm font-medium text-neutral-600 dark:text-neutral-300 bg-neutral-100 hover:bg-neutral-200 dark:bg-neutral-800 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  >
                    Reset
                  </button>
                </div>
              </div>

              <ServerGrid result={result} simulationState={simulation.state} />
            </div>
          </div>
        )}
      </section>
    </div>
  )
}
