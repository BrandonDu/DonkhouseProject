import json

from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Text,
    Integer,
    Float,
    Date,
    Table,
    TypeDecorator
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from game import Game
from player import Player
import datetime

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("player_id", ForeignKey("players.id")),
    Column("game_id", ForeignKey("games.id")),
)

class PlayerType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value.__dict__)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            player_data = json.loads(value)
            return Player.fromdict(player_data)
        return None

class PlayerTable(Base):
    __tablename__ = "players"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column('username', Text)
    stats = Column("stats", PlayerType)
    games = relationship(
        "GameTable", secondary=association_table, back_populates="players"
    )

    def __init__(self, player : Player):
        self.username = player.username
        self.stats = player


class GameType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value.to_dict())
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            game_data = json.loads(value)
            return Game.fromdict(game_data)
        return None


class GameTable(Base):
    __tablename__ = "games"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", Text)
    date = Column("date", Date)
    player_nets = Column("playerNets", GameType)
    players = relationship(
        "PlayerTable", secondary=association_table, back_populates="games"
    )

    def __init__(self, game: Game):
        self.name = game.name
        self.date = game.date
        self.player_nets = game
        

    def __repr__(self):
        return f"Game(id={self.id}, date={self.date}, name='{self.name}')"
