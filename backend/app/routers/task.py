from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create Task
@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get All Tasks
@router.get("/", response_model=list[schemas.TaskOut])
def get_all_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

# Get Tasks by Project
@router.get("/project/{project_id}", response_model=list[schemas.TaskOut])
def get_tasks_by_project(project_id: int, db: Session = Depends(database.get_db)):
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    return tasks

# Update Task
@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_data: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

# Delete Task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
