"use client"

import { useState } from "react"
import { TaskInput } from "@/lib/types_api"

interface TaskCreationFormProps {
  tasks: TaskInput[]
  onAddTask: (task: TaskInput) => void
  onRemoveTask: (id: string) => void
  numServers: number
  onChangeNumServers: (num: number) => void
}

export default function TaskCreationForm({ tasks, onAddTask, onRemoveTask, numServers, onChangeNumServers }: TaskCreationFormProps) {
  const [taskName, setTaskName] = useState("")
  const [taskTime, setTaskTime] = useState<number | "">("")
  const [predecessorId, setPredecessorId] = useState<string>("")
  const [taskPriority, setTaskPriority] = useState<number | "">("")

  const handleAddTask = (e: React.FormEvent) => {
    e.preventDefault()

    if (!taskName || typeof taskTime !== "number" || taskTime <= 0) {
      alert("Please provide a valid task name and a time > 0.")
      return
    }

    const newTask: TaskInput = {
      id: crypto.randomUUID(),
      task_name: taskName,
      task_time: taskTime,
      predecessor_id: predecessorId || null,
      task_priority: typeof taskPriority === "number" ? taskPriority : null,
    }

    onAddTask(newTask)

    // Reset form fields
    setTaskName("")
    setTaskTime("")
    setPredecessorId("")
    setTaskPriority("")
  }

  return (
    <section className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 mb-6 shadow-sm">
      <header className="mb-4">
        <h2 className="text-lg font-semibold text-neutral-800 dark:text-neutral-200">
          Task Configuration
        </h2>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          Configure the number of servers and add tasks to your schedule.
        </p>
      </header>

      {/* Global Configuration */}
      <div className="mb-6 pb-6 border-b border-neutral-200 dark:border-neutral-800">
        <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
          Number of Servers
        </label>
        <input
          type="number"
          min="1"
          value={numServers}
          onChange={(e) => onChangeNumServers(Number(e.target.value))}
          className="w-full md:w-1/3 px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-700 rounded-md focus:ring-2 focus:ring-blue-500 outline-none text-neutral-900 dark:text-neutral-100"
        />
      </div>

      {/* Task Form */}
      <form onSubmit={handleAddTask} className="flex flex-col gap-4 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Task Name
            </label>
            <input
              type="text"
              value={taskName}
              onChange={(e) => setTaskName(e.target.value)}
              placeholder="e.g. Setup DB"
              className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-700 rounded-md focus:ring-2 focus:ring-blue-500 outline-none text-neutral-900 dark:text-neutral-100"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Time (must be &gt; 0)
            </label>
            <input
              type="number"
              min="0.1"
              step="0.1"
              value={taskTime}
              onChange={(e) => setTaskTime(e.target.value === "" ? "" : Number(e.target.value))}
              placeholder="e.g. 10"
              className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-700 rounded-md focus:ring-2 focus:ring-blue-500 outline-none text-neutral-900 dark:text-neutral-100"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Predecessor (Optional)
            </label>
            <select
              value={predecessorId}
              onChange={(e) => setPredecessorId(e.target.value)}
              className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-700 rounded-md focus:ring-2 focus:ring-blue-500 outline-none text-neutral-900 dark:text-neutral-100"
            >
              <option value="">None</option>
              {tasks.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.task_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Priority (Optional)
            </label>
            <input
              type="number"
              value={taskPriority}
              onChange={(e) => setTaskPriority(e.target.value === "" ? "" : Number(e.target.value))}
              placeholder="e.g. 1 (Highest)"
              className="w-full px-3 py-2 bg-neutral-50 dark:bg-neutral-950 border border-neutral-200 dark:border-neutral-700 rounded-md focus:ring-2 focus:ring-blue-500 outline-none text-neutral-900 dark:text-neutral-100"
            />
          </div>
        </div>

        <div className="flex justify-end mt-2">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md transition-colors"
          >
            Add Task
          </button>
        </div>
      </form>

      {/* Task List */}
      <div>
        <h3 className="text-sm font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400 mb-3">
          Added Tasks ({tasks.length})
        </h3>
        {tasks.length === 0 ? (
          <p className="text-sm text-neutral-400 dark:text-neutral-500 italic">
            No tasks added yet. Create some above.
          </p>
        ) : (
          <ul className="flex flex-col gap-2">
            {tasks.map((task) => (
              <li
                key={task.id}
                className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-950 border border-neutral-100 dark:border-neutral-800 rounded-lg"
              >
                <div className="flex items-center gap-4 text-sm text-neutral-800 dark:text-neutral-200">
                  <span className="font-medium w-32 truncate">{task.task_name}</span>
                  <span className="text-neutral-500 dark:text-neutral-400 w-16">
                    Time: {task.task_time}
                  </span>
                  {task.predecessor_id && (
                    <span className="text-amber-600 dark:text-amber-400 text-xs px-2 py-1 bg-amber-50 dark:bg-amber-900/30 rounded-md">
                      Requires: {tasks.find((t) => t.id === task.predecessor_id)?.task_name || task.predecessor_id}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => onRemoveTask(task.id)}
                  className="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 text-sm font-medium transition-colors"
                  aria-label="Delete Task"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
