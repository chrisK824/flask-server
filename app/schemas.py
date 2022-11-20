from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields

db = SQLAlchemy()
marshmallow = Marshmallow()


class Member(db.Model):
    id = db.Column(db.String(200), primary_key=True,
                   unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    nationality = db.Column(db.String(80), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean(200), default=False, nullable=False)
    active = db.Column(db.Boolean(200), nullable=False)
    __table_args__ = (db.UniqueConstraint('username', 'email'),)


class Book(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True,
                   nullable=False)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publish_date = db.Column(db.Integer(), nullable=False)
    __table_args__ = (db.UniqueConstraint('name', 'author'),)


class MemberSchema(marshmallow.ModelSchema):
    class Meta:
        model = Member
        fields = ('id', 'name', 'lastname', 'username', 'email', 'age',
                  'gender', 'nationality', 'registration_date', 'active')


class BookSchema(marshmallow.ModelSchema):
    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'category', 'pages', 'publish_date')
