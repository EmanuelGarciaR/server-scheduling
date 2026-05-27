"use client"

import { useState } from "react"
import {
  BENCHMARK_RESULTS, ALGORITHM_META, CASE_META,
  type CaseId, formatMicros,
} from "@/lib/benchmarks-data"

const CASES: CaseId[] = ["small", "medium", "large"]

export default function BenchmarkTable() {
  const [activeCase, setActiveCase] = useState<CaseId>("small")

  const rows = BENCHMARK_RESULTS.filter(r => r.case === activeCase)

  return (
    <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
        <div>
          <h3 className="text-base font-semibold text-neutral-800 dark:text-neutral-200">Detailed Results</h3>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">All benchmark entries per case size</p>
        </div>

        {/* Tab filter */}
        <div className="flex items-center bg-neutral-100 dark:bg-neutral-800 rounded-lg p-1 gap-1">
          {CASES.map(c => (
            <button
              key={c}
              onClick={() => setActiveCase(c)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                activeCase === c
                  ? "bg-white dark:bg-neutral-700 text-neutral-900 dark:text-white shadow-sm"
                  : "text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300"
              }`}
            >
              {CASE_META[c].label}
              <span className="ml-1.5 text-neutral-400 dark:text-neutral-500 font-normal">
                ({CASE_META[c].n_tasks}t / {CASE_META[c].num_servers}s)
              </span>
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-neutral-100 dark:border-neutral-800">
              <th className="pb-2 text-left font-medium text-neutral-500 dark:text-neutral-400 text-xs">Algorithm</th>
              <th className="pb-2 text-right font-medium text-neutral-500 dark:text-neutral-400 text-xs">Makespan</th>
              <th className="pb-2 text-right font-medium text-neutral-500 dark:text-neutral-400 text-xs">Avg. Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-neutral-50 dark:divide-neutral-800/60">
            {rows.map(r => {
              const meta = ALGORITHM_META[r.algorithm]
              return (
                <tr key={r.algorithm} className="hover:bg-neutral-50 dark:hover:bg-neutral-800/40 transition-colors">
                  <td className="py-3">
                    <div className="flex items-center gap-2">
                      <span
                        className="inline-block w-2 h-2 rounded-full flex-shrink-0"
                        style={{ backgroundColor: meta.color }}
                      />
                      <span className="font-medium text-neutral-800 dark:text-neutral-200">
                        {meta.label}
                      </span>
                    </div>
                  </td>
                  <td className="py-3 text-right">
                    {r.makespan !== null ? (
                      <span className="text-neutral-800 dark:text-neutral-200 font-mono">
                        {r.makespan}
                      </span>
                    ) : (
                      <span className="text-neutral-400 dark:text-neutral-600 text-xs italic">N/A</span>
                    )}
                  </td>
                  <td className="py-3 text-right">
                    {r.avg_execution_time !== null ? (
                      <span className="text-neutral-800 dark:text-neutral-200 font-mono">
                        {formatMicros(r.avg_execution_time)}
                      </span>
                    ) : (
                      <span className="text-neutral-400 dark:text-neutral-600 text-xs italic">N/A</span>
                    )}
                  </td>

                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
