from flask_restful import Resource
from flask import request, jsonify
from main.models import AutorModel  
from .. import db

class Autores(Resource):
    def get(self):
        autores = db.session.query(AutorModel).all()
        return jsonify([autor.to_json() for autor in autores])
    
    def post(self):
        autor = AutorModel.from_json(request.get_json())
        try:
            db.session.add(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al agregar el autor"}, 400          
        return autor.to_json(), 201

class Autor(Resource):
    def get(self, id):   
        autor = db.session.query(AutorModel).get_or_404(id)
        return autor.to_json_complete()
    
    def delete(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        try:
            db.session.delete(autor)
            db.session.commit()
            return {"message": "Autor eliminado correctamente"}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al borrar el autor"}, 400

    def put(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(autor, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el autor"}, 400
        return autor.to_json(), 200

