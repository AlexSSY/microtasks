from db import SessionLocal
from models import Task


async def add_task(user_id, name):
    with SessionLocal() as session:
        task = Task(name=name, user_id=user_id)
        session.add(task)
        session.commit()


async def user_task_list(user_id):
    ...
