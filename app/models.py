from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String , ForeignKey , Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null , text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , nullable=False)
    email = Column(String, unique=True,  nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))


class SchoolShoes(Base):
    __tablename__ = "school_shoes"

    id = Column(Integer, primary_key=True , nullable=False)
    size = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    boysORgirls = Column(String, nullable=False)
    quntity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    
class SchoolShirts(Base):
    __tablename__ = "school_shirts"

    id = Column(Integer, primary_key=True , nullable=False)
    size = Column(Float, nullable=False)
    quntity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))

class SchoolShorts(Base):
    __tablename__ = "school_shorts"

    id = Column(Integer, primary_key=True , nullable=False)
    size = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    type = Column(String, nullable=False)
    quntity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    
class SchoolFrocks(Base):
    __tablename__ = "school_frocks"

    id = Column(Integer, primary_key=True , nullable=False)
    size = Column(String, nullable=False)
    quntity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))