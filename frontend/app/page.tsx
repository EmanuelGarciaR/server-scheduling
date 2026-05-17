import SchedulingDashboard from '@/components/SchedulingDashboard'

export default function Home() {
  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-950 p-6 md:p-10">
      <div className="max-w-6xl mx-auto flex flex-col gap-8">
        <header className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold text-neutral-900 dark:text-neutral-100">
            Server Scheduling
          </h1>
        </header>

        {/* Dashboard handles state and UI for tasks, algorithms, and results */}
        <SchedulingDashboard />
      </div>
    </main>
  )
}