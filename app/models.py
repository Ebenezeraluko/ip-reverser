from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ReverseIP(Base):
    __tablename__ = "reverse_ips"

    id = Column(Integer, primary_key=True, index=True)
    original_ip = Column(String, index=True)
    reversed_ip = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
