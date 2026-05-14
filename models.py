from database import Base
from sqlalchemy import Column, Integer,String

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key= True, autoincrement= True)
    url= Column(String)
    shortCode = Column(String, unique= True)
    createdAt= Column(String)
    updatedAt= Column(String)
    accessCount = Column(Integer)