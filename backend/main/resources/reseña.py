from flask_restful import Resource
from flask import request, jsonify
from main.models import ReseñaModel,UsuarioModel, LibroModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required
from .. import db


class Reseña(Resource):
    def get(self, id):   
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        return reseña.to_json_complete()


    @jwt_required()
    @role_required(roles=['admin','user'])
    def delete(self, id):
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        usuario = db.session.query(UsuarioModel).get_or_404(reseña.usuarioID)
        current_user_id = get_jwt_identity()

        if current_user_id != usuario.usuarioID and usuario.rol != 'admin':
            return {"message": "No tienes permiso para borrar esta reseña"}, 403
        libro = db.session.query(LibroModel).get_or_404(reseña.libroID)

        if libro.libroID != reseña.libroID:
            return {"message": "No tienes permiso para borrar esta reseña"}, 403

        try:
            db.session.delete(reseña)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al borrar la reseña"}, 400
        return {"message": "Eliminado correctamente", "reseña": reseña.to_json()}, 200


    @jwt_required()
    @role_required(roles=['user'])
    def put(self, id):
        reseña = db.session.query(ReseñaModel).get_or_404(id)
        usuario = db.session.query(UsuarioModel).get_or_404(reseña.usuarioID)
        current_user_id = get_jwt_identity()
        if current_user_id != usuario.usuarioID:
            return {"message": "No tienes permiso para editar esta reseña"}, 403
        libro = db.session.query(LibroModel).get_or_404(reseña.libroID)
        if libro.libroID != reseña.libroID:
            return {"message": "No tienes permiso para editar esta reseña"}, 403
        data = request.get_json()
        if data.get('valoracion'):
            reseña.valoracion = data.get('valoracion')
        if data.get('comentario'):
            reseña.comentario = data.get('comentario')
        try:
            db.session.add(reseña)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar la reseña"}, 400
        return {"message": "Actualizado correctamente", "reseña": reseña.to_json()}, 200    


class Reseñas(Resource):
    def get(self):
        reseñas = db.session.query(ReseñaModel).all()
        return jsonify([reseña.to_json() for reseña in reseñas])
    
    @jwt_required()
    @role_required(roles=['user'])
    def post(self):
            reseña_json = request.get_json()
            db.session.query(UsuarioModel).get_or_404(reseña_json.get('usuarioID'))
            db.session.query(LibroModel).get_or_404(reseña_json.get('libroID'))
            reseña= ReseñaModel.from_json(request.get_json())
            try:
                db.session.add(reseña)  # Agregar la reseña a la sesión
                db.session.commit()  # Guardar la reseña en la base de datos
            except:
                db.session.rollback()  # Deshacer cualquier cambio en la sesión de la base de datos
                return {"message": "Error al mostrar la reseña"}, 500  # Devolver un mensaje de error genérico
            return reseña.to_json(), 201  # Devolver la reseña como JSON con código de estado 201 (creado)
        

   



