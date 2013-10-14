from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(60))
    is_admin = Column(Boolean)
    created = Column(DateTime)

    def __init__(self, email):
        self.email = email
        self.is_admin = False
        self.created = datetime.utcnow()


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    issuer_id = Column(Integer, ForeignKey('user.id'))
    type = Column(String(20))
    status = Column(String(12))
    log = Column(Text)
    created = Column(DateTime)
    updated = Column(DateTime)

    def __init__(self, task_type, user):
        self.type = task_type
        if user:
            self.issuer_id = user.id
        self.status = "scheduled"
        self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.log = None

    def start(self):
        self.status = "started"
        self.updated = datetime.utcnow()

    def finish(self, log):
        self.status = "finished"
        self.updated = datetime.utcnow()
        self.log = log

    def error(self, log):
        self.status = "failed"
        self.updated = datetime.utcnow()
        self.log = log
