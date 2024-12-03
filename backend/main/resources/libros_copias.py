from flask import request, jsonify
from flask_restful import Resource
from main.models import LibrosCopiasModel, LibroModel
from .. import db


class LibrosCopias(Resource):
    def get(self):
        libros_copias = db.session.query(LibrosCopiasModel).all()
        return [libro_copia.to_json() for libro_copia in libros_copias]

    def post(self):
        libro_copia = LibrosCopiasModel.from_json(request.get_json())
        try:
            db.session.add(libro_copia)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar la copia del libro"}, 400    
        return libro_copia.to_json(), 201


class LibroCopia(Resource):
    def get(self, id):
        libro_copia = db.session.query(LibrosCopiasModel).get_or_404(id)
        return libro_copia.to_json()

    def put(self, id):
        libro_copia = db.session.query(LibrosCopiasModel).get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(libro_copia, key, value)
        try:
            db.session.add(libro_copia)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al actualizar la copia del libro"}, 400

    def delete(self, id):
        libro_copia = db.session.query(LibrosCopiasModel).get_or_404(id)
        try:
            db.session.delete(libro_copia)
            db.session.commit()
            return {"message": "Eliminado correctamente"}, 200
        except:
            db.session.rollback()
            return {"message": "Error al borrar la copia del libro"}, 400
