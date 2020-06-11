from pydantic import BaseModel, Schema, PositiveInt
from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, create_engine, Float, ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Keypoint(BaseModel):
    id: int = Schema(..., gt=0, description="Id du points d'intérêt")
    name: str = Schema(..., min_length=1, description="Nom du point d'intérêt")
    points: int = Schema(..., description="Nombre de points")
    url_cible: Optional[str] = Schema(None, description="Url de l'image")
    latitude: Optional[float] = Schema(..., description = "Latitude du point clef")
    longitude: Optional[float] = Schema(..., description = "Longitude du point clef")
    users: List[BaseModel] = Schema([], description="Utilisateurs ayant résolu le point clef")
    game_id: Optional[str] = Schema(None, description="Id de la partie")

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int = Schema(..., gt=0, description="Id de l'utilisateur")
    name: str = Schema(..., min_length=1, description="Nom de l'utilisateur")
    points: int = Schema(..., description="Nombre de points")
    keypoints: Optional[List[BaseModel]] = Schema([], description="Points clefs résolus")
    game_id: Optional[str] = Schema(None, description="Id de la partie")

    class Config:
        orm_mode = True


class Game(BaseModel):
    id: str = Schema(..., description="Id de la partie")
    name: str = Schema(..., min_length=1, description="Nom de la partie")
    duration: Optional[int] = Schema(..., description="Durée de la partie")
    time_start: int = Schema(..., description="Heure de début de la partie")
    nb_player_max: Optional[int] = Schema(..., description="Nombre de joueurs max")
    keypoints: Optional[List[Keypoint]] = Schema([], description="Points clefs composant la partie")
    users: Optional[List[User]] = Schema([], description="Joueurs de la partie")

    class Config:
        orm_mode = True


Base = declarative_base()


# Transcription des classes de models.py pour les rendre
# au même format que la BdD.


class KeypointDB(Base):
    __tablename__ = "keypoints"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    url_cible = Column(String)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    # jointure
    game = relationship("GameDB", back_populates="keypoints")



class GameDB(Base):
    __tablename__ = "games"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    time_start = Column(Integer, nullable=False)
    nb_player_max = Column(Integer, nullable=False)
    keypoints = relationship("KeypointDB", back_populates="game")
    users = relationship("UserDB", back_populates="game")




class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    game = relationship("GameDB", back_populates="users")
