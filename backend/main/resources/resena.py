from flask_restful import Resource
from flask import request, jsonify
from main.models import ResenaModel,UsuarioModel, LibroModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required
from .. import db


class Resena(Resource):
    def get(self, id):   
        resena = db.session.query(ResenaModel).get_or_404(id)
        return resena.to_json_complete()


    @jwt_required()
    @role_required(roles=['admin','user'])
    def delete(self, id):
        resena = db.session.query(ResenaModel).get_or_404(id)
        usuario = db.session.query(UsuarioModel).get_or_404(resena.usuarioID)
        current_user_id = get_jwt_identity()
        rol = db.session.query(UsuarioModel).get_or_404(current_user_id).rol

        if current_user_id != usuario.usuarioID and rol != 'admin':
            return {"message": "No tienes permiso para borrar esta resena"}, 403
        libro = db.session.query(LibroModel).get_or_404(resena.libroID)

        if libro.libroID != resena.libroID:
            return {"message": "No tienes permiso para borrar esta resena"}, 403

        try:
            db.session.delete(resena)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al borrar la resena"}, 400
        return {"message": "Eliminado correctamente", "resena": resena.to_json()}, 200


    @jwt_required()
    @role_required(roles=['user'])
    def put(self, id):
        resena = db.session.query(ResenaModel).get_or_404(id)
        usuario = db.session.query(UsuarioModel).get_or_404(resena.usuarioID)
        current_user_id = get_jwt_identity()
        if current_user_id != usuario.usuarioID:
            return {"message": "No tienes permiso para editar esta resena"}, 403
        libro = db.session.query(LibroModel).get_or_404(resena.libroID)
        if libro.libroID != resena.libroID:
            return {"message": "No tienes permiso para editar esta resena"}, 403
        data = request.get_json()
        if data.get('valoracion'):
            resena.valoracion = data.get('valoracion')
        if data.get('comentario'):
            resena.comentario = data.get('comentario')
        try:
            db.session.add(resena)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar la resena"}, 400
        return {"message": "Actualizado correctamente", "resena": resena.to_json()}, 200    


class Resenas(Resource):
    def get(self):
        resenas = db.session.query(ResenaModel).all()
        return jsonify([resena.to_json() for resena in resenas])
    
    @jwt_required()
    @role_required(roles=['user'])
    def post(self):
            resena_json = request.get_json()
            db.session.query(UsuarioModel).get_or_404(resena_json.get('usuarioID'))
            db.session.query(LibroModel).get_or_404(resena_json.get('libroID'))
            resena= ResenaModel.from_json(request.get_json())
            try:
                db.session.add(resena)  # Agregar la resena a la sesión
                db.session.commit()  # Guardar la resena en la base de datos
            except:
                db.session.rollback()  # Deshacer cualquier cambio en la sesión de la base de datos
                return {"message": "Error al mostrar la resena"}, 500  # Devolver un mensaje de error genérico
            return resena.to_json(), 201  # Devolver la resena como JSON con código de estado 201 (creado)