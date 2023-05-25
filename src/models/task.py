from init_app import db
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class TaskType(db.Model):
    id = Column(Integer, primary_key=True)
    opaque_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
    name = Column(db.String(100), index=True, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(db.String(50), index=True, nullable=False)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

class Task(db.Model):
    id = Column(Integer, primary_key=True)
    opaque_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    type = Column(String(100), default=uuid.uuid4, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(String(50), index=True, nullable=False)
    status = Column(String(20), default='scheduled', index=True, nullable=False)

    def __init__(self, name, task_type, created_at, created_by, status='scheduled'):
        self.name = name
        self.type = task_type
        self.created_at = created_at
        self.created_by = created_by
        self.status = status
