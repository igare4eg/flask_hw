from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    create_engine,
    func,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import PG_DSN


engine = create_engine(PG_DSN)
Base = declarative_base(bind=engine)


class AdsModel(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", backref="ads")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


Base.metadata.create_all()

Session = sessionmaker(bind=engine)
