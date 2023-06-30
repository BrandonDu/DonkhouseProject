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
            player_data = {
                'username': value.username,
                'stats': value.stats,
            }
            return json.dumps(player_data)
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
            game_data = value.__dict__.copy()
            game_data['date'] = game_data['date'].isoformat()  # Convert date to string
            return json.dumps(game_data)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            game_data = json.loads(value)
            game_data['date'] = datetime.fromisoformat(game_data['date']).date()  # Convert string to date
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


# server = 'MYSQL5048.site4now.net'
# database = 'db_a53d6c_donktrk'
# uid = 'a53d6c_donktrk'
# password = 'donkhouse72'
# driver = '{MySQL ODBC 8.0 UNICODE Driver}'
# #Create the connection URL for SQLAlchemy
# connection_string = f"mysql://{uid}:{password}@{server}/{database}"
# engine = create_engine(connection_string, echo=True)

#Drop existing tables
#Base.metadata.drop_all(bind=engine)

# Create new empty tables
# Base.metadata.create_all(bind=engine)
# engine.dispose()
