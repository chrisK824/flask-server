from flask import Flask
import os
from app.schemas import db, marshmallow, MemberSchema, BookSchema
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../storage.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
with app.app_context():
    db.create_all()
marshmallow.init_app(app)

# initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

from . import memberRoutes, bookRoutes

