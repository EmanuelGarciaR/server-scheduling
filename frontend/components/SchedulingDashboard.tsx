"use client"

import { useState } from "react"
import { TaskInput, Algorithm } from "@/lib/types_api"
import TaskCreationForm from "./TaskCreationForm"
import AlgorithmSelector from "./AlgorithmSelector"

export default function SchedulingDashboard() {
  const [tasks, setTasks] = useState<TaskInput[]>([])
  const [numServers, setNumServers] = useState<number>(2)
  const [algorithm, setAlgorithm] = useState<Algorithm>("greedy")

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
    </div>
  )
}
