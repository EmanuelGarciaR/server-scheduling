import { ServerResult } from '@/lib/types_api'

interface GanttChartProps {
    servers: ServerResult[]
    maxLoad: number
}

const TASK_COLORS = [
  'bg-blue-400 text-blue-900',
  'bg-emerald-400 text-emerald-900',
  'bg-violet-400 text-violet-900',
  'bg-amber-400 text-amber-900',
  'bg-rose-400 text-rose-900',
  'bg-cyan-400 text-cyan-900',
]

export default function GanttChart({ servers, maxLoad }: GanttChartProps) {
  const ticks = [0, 0.25, 0.5, 0.75, 1].map((t) => Math.round(t * maxLoad))

  let colorIndex = 0
  const taskColorMap: Record<string, string> = {}

  servers.forEach((server) => {
    server.tasks.forEach((task) => {
      if (!taskColorMap[task.task_name]) {
        taskColorMap[task.task_name] = TASK_COLORS[colorIndex % TASK_COLORS.length]
        colorIndex++
      }
    })
  })

  return (
    <article className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-xl p-5">
      <header className="mb-5">
        <h2 className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
          Diagrama de Gantt
        </h2>
      </header>

      <ol className="flex flex-col gap-3" aria-label="Líneas de tiempo por servidor">
        {servers.map((server) => (
          <li key={server.server_id} className="flex items-center gap-3">
            <p className="text-xs text-neutral-500 w-20 shrink-0 text-right truncate">
              {server.server_name}
            </p>

            <div
              role="img"
              aria-label={`Línea de tiempo de ${server.server_name}`}
              className="relative flex-1 h-8 bg-neutral-100 dark:bg-neutral-800 rounded-lg overflow-hidden"
            >
              {server.tasks.length === 0 ? (
                <span className="absolute inset-0 flex items-center justify-center text-xs text-neutral-300 dark:text-neutral-600">
                  idle
                </span>
              ) : (
                (() => {
                  return server.tasks.map((task) => {
                    // Use start_time for the horizontal position (left)
                    const left = (task.start_time / maxLoad) * 100
                    const width = (task.task_time / maxLoad) * 100
                    return (
                      <span
                        key={task.id}
                        title={`${task.task_name} — ${task.task_time}u`}
                        className={`absolute top-0 h-full flex items-center justify-center text-xs font-medium rounded-md ${taskColorMap[task.task_name]}`}
                        style={{ left: `${left}%`, width: `${width}%` }}
                      >
                        {width > 8 ? task.task_name : ''}
                      </span>
                    )
                  })
                })()
              )}
            </div>
          </li>
        ))}
      </ol>

      <footer className="flex justify-between mt-2 pl-24 text-xs text-neutral-400">
        {ticks.map((t) => (
          <span key={t}>{t}</span>
        ))}
      </footer>
    </article>
  )
}