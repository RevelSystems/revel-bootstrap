from datetime import datetime, timedelta
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SessionExpiredException(Exception):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(60))
    is_admin = Column(Boolean)
    created = Column(DateTime)

    def __init__(self, email):
        self.email = email
        self.is_admin = False
        self.created = datetime.utcnow()


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    value = Column(String(16))
    created = Column(DateTime)
    expires = Column(DateTime)

    def __init__(self, user):
        self.user_id = user
        self.value = unicode(uuid.uuid4())
        self.created = datetime.utcnow()
        self.expires = self.created + timedelta(hours=1)

    def prolong(self):
        if self.is_valid:
            self.expires = datetime.utcnow() + timedelta(hours=1)
        else:
            raise SessionExpiredException("user_id {} session #{} has expired".format(self.user_id, self.id))

    @property
    def is_valid(self):
        return datetime.utcnow() < self.expires


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    issuer_id = Column(Integer, ForeignKey("user.id"))
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
