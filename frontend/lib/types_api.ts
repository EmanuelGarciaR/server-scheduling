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
    id: string
    task_name: string
    task_time: number
    predecessor_id: string | null
    task_priority: number | null
}

// Respuesta completa de la API
export interface ScheduleResponse {
    algorithm: Algorithm
    input: ScheduleRequest
    result: ScheduleResult
}

export async function fetchSchedule(request: ScheduleRequest): Promise<ScheduleResult> {
    const res = await fetch('http://localhost:8000/schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    })

    if (!res.ok) {
        const errorData = await res.json().catch(() => null)
        const errorMessage = errorData?.detail || `Error: ${res.status} ${res.statusText}`
        throw new Error(errorMessage)
    }
    
    const data: ScheduleResult = await res.json()
    return data
}