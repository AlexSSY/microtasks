from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

from db import Base


class BaseFieldsMixin:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True)
    
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Task(Base, BaseFieldsMixin):
    __tablename__ = "tasks"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
