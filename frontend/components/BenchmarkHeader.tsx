import { BENCHMARK_RESULTS, ALGORITHM_META, formatMicros } from "@/lib/benchmarks-data"

export default function BenchmarkHeader() {
  const smallResults = BENCHMARK_RESULTS.filter(r => r.case === "small")

  // Best makespan in small case
  const bestMakespan = Math.min(
    ...smallResults.filter(r => r.makespan !== null).map(r => r.makespan as number)
  )
  const bestMakespanAlgs = smallResults
    .filter(r => r.makespan === bestMakespan)
    .map(r => ALGORITHM_META[r.algorithm].label)
    .join(", ")

  // Fastest algorithm in small case
  const withTime = smallResults.filter(r => r.avg_execution_time !== null)
  const fastest = withTime.reduce((a, b) =>
    (a.avg_execution_time as number) < (b.avg_execution_time as number) ? a : b
  )

  // How many algorithms completed the large case
  const largeCompleted = BENCHMARK_RESULTS.filter(
    r => r.case === "large" && r.makespan !== null
  ).length

  const stats = [
    {
      label: "Best Makespan (Small)",
      value: String(bestMakespan),
      sub: `Achieved by ${bestMakespanAlgs}`,
    },
    {
      label: "Fastest Algorithm (Small)",
      value: formatMicros(fastest.avg_execution_time as number),
      sub: ALGORITHM_META[fastest.algorithm].label,
    },
    {
      label: "Completed Large Case",
      value: `${largeCompleted} / 5`,
      sub: "Algorithms within timeout",
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
      {stats.map(s => (
        <div
          key={s.label}
          className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl px-4 py-3.5 shadow-sm"
        >
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">{s.label}</p>
          <p className="text-2xl font-semibold text-neutral-900 dark:text-neutral-100 leading-none mb-1">
            {s.value}
          </p>
          <p className="text-xs text-neutral-400 dark:text-neutral-500">{s.sub}</p>
        </div>
      ))}
    </div>
  )
}
