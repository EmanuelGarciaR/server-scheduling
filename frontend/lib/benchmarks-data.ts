export type AlgorithmId = 'greedy' | 'backtracking' | 'brute_force' | 'divide_conquer' | 'recursive'
export type CaseId = 'small' | 'medium' | 'large'

export interface BenchmarkEntry {
  algorithm: AlgorithmId
  case: CaseId
  n_tasks: number
  num_servers: number
  makespan: number | null
  avg_execution_time: number | null
  is_optimal: boolean
}

export const BENCHMARK_RESULTS: BenchmarkEntry[] = [
  { algorithm: 'greedy',         case: 'small',  n_tasks: 5,   num_servers: 3,  makespan: 25,  avg_execution_time: 2.0780041813850404e-05, is_optimal: false },
  { algorithm: 'backtracking',   case: 'small',  n_tasks: 5,   num_servers: 3,  makespan: 24,  avg_execution_time: 0.00012217992916703225,  is_optimal: true  },
  { algorithm: 'brute_force',    case: 'small',  n_tasks: 5,   num_servers: 3,  makespan: 24,  avg_execution_time: 0.001931580062955618,    is_optimal: true  },
  { algorithm: 'divide_conquer', case: 'small',  n_tasks: 5,   num_servers: 3,  makespan: 25,  avg_execution_time: 5.345996469259262e-05,  is_optimal: false },
  { algorithm: 'recursive',      case: 'small',  n_tasks: 5,   num_servers: 3,  makespan: 24,  avg_execution_time: 0.0016080200672149657,   is_optimal: true  },
  { algorithm: 'greedy',         case: 'medium', n_tasks: 20,  num_servers: 5,  makespan: 209, avg_execution_time: 8.194008842110634e-05,  is_optimal: false },
  { algorithm: 'backtracking',   case: 'medium', n_tasks: 20,  num_servers: 5,  makespan: null, avg_execution_time: null,                   is_optimal: false },
  { algorithm: 'brute_force',    case: 'medium', n_tasks: 20,  num_servers: 5,  makespan: null, avg_execution_time: null,                   is_optimal: false },
  { algorithm: 'divide_conquer', case: 'medium', n_tasks: 20,  num_servers: 5,  makespan: 209, avg_execution_time: 0.00010810000821948051,  is_optimal: false },
  { algorithm: 'recursive',      case: 'medium', n_tasks: 20,  num_servers: 5,  makespan: null, avg_execution_time: null,                   is_optimal: false },
  { algorithm: 'greedy',         case: 'large',  n_tasks: 100, num_servers: 10, makespan: 552, avg_execution_time: 0.0005369400605559349,  is_optimal: false },
  { algorithm: 'backtracking',   case: 'large',  n_tasks: 100, num_servers: 10, makespan: null, avg_execution_time: null,                   is_optimal: false },
  { algorithm: 'brute_force',    case: 'large',  n_tasks: 100, num_servers: 10, makespan: null, avg_execution_time: null,                   is_optimal: false },
  { algorithm: 'divide_conquer', case: 'large',  n_tasks: 100, num_servers: 10, makespan: 552, avg_execution_time: 0.0008845599368214607,  is_optimal: false },
  { algorithm: 'recursive',      case: 'large',  n_tasks: 100, num_servers: 10, makespan: null, avg_execution_time: null,                   is_optimal: false },
]

export const ALGORITHM_META: Record<AlgorithmId, { label: string; color: string }> = {
  greedy:         { label: 'Greedy',           color: '#10b981' },
  backtracking:   { label: 'Backtracking',     color: '#f59e0b' },
  brute_force:    { label: 'Brute Force',      color: '#f43f5e' },
  divide_conquer: { label: 'Divide & Conquer', color: '#0ea5e9' },
  recursive:      { label: 'Recursive',        color: '#a855f7' },
}

export const CASE_META: Record<CaseId, { label: string; n_tasks: number; num_servers: number }> = {
  small:  { label: 'Small',  n_tasks: 5,   num_servers: 3  },
  medium: { label: 'Medium', n_tasks: 20,  num_servers: 5  },
  large:  { label: 'Large',  n_tasks: 100, num_servers: 10 },
}

export const ALGORITHMS: AlgorithmId[] = ['greedy', 'backtracking', 'brute_force', 'divide_conquer', 'recursive']
export const CASES: CaseId[]           = ['small', 'medium', 'large']

export function formatMicros(seconds: number): string {
  const us = seconds * 1_000_000
  if (us >= 1000) return `${(us / 1000).toFixed(2)} ms`
  return `${us.toFixed(2)} µs`
}
