from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import models
import schemas 
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = updated_task.title
    db_task.completed = updated_task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task created", "task": task}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks[index] = updated_task
            return {"message": "Task updated", "task": updated_task}
    return {"message": "Task not found"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully!"}