from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import SQLALCHEMY_DATABASE_URL


Base = declarative_base()


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

def seed_data():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    # Проверка, есть ли уже данные
    if db.query(Message).count() == 0:
        messages = [
            Message(text=f"Static message number {i}") 
            for i in range(1, 11)
        ]
        db.add_all(messages)
        db.commit()
        print("Database seeded successfully!")
    else:
        print("Database already has data. Skipping seed.")
    
    db.close()

if __name__ == "__main__":
    seed_data()
