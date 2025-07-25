from db import SessionLocal
from models import Task


async def add_task(user_id, name, description):
    with SessionLocal() as session:
        task = Task(name=name, user_id=user_id, description=description)
        session.add(task)
        session.commit()


async def user_task_list(user_id):
    with SessionLocal() as session:
        return session.query(Task).where(Task.user_id==user_id).all()
