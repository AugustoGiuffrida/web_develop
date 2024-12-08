from flask_restful import Resource
from flask import request
from .. import db
from main.models import NotificacionModel, UsuarioModel
from flask import jsonify
from sqlalchemy import func, desc, asc
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required


class Notificacion(Resource):
    @jwt_required()
    @role_required(roles=["admin", "librarian", "user"])
    def get(self, id):
        current_user_id = get_jwt_identity()
        rol = db.session.query(UsuarioModel).get_or_404(current_user_id).rol
        if current_user_id != id and rol != "admin":
            return {"message": "No tienes permiso para ver esta notificacion"}, 403
        notificacion = db.session.query(NotificacionModel).get_or_404(id)
        return notificacion.to_json(), 200


    @jwt_required()
    @role_required(roles=["admin", "librarian"])
    def delete(self, id):
        notificacion = db.session.query(NotificacionModel).get_or_404(id)
        try:
            db.session.delete(notificacion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error al borrar la notificacion", "error": str(e)}), 500
        return {"message": "Eliminado correctamente", "notificacion": notificacion.to_json()}, 200

    def put(self, id):
        notificacion = db.session.query(NotificacionModel).get_or_404(id)
        data = request.get_json()
        notificacion.titulo = data.get('titulo')
        notificacion.descripcion = data.get('descripcion')
        notificacion.vista = data.get('vista')
        notificacion.categoria = data.get('categoria')
        
        try:
            db.session.add(notificacion)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar la notificacion"}, 400
        return {"message": "Actualizado correctamente", "notificacion": notificacion.to_json()}, 200 


class Notificaciones(Resource):
    @jwt_required()
    @role_required(roles=["admin", "librarian", "user"])
    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 10
        
        # Obtener todas las notificaciones
        notificaciones = db.session.query(NotificacionModel)
        notificaciones = notificaciones.order_by(desc(NotificacionModel.notificacionID))

        current_user_id = get_jwt_identity()
        rol = db.session.query(UsuarioModel).get_or_404(current_user_id).rol
        if rol == "user":
            notificaciones = notificaciones.filter(NotificacionModel.usuarioID == current_user_id)

        if request.args.get('page'): ##Existe el parametro "page" en la request?
            page = int(request.args.get('page'))##Si existe, lo cargo
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        ### FILTROS ###
        #Filtro por usuario_id
        if request.args.get('usuarioID'):
            usuarioID = int(request.args.get('usuarioID'))
            notificaciones = notificaciones.filter_by(usuarioID=usuarioID) #se filtran las notificaciones que pertenecen al usuario con el id proporcionado.
            
        #Filtro por usuario_nombre:
        if request.args.get('usuario_nombre'):
            usuario_nombre = request.args.get('usuario_nombre')
            # Obtener el ID del usuario a partir del nombre
            usuario = db.session.query(UsuarioModel).filter_by(usuario_nombre=usuario_nombre).first() #consulta en la DB para encontrar el usuario con ese nombre 
            if usuario:
                notificaciones = notificaciones.filter_by(usuarioID=usuario.usuarioID)#se filtran las notificaciones que pertenecen al usuario con el id proporcionado.
            else:
                # Si no se encuentra el usuario, retornar una lista vacía
                return jsonify({"notificaciones": [], "message": f"No se encontró un usuario con el nombre {usuario_nombre}"}), 404
        ### FIN FILTROS ####     


        notificaciones = notificaciones.paginate(page=page, per_page=per_page, error_out=True)
        # Convertir resultados a JSON y retornar
        return jsonify({"notificaciones": [notificacion.to_json() for notificacion in notificaciones.items],
                        'total': notificaciones.total,
                        'pages': notificaciones.pages,
                        'page': page      
        })


    @jwt_required()
    @role_required(roles=["admin", "librarian"])
    def post(self):
        data = request.get_json()
        notificacion = NotificacionModel.from_json(data) #notificacion = notificacion.from_json(request.get_json()

        try:
            db.session.add(notificacion)
            db.session.commit()
        except Exception as e: 
            db.session.rollback()  #realiza un rollback de la sesión y luego devuelve el mensaje de error junto con el código de estado 400.      
            return {"message": "Error al agregar la notificacion" + str(e)}, 400 # Esto garantiza que cualquier cambio no se guarde en la base de datos si ocurre un error.
        return notificacion.to_json(), 201