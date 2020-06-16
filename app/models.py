from __future__ import annotations
from pydantic import BaseModel, Schema, PositiveInt
from typing import List, Optional
from sqlalchemy import Boolean, Table, Column, Integer, String, create_engine, Float, ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Keypoint(BaseModel):
    id: int = Schema(..., gt=0, description="Id du points d'intérêt")
    name: str = Schema(..., min_length=1, description="Nom du point d'intérêt")
    points: int = Schema(..., description="Nombre de points")
    description: str = Schema(..., min_length=1, description="Question")
    solution: str = Schema(..., min_length=1, description="Solution")
    url_cible: Optional[str] = Schema(None, description="Url de l'image")
    latitude: Optional[float] = Schema(None, description = "Latitude du point clef")
    longitude: Optional[float] = Schema(None, description = "Longitude du point clef")
    game_id: str = Schema(None, description="Id de la partie")

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int = Schema(..., gt=0, description="Id de l'utilisateur")
    name: str = Schema(..., min_length=1, description="Nom de l'utilisateur")
    points: int = Schema(..., description="Nombre de points")
    game_id: str = Schema(None, description="Id de la partie")

    class Config:
        orm_mode = True

class Game(BaseModel):
    id: str = Schema(..., description="Id de la partie")
    name: str = Schema(..., min_length=1, description="Nom de la partie")
    visibility: bool = Schema(..., description="Partie publique ou privée")
    duration: Optional[int] = Schema(None, description="Durée de la partie")
    time_start: int = Schema(..., description="Heure de début de la partie")
    nb_player_max: Optional[int] = Schema(None, description="Nombre de joueurs max")
    keypoints: List[Keypoint] = Schema([], description="Points clefs composant la partie")
    users: List[User] = Schema([], description="Joueurs de la partie")

    class Config:
        orm_mode = True

class Solve(BaseModel):
    keypoint_id: int = Schema(..., gt=0, description="Id du points d'intérêt")
    user_id: int = Schema(..., gt=0, description="Id de l'utilisateur")
    game_id: str = Schema(..., description="Id de la partie")


    class Config:
        orm_mode = True

# ---------- Classes pour les routes PUT -----------------

class PutKeypoint(BaseModel):
    name: Optional[str] = Schema(None, min_length=1, description="Nom du point d'intérêt")
    points: Optional[int] = Schema(None, description="Nombre de points")
    description: Optional[str] = Schema(None, description="Question")
    solution: Optional[str] = Schema(None, description="Solution")
    url_cible: Optional[str] = Schema(None, description="Url de l'image")
    latitude: Optional[float] = Schema(None, description = "Latitude du point clef")
    longitude: Optional[float] = Schema(None, description = "Longitude du point clef")

    class Config:
        orm_mode = True

class PutUser(BaseModel):
    name: Optional[str] = Schema(None, min_length=1, description="Nom de l'utilisateur")
    points: Optional[int] = Schema(None, description="Nombre de points")

    class Config:
        orm_mode = True

class PutGame(BaseModel):
    name: Optional[str] = Schema(None, min_length=1, description="Nom de la partie")
    visibility: Optional[bool] = Schema(None, descrition="Partie publique ou privée")
    duration: Optional[int] = Schema(None, description="Durée de la partie")
    time_start: Optional[int] = Schema(None, description="Heure de début de la partie")
    nb_player_max: Optional[int] = Schema(None, description="Nombre de joueurs max")
  
    class Config:
        orm_mode = True



PutKeypoint.update_forward_refs()
PutUser.update_forward_refs()
Keypoint.update_forward_refs()
User.update_forward_refs()
Base = declarative_base()


# Transcription des classes de models.py pour les rendre
# au même format que la BdD.

class SolveDB(Base):
    __tablename__ = "solves"
    user_id = Column(Integer, primary_key=True, nullable=False)
    keypoint_id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(String, primary_key=True, nullable=False)



class KeypointDB(Base):
    __tablename__ = "keypoints"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable = False)
    solution = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=True)    
    longitude = Column(Float, nullable=True)
    url_cible = Column(String, nullable=True)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    # jointure
    game = relationship("GameDB", back_populates="keypoints")


class GameDB(Base):
    __tablename__ = "games"
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    visibility = Column(Boolean, nullable= False)
    duration = Column(Integer, nullable=True)
    time_start = Column(Integer, nullable=False)
    nb_player_max = Column(Integer, nullable=True)
    keypoints = relationship("KeypointDB", back_populates="game", cascade="delete")
    users = relationship("UserDB", back_populates="game", cascade="delete")


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    points = Column(Integer, nullable=False)
    game_id = Column(String, ForeignKey("games.id"), nullable=False)
    game = relationship("GameDB", back_populates="users")
