from typing import List

from pydantic import BaseModel


class Subtask(BaseModel):
    description: str


class Task(BaseModel):
    task_id: str
    task: str
    subtasks: List[Subtask]


class Step(BaseModel):
    step: int
    title: str
    description: str
    tasks: List[Task]


class Process(BaseModel):
    steps: List[Step]
