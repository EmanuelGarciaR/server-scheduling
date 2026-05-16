import { ServerResult } from '@/lib/types_api'

interface ServerCardProps {
    server: ServerResult
    maxLoad: number
}

function getBarColor(percentage: number) {
    if (percentage === 0) return 'bg-neutral-200 dark:bg-neutral-700'
    if (percentage < 50) return 'bg-emerald-400'
    if (percentage < 80) return 'bg-amber-400'
    return 'bg-rose-500'
}

export default function ServerCard({ server, maxLoad }: ServerCardProps) {
  const percentage = maxLoad > 0 ? Math.round((server.total_load / maxLoad) * 100) : 0

  return (
    <article className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-xl p-4">
      <header className="flex items-center gap-3 mb-4">
        <div className="w-9 h-9 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-300 text-lg">
          ▪
        </div>
        <div>
          <p className="text-sm font-medium text-neutral-900 dark:text-neutral-100">
            {server.server_name}
          </p>
          <p className="text-xs text-neutral-400 font-mono">{server.server_id.slice(0, 8)}...</p>
        </div>
        <span className="ml-auto text-xs font-medium px-2 py-1 rounded-full bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-300">
          {percentage}%
        </span>
      </header>

      <div className="h-2 bg-neutral-100 dark:bg-neutral-800 rounded-full overflow-hidden mb-1">
        <div
          className={`h-full rounded-full transition-all duration-500 ${getBarColor(percentage)}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="flex justify-between text-xs text-neutral-400 mb-4">
        <span>Carga: {server.total_load}</span>
        <span>Máx: {maxLoad}</span>
      </div>

      {server.tasks.length === 0 ? (
        <p className="border border-dashed border-neutral-200 dark:border-neutral-700 rounded-lg py-4 text-center text-xs text-neutral-400">
          Sin tareas asignadas
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {server.tasks.map((task) => (
            <li
              key={task.id}
              className="flex items-center justify-between bg-neutral-50 dark:bg-neutral-800 rounded-lg px-3 py-2"
            >
              <span className="text-sm font-medium text-neutral-800 dark:text-neutral-200">
                {task.task_name}
              </span>
              <span className="text-xs font-mono text-neutral-400">{task.task_time}u</span>
            </li>
          ))}
        </ul>
      )}
    </article>
  )
}