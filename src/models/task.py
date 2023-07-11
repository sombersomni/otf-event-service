from init_app import db
from sqlalchemy import Column, Index, Integer, ForeignKey, Text, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

class TaskType(db.Model):
    id = Column(Integer, primary_key=True)
    opaque_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
    name = Column(Text, index=True, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    retired_at = Column(TIMESTAMP(timezone=True), index=True, nullable=True)
    created_by = Column(Text, index=True, nullable=False)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

class OwnerTaskAssociation(db.Model):
    id = Column(Integer, primary_key=True)
    opaque_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    task_type_id = Column(Integer, ForeignKey('task_type.id'))
    task_type = relationship(TaskType)
    retired_at = Column(TIMESTAMP(timezone=True), index=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), index=True, server_default=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Define the composite unique index
    __table_args__ = (
        UniqueConstraint('owner_id', 'task_type_id', name='_owner_task_uc'),
    )

    def __init__(self, task_type_id, owner_id, created_by):
        self.task_type_id = task_type_id
        self.created_by = created_by
        self.owner_id = owner_id

class Task(db.Model):
    id = Column(Integer, autoincrement=True)
    opaque_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
    type = Column(Text, index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column(Text, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    status = Column(Text, default='scheduled', index=True, nullable=False)

    # Define the composite unique index
    __table_args__ = (
        PrimaryKeyConstraint('id', 'created_at', name='pk_task_id_created_at'),
        Index('idx_task_created_at', 'created_at'),
    )

    def __init__(self, name, task_type, created_at, created_by, status='scheduled'):
        self.name = name
        self.type = task_type
        self.created_at = created_at
        self.created_by = created_by
        self.status = status
