#!/usr/bin/env python3

from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        try:
            page = int(request.args.get("page", 1))
        except (TypeError, ValueError):
            page = 1

        try:
            per_page = int(request.args.get("per_page", 5))
        except (TypeError, ValueError):
            per_page = 5

        pagination = (
            Book.query.order_by(Book.id.asc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        items = BookSchema(many=True).dump(pagination.items)
        response = {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "items": items,
        }
        return response, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)