import os
import uuid
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Form, File, UploadFile
from models import Base, Game, GameDB, Keypoint, KeypointDB

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import joinedload

from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND

SQLALCHEMY_DATABASE_URI = "sqlite:///./database_arriddle.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
db_session = SessionLocal()

# Permet de créer la base de données avec une oeuvre si ce n'est pas déjà fait
try:
    test_games = [
        GameDB(
        id=1,
        name="Partie 1",
        duration=7200,
        time_start=1591019348,
        nb_player=0,
        nb_player_max=12,
        keypoints=[
            KeypointDB(
                id=1,
                name="Centrale Lille",
                points=10,
                url_cible="https://duckduckgo.com",
                url_audio="https://rezoleo.fr",
                game_id=1,
            ),
        ],
    ),
    GameDB(
        id=2,
        name="Partie 2",
        duration=3600,
        time_start=1591039848,
        nb_player=2,
        nb_player_max=12,
        keypoints=[
            KeypointDB(
                id=2,
                name="IG21",
                points=30,
                url_cible="https://duckduckgo.com",
                url_audio="https://re2o.rezoleo.fr",
                game_id=2,
            ),
            KeypointDB(
                id=3,
                name="ITEM",
                points=20,
                url_cible="https://duckduckgo.com",
                url_audio="https://re2o.rezoleo.fr",
                game_id=2,
            ),
        ],
    ),
    GameDB(
        id=3,
        name="Partie 3",
        duration=9780,
        time_start=1591019348,
        nb_player=4,
        nb_player_max=8,
        keypoints=[
            KeypointDB(
                id=4,
                name="Centrale Paris",
                points=10,
                url_cible="https://duckduckgo.com",
                url_audio="https://rezoleo.fr",
                game_id=3,
            ),
            KeypointDB(
                id=5,
                name="Centrale Lyon",
                points=10,
                url_cible="https://duckduckgo.com",
                url_audio="https://rezoleo.fr",
                game_id=3,
            ),
        ],
    ),
    ]
    
    db_session.add_all(test_games)
    db_session.commit()

except exc.IntegrityError:
    print("BdD déjà initialisée")

db_session.close()


# Dependency
def get_db():
    try:
        yield db_session
    finally:
        db_session.close()


def get_keypoint(db_session: Session, keypoint_id: int) -> Optional[KeypointDB]:
    return (
        db_session.query(KeypointDB)
        .filter(KeypointDB.id == keypoint_id)
        .first()
    )


def get_all_keypoints(db_session: Session) -> List[Optional[KeypointDB]]:
    return (
        db_session.query(KeypointDB)
        .options(
            joinedload(KeypointDB.game),
        )  # L'option joinedload réalise la jointure dans python
        .all()
    )


def get_game(db_session: Session, game_id: int) -> Optional[GameDB]:
    return (
        db_session.query(GameDB)
        .filter(GameDB.id == game_id)
        .first()
    )


def get_all_games(db_session: Session) -> List[Optional[GameDB]]:
    return (
        db_session.query(GameDB)
        .options(
            joinedload(GameDB.keypoints),
        )  # L'option joinedload réalise la jointure dans python
        .all()
    )


app = FastAPI(title="ARriddle API", version=os.getenv("API_VERSION", "dev"))


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/keypoints/{keypoint_id}", summary="Récupère le point clé correspondant à l'id", response_model=Keypoint)
async def read_oeuvre(keypoint_id: int, db: Session = Depends(get_db)):
    keypoint = get_keypoint(db, keypoint_id=keypoint_id)
    if keypoint is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return keypoint


@app.get("/keypoints", summary="Récupère tous les points clés", response_model=List[Keypoint])
async def read_all_keypoints(db: Session = Depends(get_db)):
    keypoints = get_all_keypoints(db)
    if keypoints is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return keypoints


@app.get("/games/{game_id}", summary="Récupère la partie correspondante à l'id", response_model=Game)
async def read_game(game_id: int, db: Session = Depends(get_db)):
    game = get_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return game


@app.get("/games", summary="Récupère toutes les parties", response_model=List[Game])
async def read_all_games(db: Session = Depends(get_db)):
    games = get_all_games(db)
    if games is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return games


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
