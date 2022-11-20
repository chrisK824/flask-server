from app import app, db, book_schema, books_schema
from app.schemas import Book
from utils.defines import Messages as msg
from utils.defines import ErrorMessages as err
from utils.utils import customResponse
from uuid import uuid4
import sqlalchemy
from flask import request


@app.route('/books', methods=['GET', 'POST'])
def GetPostBooks():
    if request.method == 'GET':
        books = Book.query.all()
        return customResponse(books_schema.dump(books))
    elif request.method == 'POST':
        # FIXME : Validate input for headers, fields and return 400 for bad requests
        post_data = request.get_json()
        new_book = Book(name=post_data['name'],
                        author=post_data['author'],
                        category=post_data['category'],
                        pages=post_data['pages'],
                        publish_date=post_data['publish_date'],
                        id=str(uuid4()))

        try:
            db.session.add(new_book)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return customResponse(err.INTEGRITY, 403)
        return customResponse(book_schema.dump(new_book))


@app.route('/books/<id>', methods=['GET', 'PUT', 'DELETE'])
def GetPutDeleteBook(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        return customResponse(err.NOT_FOUND.format('Book'), 404)

    if request.method == 'GET':
        return customResponse(book_schema.dump(book))

    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return customResponse(msg.DELETE_SUCCESS.format('Book'))

    if request.method == 'PUT':
        post_data = request.get_json()

        book.name = post_data['name']
        book.author = post_data['author']
        book.category = post_data['category']
        book.pages = post_data['pages']
        book.publish_date = post_data['publish_date']

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return customResponse(err.INTEGRITY, 403)

        return customResponse(book_schema.dump(book))
