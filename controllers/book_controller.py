from flask import request
from flask_restplus import Resource, fields

from models.book_model import BookModel
from schemas.book_schema import BookSchema

from server.instance import server

book_ns = server.book_ns

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

item = book_ns.model(
    "Book",
    {
        "title": fields.String(description="Book title"),
        "pages": fields.Integer(default=0),
    },
)


class Book(Resource):
    @book_ns.doc("List a book")
    def get(self, id):
        book_data = BookModel.find_by_id(id)

        if book_data:
            return book_schema.dump(book_data), 200

        return {"message": "Book not found"}, 404

    @book_ns.expect(item)
    @book_ns.doc("Update a book")
    def put(self, id):
        book_json = request.get_json()

        book_data = BookModel.find_by_id(id)

        if not book_data:
            return {"message": "Invalid book"}, 400

        book_data.title = book_json["title"]
        book_data.pages = book_json["pages"]

        book_data.save_to_db()

        return book_schema.dump(book_data), 200

    @book_ns.doc("Delete a book")
    def delete(self, id):
        book_data = BookModel.find_by_id(id)

        if not book_data:
            return {"message": "Invalid book"}, 400

        book_data.delete_from_db()

        return {"message": "Book deleted successfully"}, 200


class BookList(Resource):
    def get(self):
        return book_list_schema.dump(BookModel.find_all()), 200

    @book_ns.expect(item)
    @book_ns.doc("Create a book")
    def post(self):
        # o metodo get_json() pega todos os dados que estão no body da requisição
        book_json = request.get_json()

        # recebe todo o dicionário python e o transforma em um objeto que pode
        # ser utilizado no banco de dados
        book_data = book_schema.load(book_json)

        book_data.save_to_db()

        return book_schema.dump(book_data), 201
