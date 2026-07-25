from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from database import Base, engine


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)


# Automatically create the table in SQLite if it doesn't exist
Base.metadata.create_all(bind=engine)
