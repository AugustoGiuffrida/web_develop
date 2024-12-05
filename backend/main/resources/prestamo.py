from flask_restful import Resource
from flask import request
from .. import db
from main.models import PrestamoModel
from flask import jsonify
from sqlalchemy import cast, Date
from datetime import datetime


class Prestamos(Resource):

    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 9
        
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

    #insertar recurso
    def post(self):
        prestamo = PrestamoModel.from_json(request.get_json())
        try:
            db.session.add(prestamo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al agregar el prestamo"}, 400         
        return prestamo.to_json(), 201

    
class Prestamo(Resource):

    def get(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        return prestamo.to_json_complete()

    def delete(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        try:
            db.session.delete(prestamo)
            db.session.commit()
            return {"message": "Eliminado correctamente"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el prestamo"}, 400

   
    def put(self, id):
            prestamo = db.session.query(PrestamoModel).get_or_404(id)
            data = request.get_json()
            for key, value in data.items():
                if key in ['fecha_entrega', 'fecha_devolucion']:
                    try:
                        value = datetime.strptime(value, '%Y-%m-%d')  # Convertir la cadena en objeto datetime
                    except ValueError:
                        return {"message": "Formato incorrecto de fecha {key}, debe ser YYYY-MM-DD"}, 400      
                setattr(prestamo, key, value)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {"message": "Error al actualizar el préstamo"}, 400
            return prestamo.to_json_complete(), 200

