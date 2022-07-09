from flask import request
from flask_restplus import Resource, fields

from models.book_model import BookModel
from schemas.book_schema import BookSchema

from server.instance import server

book_ns = server.book_ns

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)


class Book(Resource):
    def get(self, id):
        book_data = BookModel.find_by_id(id)

        if book_data:
            print("Book Data directly from database: ", book_data)
            return book_schema.dump(book_data), 200

        return {"message": "Book not found"}, 404
