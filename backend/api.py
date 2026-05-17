from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.core.sheduler import run_scheduler, CircularDependencyError, ValidationError

app = FastAPI(
    title="Server Scheduling API",
    description="API for scheduling tasks across multiple servers using various algorithms.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development, you can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskInput(BaseModel):
    id: str = Field(..., description="Unique identifier for the task")
    task_name: str = Field(..., description="Name of the task")
    task_time: float = Field(..., description="Time required to complete the task")
    predecessor_id: Optional[str] = Field(None, description="ID of the predecessor task, if any")
    task_priority: Optional[int] = Field(None, description="Priority of the task (optional)")

class ScheduleRequest(BaseModel):
    tasks: List[TaskInput] = Field(..., description="List of tasks to schedule")
    algorithm: str = Field("greedy", description="Algorithm to use for scheduling (e.g., greedy, backtracking, brute_force)")
    num_servers: Optional[int] = Field(None, description="Number of servers available. If not provided, defaults to CPU count.")

@app.post("/schedule", summary="Schedule Tasks")
def schedule_tasks(request: ScheduleRequest):
    """
    Schedules a list of tasks using the specified algorithm.
    """
    # Convert Pydantic models to dicts as expected by run_scheduler
    raw_data = {
        "tasks": [task.model_dump() for task in request.tasks],
        "num_servers": request.num_servers
    }
    
    try:
        result = run_scheduler(raw_data, request.algorithm, request.num_servers)
        return result.to_json_schedule_result()
    except CircularDependencyError as e:
        raise HTTPException(status_code=400, detail=f"Circular Dependency Error: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value Error: {str(e)}")
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Type Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
