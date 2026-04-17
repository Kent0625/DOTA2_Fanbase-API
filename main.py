from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional

# --- DATABASE SETUP (SQLite) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./dota2.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLALCHEMY MODELS ---
class VoiceActor(Base):
    __tablename__ = "voice_actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    heroes = relationship("Hero", back_populates="voice_actor")

class Hero(Base):
    __tablename__ = "heroes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    primary_attribute = Column(String)
    attack_type = Column(String)
    voice_actor_id = Column(Integer, ForeignKey("voice_actors.id"))
    voice_actor = relationship("VoiceActor", back_populates="heroes")

# --- PYDANTIC SCHEMAS ---
class HeroBase(BaseModel):
    name: str
    primary_attribute: str
    attack_type: str

class HeroResponse(HeroBase):
    id: int
    voice_actor_id: Optional[int]

    class Config:
        from_attributes = True

class VoiceActorResponse(BaseModel):
    id: int
    name: str
    heroes: List[HeroResponse] = []

    class Config:
        from_attributes = True

# --- FASTAPI APP & SEED DATA ---
app = FastAPI(title="Dota 2 Fanbase API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    # Force refresh: Drop and recreate tables to ensure new data is loaded
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Define Voice Actors
    actors = {
        "John Patrick Lowrie": VoiceActor(name="John Patrick Lowrie"),
        "Gin Hammond": VoiceActor(name="Gin Hammond"),
        "Dennis Bateman": VoiceActor(name="Dennis Bateman"),
        "Ellen McLain": VoiceActor(name="Ellen McLain"),
        "Nolan North": VoiceActor(name="Nolan North"),
        "Fred Tatasciore": VoiceActor(name="Fred Tatasciore"),
        "TJ Ramini": VoiceActor(name="TJ Ramini"),
        "Linda K. Morris": VoiceActor(name="Linda K. Morris"),
        "Barry Dennen": VoiceActor(name="Barry Dennen"),
        "Sam Mowry": VoiceActor(name="Sam Mowry"),
        "Dave Fennoy": VoiceActor(name="Dave Fennoy"),
        "Gary Schwartz": VoiceActor(name="Gary Schwartz"),
        "Jim French": VoiceActor(name="Jim French"),
        "Eric Newsome": VoiceActor(name="Eric Newsome")
    }
    db.add_all(actors.values())
    db.commit()

    # Define Heroes (Comprehensive List - Unique Names Only)
    heroes_data = [
        # STRENGTH
        ("Axe", "Strength", "Melee", "John Patrick Lowrie"),
        ("Earthshaker", "Strength", "Melee", "John Patrick Lowrie"),
        ("Pudge", "Strength", "Melee", "John Patrick Lowrie"),
        ("Sven", "Strength", "Melee", "Fred Tatasciore"),
        ("Tiny", "Strength", "Melee", "Fred Tatasciore"),
        ("Kunkka", "Strength", "Melee", "John Patrick Lowrie"),
        ("Dragon Knight", "Strength", "Melee", "TJ Ramini"),
        ("Clockwerk", "Strength", "Melee", "Gin Hammond"),
        ("Omniknight", "Strength", "Melee", "TJ Ramini"),
        ("Huskar", "Strength", "Ranged", "TJ Ramini"),
        ("Alchemist", "Strength", "Melee", "Nolan North"),
        ("Centaur Warrunner", "Strength", "Melee", "Sam Mowry"),
        ("Timbersaw", "Strength", "Melee", "TJ Ramini"),
        ("Bristleback", "Strength", "Melee", "TJ Ramini"),
        ("Tusk", "Strength", "Melee", "TJ Ramini"),
        ("Elder Titan", "Strength", "Melee", "Jim French"),
        ("Legion Commander", "Strength", "Melee", "Linda K. Morris"),
        ("Earth Spirit", "Strength", "Melee", "TJ Ramini"),
        ("Mars", "Strength", "Melee", "Fred Tatasciore"),
        ("Primal Beast", "Strength", "Melee", "Fred Tatasciore"),

        # AGILITY
        ("Anti-Mage", "Agility", "Melee", "Sam Mowry"),
        ("Drow Ranger", "Agility", "Ranged", "Gin Hammond"),
        ("Juggernaut", "Agility", "Melee", "John Patrick Lowrie"),
        ("Morphling", "Agility", "Ranged", "Sam Mowry"),
        ("Phantom Assassin", "Agility", "Melee", "Gin Hammond"),
        ("Sniper", "Agility", "Ranged", "Sam Mowry"),
        ("Templar Assassin", "Agility", "Ranged", "Linda K. Morris"),
        ("Luna", "Agility", "Ranged", "Linda K. Morris"),
        ("Bounty Hunter", "Agility", "Melee", "Sam Mowry"),
        ("Ursa", "Agility", "Melee", "Dave Fennoy"),
        ("Gyrocopter", "Agility", "Ranged", "TJ Ramini"),
        ("Troll Warlord", "Agility", "Melee", "TJ Ramini"),
        ("Ember Spirit", "Agility", "Melee", "TJ Ramini"),
        ("Monkey King", "Agility", "Melee", "TJ Ramini"),
        ("Hoodwink", "Agility", "Ranged", "TJ Ramini"),

        # INTELLIGENCE
        ("Crystal Maiden", "Intelligence", "Ranged", "Gin Hammond"),
        ("Puck", "Intelligence", "Ranged", "Gin Hammond"),
        ("Storm Spirit", "Intelligence", "Ranged", "Gary Schwartz"),
        ("Zeus", "Intelligence", "Ranged", "John Patrick Lowrie"),
        ("Lina", "Intelligence", "Ranged", "Gin Hammond"),
        ("Shadow Shaman", "Intelligence", "Ranged", "Gary Schwartz"),
        ("Tinker", "Intelligence", "Ranged", "Dennis Bateman"),
        ("Nature's Prophet", "Intelligence", "Ranged", "John Patrick Lowrie"),
        ("Enchantress", "Intelligence", "Ranged", "Gin Hammond"),
        ("Jakiro", "Intelligence", "Ranged", "Dave Fennoy"),
        ("Silencer", "Intelligence", "Ranged", "TJ Ramini"),
        ("Ogre Magi", "Intelligence", "Melee", "Nolan North"),
        ("Rubick", "Intelligence", "Ranged", "Barry Dennen"),
        ("Disruptor", "Intelligence", "Ranged", "TJ Ramini"),
        ("Skywrath Mage", "Intelligence", "Ranged", "TJ Ramini"),
        ("Oracle", "Intelligence", "Ranged", "TJ Ramini"),

        # UNIVERSAL
        ("Abaddon", "Universal", "Melee", "TJ Ramini"),
        ("Bane", "Universal", "Ranged", "TJ Ramini"),
        ("Batrider", "Universal", "Ranged", "Gin Hammond"),
        ("Beastmaster", "Universal", "Melee", "TJ Ramini"),
        ("Brewmaster", "Universal", "Melee", "Nolan North"),
        ("Broodmother", "Universal", "Melee", "Gin Hammond"),
        ("Chen", "Universal", "Ranged", "TJ Ramini"),
        ("Dark Seer", "Universal", "Melee", "TJ Ramini"),
        ("Dark Willow", "Universal", "Ranged", "TJ Ramini"),
        ("Dazzle", "Universal", "Ranged", "TJ Ramini"),
        ("Enigma", "Universal", "Ranged", "TJ Ramini"),
        ("Invoker", "Universal", "Ranged", "Dennis Bateman"),
        ("Io", "Universal", "Ranged", "TJ Ramini"),
        ("Lone Druid", "Universal", "Melee", "TJ Ramini"),
        ("Lycan", "Universal", "Melee", "TJ Ramini"),
        ("Magnus", "Universal", "Melee", "TJ Ramini"),
        ("Marci", "Universal", "Melee", "TJ Ramini"),
        ("Mirana", "Universal", "Ranged", "Gin Hammond"),
        ("Nyx Assassin", "Universal", "Melee", "TJ Ramini"),
        ("Pangolier", "Universal", "Melee", "TJ Ramini"),
        ("Phoenix", "Universal", "Ranged", "TJ Ramini"),
        ("Sand King", "Universal", "Melee", "TJ Ramini"),
        ("Snapfire", "Universal", "Ranged", "TJ Ramini"),
        ("Techies", "Universal", "Ranged", "Gin Hammond"),
        ("Vengeful Spirit", "Universal", "Ranged", "Gin Hammond"),
        ("Venomancer", "Universal", "Ranged", "TJ Ramini"),
        ("Visage", "Universal", "Ranged", "TJ Ramini"),
        ("Void Spirit", "Universal", "Melee", "TJ Ramini"),
        ("Windranger", "Universal", "Ranged", "Gin Hammond"),
        ("Winter Wyvern", "Universal", "Ranged", "TJ Ramini")
    ]

    # Add heroes to DB
    for name, attr, attack, actor_name in heroes_data:
        hero = Hero(
            name=name, 
            primary_attribute=attr, 
            attack_type=attack, 
            voice_actor_id=actors[actor_name].id
        )
        db.add(hero)
    
    db.commit()
    db.close()

# --- API ENDPOINTS ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Dota 2 Fanbase API. Go to /docs for the Swagger UI."}

@app.get("/heroes/", response_model=List[HeroResponse], tags=["Heroes"])
def get_all_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """1. Get All Characters (Heroes)"""
    return db.query(Hero).offset(skip).limit(limit).all()

@app.get("/heroes/{name}", response_model=HeroResponse, tags=["Heroes"])
def get_specific_hero(name: str, db: Session = Depends(get_db)):
    """2. Get a Specific Character by Name"""
    hero = db.query(Hero).filter(Hero.name == name).first()
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.get("/actors/", response_model=List[VoiceActorResponse], tags=["Actors"])
def get_all_actors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """3. Get Actors (and the heroes they voice)"""
    return db.query(VoiceActor).offset(skip).limit(limit).all()
