export type Algorithm = 'brute_force' | 'recursive' | 'greedy' | 'backtracking' | 'divide_conquer'

// Corresponde a Task.to_json_task()
export interface Task {
    id: string
    task_name: string
    task_time: number
    }

// Corresponde a Server.to_json_server()
export interface ServerResult {
    server_id: string
    server_name: string
    tasks: Task[]
    total_load: number
    }

// Corresponde a ScheduleResult.to_json_schedule_result()
export interface ScheduleResult {
    servers: ServerResult[]
    max_load: number
    execution_time: number
    total_tasks: number
    }

// Lo que envías al backend
export interface ScheduleRequest {
    algorithm: Algorithm
    num_servers: number
    tasks: TaskInput[]
    }

// Tarea como entrada del usuario (antes de ser procesada por el backend)
export interface TaskInput {
    name: string
    time: number
    priority?: number
    deps?: string[]   // dependencias por nombre de tarea
    }

// Respuesta completa de la API
export interface ScheduleResponse {
    algorithm: Algorithm
    input: ScheduleRequest
    result: ScheduleResult
    }

export async function fetchSchedule(request: ScheduleRequest): Promise<ScheduleResponse> {
    const res = await fetch('/mock/schedule.json') 

    if (!res.ok) {
        throw new Error(`Failed to fetch schedule: ${res.status} ${res.statusText}`)
    }
    
    const data: ScheduleResponse = await res.json()
    return data
    }