"use client"

import { useState } from "react"
import {
  ALGORITHMS, CASES, ALGORITHM_META, CASE_META,
  formatMicros,
  type BenchmarkEntry, type AlgorithmId, type CaseId,
} from "@/lib/benchmarks-data"

interface Props {
  title: string
  description: string
  dataKey: "makespan" | "avg_execution_time"
  data: BenchmarkEntry[]
}

interface TooltipState {
  algorithm: AlgorithmId
  caseId: CaseId
  value: number | null
  px: number
  py: number
}

const ML = 70, MR = 20, MT = 20, MB = 68
const W = 640, H = 300
const CW = W - ML - MR
const CH = H - MT - MB
const NA_H = 10

function formatTick(v: number, dataKey: "makespan" | "avg_execution_time"): string {
  if (v === 0) return "0"
  if (dataKey === "avg_execution_time") {
    const us = v * 1_000_000
    return us >= 1000 ? `${(us / 1000).toFixed(1)}ms` : `${us.toFixed(0)}µs`
  }
  return String(Math.round(v))
}

function formatTooltip(v: number, dataKey: "makespan" | "avg_execution_time"): string {
  if (dataKey === "avg_execution_time") return formatMicros(v)
  return `${Math.round(v)} units`
}

export default function BenchmarkBarChart({ title, description, dataKey, data }: Props) {
  const [tip, setTip] = useState<TooltipState | null>(null)

  const getValue = (c: CaseId, alg: AlgorithmId): number | null => {
    const e = data.find(d => d.case === c && d.algorithm === alg)
    return e ? e[dataKey] : null
  }

  const allVals = data.map(d => d[dataKey]).filter((v): v is number => v !== null)
  const maxVal = allVals.length ? Math.max(...allVals) : 1

  const niceMax = (() => {
    const mag = Math.pow(10, Math.floor(Math.log10(maxVal)))
    return Math.ceil(maxVal / mag) * mag
  })()

  const yTicks = Array.from({ length: 6 }, (_, i) => (niceMax * i) / 5)

  const groupW = CW / CASES.length
  const barSlot = (groupW * 0.82) / ALGORITHMS.length
  const barW = Math.max(barSlot - 3, 6)
  const groupPad = (groupW - ALGORITHMS.length * barSlot) / 2

  const barX = (gi: number, ai: number) =>
    gi * groupW + groupPad + ai * barSlot + (barSlot - barW) / 2

  const barY = (v: number) => CH * (1 - v / niceMax)
  const barH = (v: number) => CH * (v / niceMax)

  const trackMouse = (e: React.MouseEvent<SVGGElement>, algorithm: AlgorithmId, caseId: CaseId, value: number | null) => {
    const svg = e.currentTarget.ownerSVGElement as SVGSVGElement
    const rect = svg.getBoundingClientRect()
    setTip({
      algorithm, caseId, value,
      px: (e.clientX - rect.left) * (W / rect.width) - ML,
      py: (e.clientY - rect.top) * (H / rect.height) - MT,
    })
  }

  return (
    <div className="bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-xl p-5 shadow-sm">
      <div className="mb-3">
        <h3 className="text-base font-semibold text-neutral-800 dark:text-neutral-200">{title}</h3>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">{description}</p>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-x-4 gap-y-1.5 mb-4">
        {ALGORITHMS.map(alg => (
          <div key={alg} className="flex items-center gap-1.5">
            <span className="inline-block w-2.5 h-2.5 rounded-sm" style={{ backgroundColor: ALGORITHM_META[alg].color }} />
            <span className="text-xs text-neutral-600 dark:text-neutral-400">{ALGORITHM_META[alg].label}</span>
          </div>
        ))}
        <div className="flex items-center gap-1.5">
          <span className="inline-block w-2.5 h-2.5 rounded-sm bg-neutral-300 dark:bg-neutral-600" />
          <span className="text-xs text-neutral-400 dark:text-neutral-500">N/A (timeout)</span>
        </div>
      </div>

      {/* SVG Chart */}
      <div className="relative w-full overflow-hidden">
        <svg
          viewBox={`0 0 ${W} ${H}`}
          className="w-full"
          style={{ height: "auto", display: "block" }}
          onMouseLeave={() => setTip(null)}
        >
          <g transform={`translate(${ML},${MT})`}>

            {/* Grid + Y-axis labels */}
            {yTicks.map((tick, i) => {
              const y = CH * (1 - tick / niceMax)
              return (
                <g key={i}>
                  <line x1={0} y1={y} x2={CW} y2={y} stroke="currentColor" strokeOpacity={0.07} strokeWidth={1} />
                  <text x={-8} y={y} textAnchor="end" dominantBaseline="middle" fontSize={9} fill="currentColor" fillOpacity={0.45}>
                    {formatTick(tick, dataKey)}
                  </text>
                </g>
              )
            })}

            {/* Axes */}
            <line x1={0} y1={0} x2={0} y2={CH} stroke="currentColor" strokeOpacity={0.12} strokeWidth={1} />
            <line x1={0} y1={CH} x2={CW} y2={CH} stroke="currentColor" strokeOpacity={0.12} strokeWidth={1} />

            {/* Bars */}
            {CASES.map((c, gi) => (
              <g key={c}>
                {ALGORITHMS.map((alg, ai) => {
                  const val = getValue(c, alg)
                  const x = barX(gi, ai)
                  const isHov = tip?.algorithm === alg && tip?.caseId === c

                  if (val === null) {
                    return (
                      <g key={alg}
                        onMouseEnter={e => trackMouse(e, alg, c, null)}
                        onMouseMove={e => trackMouse(e, alg, c, null)}
                      >
                        <rect x={x} y={CH - NA_H} width={barW} height={NA_H} rx={1.5}
                          fill="currentColor" fillOpacity={isHov ? 0.22 : 0.13} />
                        <text x={x + barW / 2} y={CH - NA_H - 3} textAnchor="middle"
                          fontSize={7} fill="currentColor" fillOpacity={0.35}>N/A</text>
                      </g>
                    )
                  }

                  const by = barY(val)
                  const bh = barH(val)
                  return (
                    <g key={alg}
                      onMouseEnter={e => trackMouse(e, alg, c, val)}
                      onMouseMove={e => trackMouse(e, alg, c, val)}
                    >
                      <rect x={x} y={by} width={barW} height={bh} rx={2}
                        fill={ALGORITHM_META[alg].color}
                        fillOpacity={isHov ? 1 : 0.82}
                      />
                    </g>
                  )
                })}

                {/* Group X labels */}
                <text x={gi * groupW + groupW / 2} y={CH + 16}
                  textAnchor="middle" fontSize={11} fill="currentColor" fillOpacity={0.65} fontWeight={500}>
                  {CASE_META[c].label}
                </text>
                <text x={gi * groupW + groupW / 2} y={CH + 30}
                  textAnchor="middle" fontSize={9} fill="currentColor" fillOpacity={0.35}>
                  {CASE_META[c].n_tasks} tasks · {CASE_META[c].num_servers} servers
                </text>
              </g>
            ))}

            {/* Tooltip */}
            {tip && (() => {
              const tw = 148, th = 46
              const tx = Math.min(Math.max(tip.px - tw / 2, 0), CW - tw)
              const ty = tip.py - th - 10 < 0 ? tip.py + 14 : tip.py - th - 10
              return (
                <g style={{ pointerEvents: "none" }}>
                  <rect x={tx} y={ty} width={tw} height={th} rx={5}
                    fill="#111827" fillOpacity={0.93} />
                  <text x={tx + 10} y={ty + 14} fontSize={9.5} fill="white" fillOpacity={0.6}>
                    {ALGORITHM_META[tip.algorithm].label} · {CASE_META[tip.caseId].label}
                  </text>
                  <text x={tx + 10} y={ty + 32} fontSize={13} fontWeight={700} fill="white">
                    {tip.value !== null ? formatTooltip(tip.value, dataKey) : "N/A — timeout"}
                  </text>
                </g>
              )
            })()}

          </g>
        </svg>
      </div>
    </div>
  )
}
