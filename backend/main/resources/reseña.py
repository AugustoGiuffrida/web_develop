from flask_restful import Resource
from flask import request, jsonify
from main.models import ReseñaModel
from .. import db

class Reseñas(Resource):
    def get(self):
        reseñas = db.session.query(ReseñaModel).all()
        return jsonify([reseña.to_json() for reseña in reseñas])
    
    def post(self):
            reseña= ReseñaModel.from_json(request.get_json())
            try:
                db.session.add(reseña)  # Agregar la reseña a la sesión
                db.session.commit()  # Guardar la reseña en la base de datos
            except:
                db.session.rollback()  # Deshacer cualquier cambio en la sesión de la base de datos
                return {"message": "Error al mostrar la reseña"}, 500  # Devolver un mensaje de error genérico
            return reseña.to_json(), 201  # Devolver la reseña como JSON con código de estado 201 (creado)
        

class Reseña(Resource):
    def get(self, id):   
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        return reseña.to_json_complete()
    
    def delete(self, id):
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        try:
            db.session.delete(reseña)
            db.session.commit()
            return {"message": "Eliminado correctamente"}, 200
        except:
            db.session.rollback()
            return {"message": "Error al borrar la reseña"}, 400

    def put(self, id):
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(reseña, key, value)
        try:
            db.session.add(reseña)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar la reseña"}, 400
   



