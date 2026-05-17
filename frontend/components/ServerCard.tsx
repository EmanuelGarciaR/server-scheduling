import { ServerResult } from '@/lib/types_api'
import { SimulationState } from '../hooks/useSimulation'

interface ServerCardProps {
    server: ServerResult
    maxLoad: number
}

interface SimulationProps {
    simulationState?: SimulationState
}

function getBarColor(percentage: number) {
    if (percentage === 0) return 'bg-neutral-200 dark:bg-neutral-700'
    if (percentage < 50) return 'bg-emerald-400'
    if (percentage < 80) return 'bg-amber-400'
    return 'bg-rose-500'
}

export default function ServerCard({ server, maxLoad, simulationState }: ServerCardProps & SimulationProps) {
  const isSimulating = simulationState !== undefined;
  const simTime = simulationState?.simulationTime ?? maxLoad;

  const taskTimelines = server.tasks.map(task => {
    const start = task.start_time;
    const end = task.finish_time;
    
    let state: 'waiting' | 'running' | 'completed' = 'waiting';
    if (!isSimulating || simTime >= end) {
      state = 'completed';
    } else if (simTime >= start && simTime < end) {
      state = 'running';
    }

    return { ...task, start, end, state };
  });

  const runningTask = taskTimelines.find(t => t.state === 'running');
  const runningLoad = runningTask ? (simTime - runningTask.start) : 0;
  
  const remainingLoad = isSimulating 
    ? Math.max(0, server.total_load - simTime) 
    : server.total_load;
  
  const percentage = maxLoad > 0 ? Math.round((remainingLoad / maxLoad) * 100) : 0;

  return (
    <article className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-xl p-4 transition-colors">
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
        <span>Carga: {isSimulating ? Math.ceil(remainingLoad) : server.total_load}</span>
        <span>Máx: {maxLoad}</span>
      </div>

      {runningTask && isSimulating && (
        <div className="mb-4">
           <div className="flex justify-between text-xs mb-1">
             <span className="text-blue-600 dark:text-blue-400 font-medium truncate pr-2">Running: {runningTask.task_name}</span>
             <span className="text-neutral-500 whitespace-nowrap">{runningLoad.toFixed(0)} / {runningTask.task_time}u</span>
           </div>
           <div className="h-1.5 bg-blue-100 dark:bg-blue-900/30 rounded-full overflow-hidden">
             <div 
               className="h-full bg-blue-500 rounded-full transition-all duration-300 ease-linear"
               style={{ width: `${(runningLoad / runningTask.task_time) * 100}%` }}
             />
           </div>
        </div>
      )}

      {server.tasks.length === 0 ? (
        <p className="border border-dashed border-neutral-200 dark:border-neutral-700 rounded-lg py-4 text-center text-xs text-neutral-400">
          Sin tareas asignadas
        </p>
      ) : (
        <ul className="flex flex-col gap-2">
          {taskTimelines.map((task) => {
            let itemClass = "flex items-center justify-between rounded-lg px-3 py-2 transition-all duration-300";
            let nameClass = "text-sm font-medium";
            let timeClass = "text-xs font-mono";
            let icon = null;

            if (task.state === 'completed') {
              itemClass += " bg-emerald-50 dark:bg-emerald-900/10 opacity-60";
              nameClass += " text-emerald-700 dark:text-emerald-500";
              timeClass += " text-emerald-600 dark:text-emerald-500";
              icon = <span className="mr-2 text-emerald-500 dark:text-emerald-400 text-sm">✓</span>;
            } else if (task.state === 'running') {
              itemClass += " bg-blue-50 dark:bg-blue-900/20 ring-1 ring-blue-400 dark:ring-blue-500 animate-pulse";
              nameClass += " text-blue-800 dark:text-blue-300";
              timeClass += " text-blue-600 dark:text-blue-400";
              icon = <span className="mr-2 text-blue-500 dark:text-blue-400 text-xs">▶</span>;
            } else {
              itemClass += " bg-neutral-50 dark:bg-neutral-800/50";
              nameClass += " text-neutral-500 dark:text-neutral-400";
              timeClass += " text-neutral-400 dark:text-neutral-500";
            }

            return (
              <li key={task.id} className={itemClass}>
                <div className="flex items-center overflow-hidden">
                  {icon}
                  <span className={`${nameClass} truncate`}>{task.task_name}</span>
                </div>
                <span className={`${timeClass} ml-2 shrink-0`}>{task.task_time}u</span>
              </li>
            )
          })}
        </ul>
      )}
    </article>
  )
}