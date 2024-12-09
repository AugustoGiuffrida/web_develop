from flask_restful import Resource
from flask import request
from .. import db
from main.models import PrestamoModel, LibrosCopiasModel, UsuarioModel
from flask import jsonify
from sqlalchemy import cast, Date
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required
from datetime import datetime


class Prestamo(Resource):

    @jwt_required()
    @role_required(roles=["admin", "librarian"])
    def get(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        return prestamo.to_json_complete()

    @jwt_required()
    @role_required(roles=["admin", "librarian"])
    def delete(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        try:
            db.session.delete(prestamo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el prestamo"}, 400
        return {"message": "Eliminado correctamente"}, 200


    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def put(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        data = request.get_json()

        try:
            if data.get('fecha_entrega'):
                # Convertir a objeto datetime.date
                prestamo.fecha_entrega = datetime.strptime(data.get('fecha_entrega'), '%Y-%m-%d').date()
            if data.get('fecha_devolucion'):
                # Convertir a objeto datetime.date
                prestamo.fecha_devolucion = datetime.strptime(data.get('fecha_devolucion'), '%Y-%m-%d').date()

            db.session.add(prestamo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el préstamo", "error": str(e)}, 400

        return prestamo.to_json_complete(), 200


class Prestamos(Resource):

    @jwt_required()
    @role_required(roles=['admin', 'librarian', 'user'])
    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 8
        
        #no ejecuto el .all()
        prestamos = db.session.query(PrestamoModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        ### FILTROS ###

        # Filtrar por fecha de entrega
        if fecha_entrega := request.args.get('fecha_entrega'):
            try:
                fecha_entrega = datetime.strptime(fecha_entrega, "%Y-%m-%d").date()
                prestamos = prestamos.filter(PrestamoModel.fecha_entrega == fecha_entrega)
            except ValueError:
                return {"message": "Formato de fecha incorrecto. Use 'YYYY-MM-DD'."}, 400

        # Filtrar por fecha de devolución
        if fecha_devolucion := request.args.get('fecha_devolucion'):
            try:
                fecha_devolucion = datetime.strptime(fecha_devolucion, "%Y-%m-%d").date()
                prestamos = prestamos.filter(PrestamoModel.fecha_devolucion == fecha_devolucion)
            except ValueError:
                return {"message": "Formato de fecha incorrecto. Use 'YYYY-MM-DD'."}, 400


        #Filtrar por Id de libro
        if request.args.get('copiaID'):
            prestamos = prestamos.filter(PrestamoModel.copiaID == request.args.get('copiaID'))
        
        #Filtrar por Id de usuario
        if request.args.get('usuarioID'):
            prestamos = prestamos.filter(PrestamoModel.usuarioID == request.args.get('usuarioID'))
        ### FIN FILTROS ####     
          
        #Obtener valor paginado
        prestamos = prestamos.paginate(page=page, per_page=per_page, error_out=True)

        return jsonify({"prestamos":[prestamo.to_json_complete() for prestamo in prestamos],    
                  'total': prestamos.total,
                  'pages': prestamos.pages,
                  'page': page      
        })

    @jwt_required()
    @role_required(roles=['admin', 'librarian', 'user'])
    def post(self):
        data = request.get_json()
        db.session.query(LibrosCopiasModel).get_or_404(data.get('copiaID'))
        db.session.query(UsuarioModel).get_or_404(data.get('usuarioID'))
        prestamo = PrestamoModel.from_json(data)
        try:
            db.session.add(prestamo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al agregar el prestamo", "error": str(e)}, 400         
        return prestamo.to_json(), 201

    

