from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    total_points = Column(Integer, default=0)
    total_amount = Column(Float, default=0)
    transaction_count = Column(Integer, default=0)
    penalty = Column(Integer, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    user_id = Column(String)
    amount = Column(Float)
    points = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)