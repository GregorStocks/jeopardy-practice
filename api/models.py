from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, ForeignKey

Base = declarative_base()


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, autoincrement=False)
    airdate = Column(String, nullable=False)
    game_comments = Column(String)
    game_type = Column(String, nullable=False)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False, unique=True)


class Clue(Base):
    __tablename__ = "clues"
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey(Game.id), nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    round = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    clue = Column(String, nullable=False)
    answer = Column(String, nullable=False)
