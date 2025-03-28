from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)

    # Связь один-ко-многим с UserGame
    games = relationship("UserGame", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}')>"


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    price = Column(Integer)

    # Связь один-ко-многим с UserGame
    user_games = relationship("UserGame", back_populates="tournament")

    # Связь многие-к-одному с Chat
    chat_id = Column(Integer, ForeignKey("chats.id"))
    chat = relationship("Chat", back_populates="tournaments")


class UserGame(Base):
    __tablename__ = "user_games"

    id = Column(Integer, primary_key=True)

    played_at = Column(DateTime)

    # количество закупов
    rebuys = Column(Integer, default=0)
    # время присоединения
    attached = Column(DateTime)
    # время окончания
    finished = Column(DateTime)

    # Занятое место
    position = Column(Integer)

    # Связь многие-к-одному с User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="games")

    # Связь многие-к-одному с Tournament
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="user_games")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    tg_id = Column(String(100))
    name = Column(String(100))

    # Связь один-ко-многим с Tournament
    tournaments = relationship("Tournament", back_populates="chat")

    def __repr__(self):
        return f"<Chat(name='{self.name}')>"


def main():

    # Создаем базовый класс для моделей (современный способ для SQLAlchemy 2.0+)

    # Создаем базу данных SQLite в памяти (можно заменить на файл: 'sqlite:///database.db')
    engine = create_engine("sqlite:///game_database.db")

    # Создаем все таблицы
    Base.metadata.create_all(engine)

    print("База данных и таблицы успешно созданы!")


if __name__ == "__main__":
    main()
