import os
import uuid
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Form, File, UploadFile
from models import Base, Game, GameDB, PutGame, Keypoint, KeypointDB, PutKeypoint, User, UserDB,PutUser
from functions import gen_id


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
        UserDB(
            name="Alvin",
            points=10,
            game_id="JKDKJFD3",
            keypoints_solved=[]
        ),
        UserDB(
            name="Erik",
            points=25,
            game_id="JKDKJFD3",
            keypoints_solved=[]

        ),
        UserDB(
            name="Ashka",
            points=5,
            game_id="JKDKJFD3",
            keypoints_solved=[]

        ),
        UserDB(
            name="Johan",
            points=10,
            game_id="JKDKJFD3",
            keypoints_solved=[]
        ),

        UserDB(
            name="Wincaml",
            points=15,
            game_id="JKDKJFD3",
            keypoints_solved=[]
        ),
        KeypointDB(
            id=4,
            name="La résidence Léonard de Vinci",
            points=10,
            url_cible="https://rezoleo.fr",
            latitude=50.60891984079241,
            longitude=3.1479595389831827,
            game_id="JKDKJFD3",
            users_solvers=[]
        ),
        KeypointDB(
            id=5,
            name="Centrale Lille",
            points=10,
            url_cible="https://centralelille.fr",
            latitude=50.60671204431724,
            longitude=3.1362654536795187,
            game_id="JKDKJFD3",
            users_solvers=[]

        ),
        KeypointDB(
            id=1,
            name="Chimie Lille",
            points=20,
            url_cible="https://www.ensc-lille.fr/",
            latitude=50.60961737017392,
            longitude=3.1465197652352384,
            game_id="JKDKJFD3",
            users_solvers=[]

        ),
        KeypointDB(
            id=2,
            name="Stade Pierre Mauroy",
            points=30,
            url_cible="https://www.stade-pierre-mauroy.com/",
            latitude=50.611909431152135,
            longitude=3.1306297350229695,
            game_id="JKDKJFD3",
            users_solvers=[]
        ),
        KeypointDB(
            id=3,
            name="Polytech Lille",
            points=20,
            url_cible="https://www.polytech-lille.fr/",
            latitude=50.607782321056426,
            longitude=3.136245795396877,
            game_id="JKDKJFD3",
            users_solvers=[]
        ),
        GameDB(
            id="JKDKJFD3",
            name="Découverte du campus universitaire de Villeneuve d'Ascq",
            duration=10800,
            time_start=1592645436,
            nb_player_max=12,
            keypoints=[],
            users=[]
        ),
        GameDB(
            id="DJ83JDJF",
            name="Découverte de Paris",
            duration=21600,
            time_start=1591039848,
            nb_player_max=8,
            keypoints=[],
            users=[],
        ),
        GameDB(
            id="FUEIJE23",
            name="Découverte de Lille",
            duration=9000,
            time_start=1591019348,
            nb_player_max=6,
            keypoints=[],
            users=[]
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


def get_keypoint(db_session: Session, keypoint_id: int, game_id: str) -> Optional[KeypointDB]:
    return (
        db_session.query(KeypointDB)
        .filter(KeypointDB.game_id == game_id)
        .filter(KeypointDB.id == keypoint_id)
        .first()
    )


def get_all_keypoints(db_session: Session, game_id: str) -> List[Optional[KeypointDB]]:
    return (
        db_session.query(KeypointDB)
        .filter(KeypointDB.game_id == game_id)
        .all()
    )


def get_game(db_session: Session, game_id: str) -> Optional[GameDB]:
    return (
        db_session.query(GameDB)
        .filter(GameDB.id == game_id)
        .first()
    )


def get_all_games(db_session: Session) -> List[Optional[GameDB]]:
    return (
        db_session.query(GameDB)
        .all()
    )


def get_user(db_session: Session, user_id: str, game_id: str) -> Optional[UserDB]:
    return (
        db_session.query(UserDB)
        .filter(UserDB.game_id == game_id)
        .filter(UserDB.id == user_id)
        .first()
    )


def get_all_users(db_session: Session, game_id: str) -> List[Optional[UserDB]]:
    return (
        db_session.query(UserDB)
        .filter(UserDB.game_id == game_id)
        .all()
    )


app = FastAPI(title="ARriddle API", version=os.getenv("API_VERSION", "dev"))

# ---------------------------------- GET -------------------------------


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/games/{game_id}/keypoints/{keypoint_id}", summary="Récupère le point clé correspondant à l'id", response_model=Keypoint)
async def read_keypoint(keypoint_id: int, game_id: str, db: Session = Depends(get_db)):
    keypoint = get_keypoint(db, keypoint_id=keypoint_id, game_id=game_id)
    if keypoint is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return keypoint


@app.get("/games/{game_id}/keypoints", summary="Récupère tous les points clés", response_model=List[Keypoint])
async def read_all_keypoints(game_id: str, db: Session = Depends(get_db)):
    keypoints = get_all_keypoints(db, game_id=game_id)
    if keypoints is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return keypoints


@app.get("/games/{game_id}", summary="Récupère la partie correspondante à l'id", response_model=Game)
async def read_game(game_id: str, db: Session = Depends(get_db)):
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


@app.get("/games/{game_id}/users", summary="Récupère les utilisateurs la partie correspondante à l'id", response_model=List[User])
async def read_users(game_id: str, db: Session = Depends(get_db)):
    users = get_all_users(db, game_id=game_id)
    if users is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return users


@app.get("/games/{game_id}/users/{user_id}", summary="Récupère l'utilisateur correspondant à l'id de la partie correspondante à l'id de partie", response_model=User)
async def read_user(user_id: str, game_id: str, db: Session = Depends(get_db)):
    users = get_user(db, user_id=user_id, game_id=game_id)
    if users is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return users

# ---------------------------------- POST -------------------------------


@app.post("/games", summary="Crée une partie")
async def create_game(
        name: str,
        time_start: int,
        nb_player_max: int = None,
        duration: int = None,
        db: Session = Depends(get_db)):

    # Génération de la nouvelle partie
    new_game = GameDB(
        id=gen_id(8),
        name=name,
        duration=duration,
        time_start=time_start,
        nb_player_max=nb_player_max,
    )
    db_session.add(new_game)
    db_session.commit()
    db_session.refresh(new_game)
    return new_game


@app.post("/games/{game_id}/keypoints", summary="Crée un keypoint")
async def create_keypoints(
        name: str,
        points: int,
        game_id: str,
        latitude: float = None,
        longitude: float = None,
        url_cible: str = None,
        db: Session = Depends(get_db)):

    # Génération de la nouvelle partie
    new_keypoint = KeypointDB(
        name=name,
        points=points,
        game_id=game_id,
        latitude=latitude,
        longitude=longitude,
        url_cible=url_cible,
    )
    db_session.add(new_keypoint)
    db_session.commit()
    db_session.refresh(new_keypoint)
    return new_keypoint


@app.post("/games/{game_id}/users", summary="Crée un user")
async def create_keypoints(
        name: str,
        points: int,
        game_id: str,
        db: Session = Depends(get_db)):

    # Génération de la nouvelle partie
    new_user = UserDB(
        name=name,
        points=points,
        game_id=game_id,
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

# ------------------------- DELETE ------------------------------


@app.delete("/games/{game_id}", summary="Supprime une partie")
async def delete_game(
        game_id: str,
        db: Session = Depends(get_db)):
    try:
        game = db_session.query(GameDB).filter(GameDB.id == game_id).first()
        db_session.delete(game)
        db_session.commit()
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@app.delete("/games/{game_id}/users/{user_id}", summary="Supprime un user")
async def delete_user(
        game_id: str,
        user_id: int,
        db: Session = Depends(get_db)):
    try:
        user = db_session.query(UserDB).filter(UserDB.id == user_id).filter(UserDB.game_id==game_id).first()
        db_session.delete(user)
        db_session.commit()
    except:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@app.delete("/games/{game_id}/keypoints/{keypoint_id}", summary="Supprime un keypoint")
async def delete_keypoint(
        game_id: str,
        keypoint_id: int,
        db: Session = Depends(get_db)):
    try:
        keypoint = db_session.query(KeypointDB).filter(KeypointDB.id == keypoint_id).filter(KeypointDB.game_id==game_id).first()
        db_session.delete(keypoint)
        db_session.commit()
    except:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)


# ---------------------------- PUT --------------------------------------------

@app.put("/games/{game_id}", summary="Met à jour une partie", response_model=Game)
async def update_game(
    game_id: str, 
    updates: PutGame,
    db: Session = Depends(get_db)
):
    
    game = get_game(db, game_id=game_id)
    if game is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    for key, value in updates.dict().items():
        if value is not None:
            setattr(game, key, value)
    db.commit()
    db.refresh(game)
    return game

@app.put("/games/{game_id}/keypoints/{keypoint_id}", summary="Met à jour un keypoint", response_model=Keypoint)
async def update_game(
    game_id: str, 
    keypoint_id: int,
    updates: PutKeypoint,
    db: Session = Depends(get_db)
):
    
    keypoint = get_keypoint(db, game_id=game_id, keypoint_id=keypoint_id)
    if keypoint is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    for key, value in updates.dict().items():
        if value is not None:
            setattr(keypoint, key, value)
    db.commit()
    db.refresh(keypoint)
    return keypoint

@app.put("/games/{game_id}/users/{user_id}", summary="Met à jour un user", response_model=User)
async def update_game(
    game_id: str, 
    user_id: int,
    updates: PutUser,
    db: Session = Depends(get_db)
):
    
    user = get_user(db, game_id=game_id, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    
    for key, value in updates.dict().items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
