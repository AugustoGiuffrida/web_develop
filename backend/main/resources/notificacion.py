from flask_restful import Resource
from flask import request
from .. import db
from main.models import NotificacionModel, UsuarioModel
from flask import jsonify



NOTIFICACION = {
    1: {'nombre':'libro_nuevo','Descripcion':'Salio un libro nuevo'}
    
}

class Notificaciones(Resource):
    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 10
        
        # Obtener todas las notificaciones
        notificaciones = db.session.query(NotificacionModel)

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

    def post(self):
        data = request.get_json()
        notificacion = NotificacionModel.from_json(data) #notificacion = notificacion.from_json(request.get_json()

        try:
            db.session.add(notificacion)
            db.session.commit()
        except: # captura cualquier excepción que ocurra durante la ejecución del código en el bloque try,
            db.session.rollback()  #realiza un rollback de la sesión y luego devuelve el mensaje de error junto con el código de estado 400.      
            return {"message": "Error al agregar la notificacion"}, 400 # Esto garantiza que cualquier cambio no se guarde en la base de datos si ocurre un error.
        return notificacion.to_json(), 201
        
        

#Cuando ocurre una excepción durante la ejecución del código dentro de un bloque try, 
#es una buena práctica realizar un rollback de la sesión de la base de datos para 
#deshacer cualquiercambio realizado desde el inicio de la transacción actual.
#Esto asegura que la base de datos no quede en un estado inconsistente.

#rollback() se llama para deshacer cualquier cambio realizado en la sesión de la base de datos. 
#Esto asegura que la base de datos mantenga su integridad en caso de error.

        #notificacion = request.get_json()
        #id = int(max(NOTIFICACION.keys()))+1
        #NOTIFICACION[id] = notificacion
        #return NOTIFICACION[id], 201 