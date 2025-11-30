from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship(
        "User_Favorite", back_populates="user", uselist=True)

    def __repr__(self):
        return f"<User {self.user!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }


class Star_Systems(db.Model):
    __tablename__ = 'star_systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    galactic_coordinates = db.Column(db.String(50))

    def __repr__(self):
        return f"<Star_Systems {self.star_systems!r}>"

    def serialize(self):
        return {
            "id":  self.id,
            "name": self.name,
            "galactic_coordiantes": self.galactic_coordinates
        }


class Factions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    leader = db.Column(db.String, unique=True, nullable=False)
    organization_type = db.Column(db.String)
    capital = db.Column(db.String)
    affiliation = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Factions {self.factions!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "leader": self.leader,
            "organization_type": self.organization_type,
            "capital": self.capital,
            "affiliation": self.affiliation,
        }


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(100))
    climate = db.Column(db.String(100))
    favorite_planets = db.relationship(
        "User_Favorite", back_populates="planets", uselist=True)

    def __repr__(self):
        return f"<Planets {self.planets!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "favorites": [favorite.serialize() for favorite in self.favorite_planets],
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
        }


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    classification = db.Column(db.String(100), unique=True, nullable=False)
    lifespan = db.Column(db.Integer)
    language = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Species {self.species!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "lifespan": self.lifespan,
            "language": self.language,
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String)
    occupation = db.Column(db.String(50))
    favorite_characters = db.relationship(
        "User_Favorite", back_populates="characters", uselist=True)

    def __repr__(self):
        return f"<Characters {self.chaaracters!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "weight": self.weight,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "occupation": self.occupation
        }


class User_Favorite(db.Model):
    __tablename__ = 'user_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_Id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    planet_Id = db.Column(db.Integer, db.ForeignKey(
        'planets.id'), nullable=True)
    planets = db.relationship(Planets)
    character_id = db.Column(db.Integer, db.ForeignKey(
        'characters.id'), nullable=True)
    characters = db.relationship(Characters)
    name_of_favorite = db.Column(db.String(100), nullable=False)
    __table_args__ = (db.UniqueConstraint(
        "user_Id", "name_of_favorite", "id", name="unique_favorite"),)

    def __repr__(self):
        return f"<User_Favorite {self.user_favorite!r}>"

    def serialize(self):
        return {
            "id": self.id,
            "name_of_favorite": self.name_of_favorite,
            "planet_id": self.planet_Id,
            "character_id": self.character_id,
        }
