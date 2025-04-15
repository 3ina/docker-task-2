from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List
from .models import TaskModel, TaskUpdateModel, TaskResponse
from .database import get_all_tasks, get_task, create_task, update_task, delete_task

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def read_tasks():
    """Get all tasks"""
    tasks = await get_all_tasks()
    for item in tasks:
        item["_id"] = str(item["_id"])
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: str):
    """Get a specific task by ID"""
    try:
        task_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    task = await get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(task: TaskModel):
    """Create a new task"""
    # Convert the model to a dict and remove the id field (MongoDB will generate it)
    task_dict = task.dict(exclude={"id"})
    
    # Create the task in the database
    created_task = await create_task(task_dict)
    
    return created_task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: str, task_update: TaskUpdateModel):
    """Update an existing task"""
    try:
        task_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    # Check if task exists
    existing_task = await get_task(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update the task
    updated_task = await update_task(task_id, task_update.dict(exclude_unset=True))
    
    updated_task["_id"] = str(updated_task["_id"])


    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(task_id: str):
    """Delete a task"""
    try:
        task_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    # Check if task exists
    existing_task = await get_task(task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete the task
    deleted = await delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete task")
