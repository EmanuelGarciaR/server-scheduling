interface MetricCardProps {
    label: string
    value: string | number
    sub?: string
    }

export default function MetricCard({ label, value, sub }: MetricCardProps) {
    return (
        <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg px-4 py-3">
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">{label}</p>
            <p className="text-2xl font-medium text-neutral-900 dark:text-neutral-100">{value}</p>
            {sub && <p className="text-xs text-neutral-400 dark:text-neutral-500 mt-1">{sub}</p>}
        </div>
    )
    }