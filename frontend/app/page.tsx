import { fetchSchedule } from '@/lib/types_api'
import MetricCard from '@/components/MetricCard'
import ServerGrid from '@/components/ServerGrid'
import GanttChart from '@/components/GanntChart'

export default async function Home() {
  const data = await fetchSchedule({
    algorithm: 'greedy',
    num_servers: 10,
    tasks: [],
  })

  const { result, algorithm } = data

  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-950 p-6 md:p-10">
      <div className="max-w-6xl mx-auto flex flex-col gap-8">

        <header className="flex items-center gap-3">
          <h1 className="text-xl font-medium text-neutral-900 dark:text-neutral-100">
            Server Scheduling
          </h1>
          <span className="text-xs px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-900 text-emerald-700 dark:text-emerald-300 font-medium">
            {algorithm}
          </span>
        </header>

        <section aria-label="Métricas generales">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <MetricCard label="Makespan" value={result.max_load} sub="unidades de tiempo" />
            <MetricCard label="Tareas" value={result.total_tasks} />
            <MetricCard label="Servidores" value={result.servers.length} />
            <MetricCard
              label="Tiempo algoritmo"
              value={`${(result.execution_time * 1000).toFixed(2)}ms`}
            />
          </div>
        </section>

        <section aria-label="Servidores">
          <p className="text-xs font-medium uppercase tracking-widest text-neutral-400 mb-3">
            Servidores
          </p>
          <ServerGrid result={result} />
        </section>

        <section aria-label="Diagrama de Gantt">
          <GanttChart servers={result.servers} maxLoad={result.max_load} />
        </section>

      </div>
    </main>
  )
}