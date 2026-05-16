import { ScheduleResult } from '@/lib/types_api'
import ServerCard from './ServerCard'

interface ServerGridProps {
    result: ScheduleResult
}

export default function ServerGrid({ result }: ServerGridProps) {
  return (
    <section aria-label="Grid de servidores" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {result.servers.map((server) => (
        <ServerCard
          key={server.server_id}
          server={server}
          maxLoad={result.max_load}
        />
      ))}
    </section>
  )
}