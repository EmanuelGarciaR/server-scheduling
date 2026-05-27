import { BENCHMARK_RESULTS } from "@/lib/benchmarks-data"
import BenchmarkBarChart from "@/components/BenchmarkBarChart"
import BenchmarkTable from "@/components/BenchmarkTable"
import BenchmarkHeader from "@/components/BenchmarkHeader"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Benchmarks — Server Scheduling",
  description: "Interactive benchmark results comparing scheduling algorithm performance across small, medium and large cases.",
}

export default function BenchmarksPage() {
  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-950 p-6 md:p-10">
      <div className="max-w-6xl mx-auto flex flex-col gap-8">
        <header>
          <h1 className="text-2xl font-semibold text-neutral-900 dark:text-neutral-100">
            Benchmarks
          </h1>
          <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
            Empirical comparison of scheduling algorithms across three problem sizes.
          </p>
        </header>

        <BenchmarkHeader />

        <BenchmarkBarChart
          title="Execution Time by Algorithm"
          description="Average time each algorithm took to compute the schedule. Algorithms that exceeded the timeout are shown as N/A."
          dataKey="avg_execution_time"
          data={BENCHMARK_RESULTS}
        />

        <BenchmarkBarChart
          title="Makespan by Algorithm"
          description="Total completion time (makespan) of the produced schedule. Lower is better. N/A means the algorithm did not finish."
          dataKey="makespan"
          data={BENCHMARK_RESULTS}
        />

        <BenchmarkTable />
      </div>
    </main>
  )
}
