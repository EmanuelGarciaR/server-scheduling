"use client"

import { Algorithm } from "@/lib/types_api"

interface AlgorithmSelectorProps {
  selected: Algorithm
  onSelect: (alg: Algorithm) => void
}

type ColorTheme = {
  bg: string
  border: string
  textTitle: string
  textDesc: string
}

const ALGORITHMS: { id: Algorithm; label: string; description: string; theme: ColorTheme }[] = [
  {
    id: "greedy",
    label: "Greedy",
    description: "Fast, heuristic-based assignment",
    theme: {
      bg: "bg-emerald-50 dark:bg-emerald-900/20",
      border: "border-emerald-500 ring-1 ring-emerald-500",
      textTitle: "text-emerald-700 dark:text-emerald-300",
      textDesc: "text-emerald-600 dark:text-emerald-400",
    },
  },
  {
    id: "backtracking",
    label: "Backtracking",
    description: "Exhaustive search with pruning",
    theme: {
      bg: "bg-amber-50 dark:bg-amber-900/20",
      border: "border-amber-500 ring-1 ring-amber-500",
      textTitle: "text-amber-700 dark:text-amber-300",
      textDesc: "text-amber-600 dark:text-amber-400",
    },
  },
  {
    id: "brute_force",
    label: "Brute Force",
    description: "Evaluates all combinations",
    theme: {
      bg: "bg-rose-50 dark:bg-rose-900/20",
      border: "border-rose-500 ring-1 ring-rose-500",
      textTitle: "text-rose-700 dark:text-rose-300",
      textDesc: "text-rose-600 dark:text-rose-400",
    },
  },
  {
    id: "recursive",
    label: "Recursive",
    description: "Simple recursive assignment",
    theme: {
      bg: "bg-purple-50 dark:bg-purple-900/20",
      border: "border-purple-500 ring-1 ring-purple-500",
      textTitle: "text-purple-700 dark:text-purple-300",
      textDesc: "text-purple-600 dark:text-purple-400",
    },
  },
  {
    id: "divide_conquer",
    label: "Divide & Conquer",
    description: "Splits task list",
    theme: {
      bg: "bg-sky-50 dark:bg-sky-900/20",
      border: "border-sky-500 ring-1 ring-sky-500",
      textTitle: "text-sky-700 dark:text-sky-300",
      textDesc: "text-sky-600 dark:text-sky-400",
    },
  },
]

export default function AlgorithmSelector({ selected, onSelect }: AlgorithmSelectorProps) {
  return (
    <section className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 mb-6 shadow-sm">
      <header className="mb-4">
        <h2 className="text-lg font-semibold text-neutral-800 dark:text-neutral-200">
          Scheduling Algorithm
        </h2>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          Choose the strategy for assigning tasks to servers.
        </p>
      </header>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {ALGORITHMS.map((algo) => {
          const isSelected = selected === algo.id;
          return (
            <button
              key={algo.id}
              onClick={() => onSelect(algo.id)}
              className={`flex flex-col text-left p-3 rounded-lg border transition-all ${
                isSelected
                  ? `${algo.theme.bg} ${algo.theme.border} shadow-sm`
                  : "bg-neutral-50 dark:bg-neutral-950 border-neutral-200 dark:border-neutral-800 hover:border-neutral-300 dark:hover:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-900"
              }`}
            >
              <span className={`text-sm font-semibold mb-1 ${
                isSelected ? algo.theme.textTitle : "text-neutral-700 dark:text-neutral-300"
              }`}>
                {algo.label}
              </span>
              <span className={`text-xs leading-tight ${
                isSelected ? algo.theme.textDesc : "text-neutral-500 dark:text-neutral-500"
              }`}>
                {algo.description}
              </span>
            </button>
          )
        })}
      </div>
    </section>
  )
}
