from venv import logger
from flask_restful import Resource
from flask import request
from .. import db
from sqlalchemy import func
from main.models import UsuarioModel, NotificacionModel, PrestamoModel
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required

class Usuario(Resource): #A la clase usuario le indico que va a ser del tipo recurso(Resource)
    
    #obtener recurso 
    @jwt_required()
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        current_user_id = get_jwt_identity()
        if current_user_id:
            return usuario.to_json_complete()
        else:
            return usuario.to_json()


    #eliminar recurso
    @jwt_required()
    @role_required(roles=["admin", "user"])
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        current_user_id = get_jwt_identity()
        rol = db.session.query(UsuarioModel).get_or_404(current_user_id).rol
        print(current_user_id, rol)
        if current_user_id != id and rol != "admin":
            return {"message": "No tienes permiso para eliminar este usuario"}, 403
        try:
            # Eliminar notificaciones relacionadas
            db.session.query(NotificacionModel).filter(NotificacionModel.usuarioID == id).delete()

            # Ahora eliminar el usuario
            db.session.delete(usuario)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al borrar al usuario", "error": str(e)}, 400
        return {"message": "Eliminado correctamente"}, 201
            
    #Modificar el recurso usuario
    @jwt_required()
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        if usuario.usuarioID != get_jwt_identity():
            return {"message": "No tienes permiso para editar este usuario"}, 403
        for key, value in data:
            if key == 'rol' and usuario.rol != 'admin':
                continue
            setattr(usuario, key, value)
        try:
            db.session.commit()  
        except:
            db.session.rollback()
            return {"message": "Error al agregar al usuario"}, 400
        return usuario.to_json(), 200

class Usuarios(Resource):
    @jwt_required()
    @role_required(roles=["admin", "librarian"]) 
    def get(self):

        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 9
        
        usuarios = db.session.query(UsuarioModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))
        
        params = request.args
        
        ### FILTROS ###
        # Filtrar por nombre 
        if request.args.get('nombre'):
            usuarios = usuarios.filter(UsuarioModel.usuario_nombre.like(f"%{request.args.get('nombre')}%"))       
        if 'apellido_nombre' in params:
            usuarios = usuarios.order_by(UsuarioModel.usuario_nombre.desc())    
        # Filtrar por apellido 
        if request.args.get('apellido'):
            usuarios = usuarios.filter(UsuarioModel.usuario_apellido.like(f"%{request.args.get('apellido')}%"))     
        if 'apellido_titulo' in params:
            usuarios = usuarios.order_by(UsuarioModel.usuario_apellido.desc())
        # Filtrar por rol
        if request.args.get('rol'):
            usuarios = usuarios.filter(UsuarioModel.rol == request.args.get('rol'))
        if 'sortby_rol' in params:
            usuarios = usuarios.order_by(UsuarioModel.rol.desc())    
        # Filtrar por número de préstamos 
        if request.args.get('nr_prestamos'):
            # Convierte el valor de préstamos a entero
            nr_prestamos = int(request.args.get('nr_prestamos'))
            
            # Subquery para contar el número de préstamos por usuario
            subquery = db.session.query(
                PrestamoModel.usuarioID,
                func.count(PrestamoModel.prestamoID).label('total_prestamos')
            ).group_by(PrestamoModel.usuarioID).subquery()

            # Filtrar usuarios que tienen el número específico de préstamos solicitado
            usuarios = usuarios.join(subquery, UsuarioModel.usuarioID == subquery.c.usuarioID) \
                            .filter(subquery.c.total_prestamos == nr_prestamos) \
                            .order_by(subquery.c.total_prestamos.desc())

        ### FIN FILTROS ####     
          
        #Obtener valor paginado
        usuarios = usuarios.paginate(page=page, per_page=per_page, error_out=True)

        return jsonify({"usuarios":[usuario.to_json() for usuario in usuarios.items],    
                  'total': usuarios.total,
                  'pages': usuarios.pages,
                  'page': page      
        })


    
