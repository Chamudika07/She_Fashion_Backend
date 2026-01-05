from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String , ForeignKey
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
