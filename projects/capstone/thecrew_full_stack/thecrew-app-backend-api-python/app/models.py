import uuid
from sqlalchemy_utils import UUIDType
from app import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType(binary=False), nullable=False, unique=True,
                     default=uuid.uuid4)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.id == other.id


class Gender(BaseModel):
    __tablename__ = 'genders'
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f'<Gender {self.name}>'


movies_actors = db.Table('movies_actors',
                         db.Column('movie_id', db.Integer, db.ForeignKey(
                             'movies.id'), primary_key=True),
                         db.Column('actor_id', db.Integer, db.ForeignKey(
                             'actors.id'), primary_key=True))


class Actor(BaseModel):
    __tablename__ = 'actors'
    age = db.Column(db.Integer)
    full_name = db.Column(db.String(60), nullable=False)
    gender = db.relationship('Gender', uselist=False)
    gender_id = db.Column(db.Integer, db.ForeignKey(
        'genders.id'), nullable=False)

    def __repr__(self):
        return f'<Actor {self.full_name}>'


class Movie(BaseModel):
    __tablename__ = 'movies'
    title = db.Column(db.String(140), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    actors = db.relationship('Actor', secondary=movies_actors,
                             backref=db.backref('movies', lazy='dynamic'),
                             lazy='dynamic')

    def __repr__(self):
        return f'<Movie {self.title}>'
