from faker import Faker

from models import Task
from db import SessionLocal


if __name__ == "__main__":
    fake = Faker()

    with SessionLocal() as session:
        for _ in range(10):
            task = Task(name=fake.name(), user_id=5536)
            session.add(task)
        session.commit()
