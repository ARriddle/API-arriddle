from pydantic import BaseModel, Schema, PositiveInt
from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, create_engine, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



class Keypoint(BaseModel):
    id: int = Schema(..., gt=0, description="Id du points d'intérêt")
    name: str = Schema(..., min_length=1, description="Nom du point d'intérêt")
    points: int = Schema(..., description="Nombre de points")
    url_cible: Optional[str] = Schema(
        None, description="Url de l'image")
    url_audio: Optional[str] = Schema(None, description="Url du fichier audio")
    game_id: Optional[int] = Schema(None, gt=0, description="Id de la partie")
    class Config:
        orm_mode = True


class Game(BaseModel):
    id: int = Schema(..., gt=0, description="Id de la partie")
    name: str = Schema(..., min_length=1, description="Nom de la partie")
    duration: int = Schema(..., description="Durée de la partie")
    time_start: int = Schema(..., description="Heure de début de la partie")
    nb_player: int = Schema(..., description="Nombre de joueurs")
    nb_player_max: int = Schema(..., description="Nombre de joueurs max")
    keypoints: List[Keypoint] = Schema(
        [], description="Points clefs composant la partie")
    class Config:
        orm_mode = True



"""
class User(BaseModel):
    id: int = Schema(..., gt=0, description="Id de l'utilisateur")
"""
Base = declarative_base()

# Transcription des classes de models.py pour les rendre
# au même format que la BdD.


class KeypointDB(Base):
    __tablename__ = "keypoints"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    name = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    url_cible = Column(String)
    url_audio = Column(String)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    # jointure
    game = relationship("GameDB", back_populates="keypoints")


class GameDB(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    time_start = Column(Integer, nullable=False)
    nb_player = Column(Integer, nullable=False)
    nb_player_max = Column(Integer, nullable=False)

    # jointure
    keypoints = relationship("KeypointDB", back_populates="game")
