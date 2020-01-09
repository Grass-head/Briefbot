from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brief(Base):
    __tablename__ = 'brief'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    is_active = Column(Boolean)


