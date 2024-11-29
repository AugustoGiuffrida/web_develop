from flask_restful import Resource
from flask import request
from .. import db
from main.models import PrestamoModel
from flask import jsonify
from datetime import datetime


PRESTAMOS = {
    1: {'fecha_alquilado':'20/03/2024', 'fecha_limite':'30/03/2024'},
    2: {'fecha_alquilado':'10/4/2024', 'fecha_limite':'20/04/2024'}
}

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
        if request.args.get('fecha_entrega'):#verifica si el parámetro está en los argumentos de la solicitud
            try:
                fecha_entrega = datetime.strptime(request.args.get('fecha_entrega'), "%Y-%m-%d") #convertir el texto que representa la fecha alquilado en un objeto datetime. 
                prestamos = prestamos.filter(PrestamoModel.fecha_entrega == fecha_entrega) #selecciona los préstamos cuya fecha alquilado coincida con la fecha ingresada.
            except:# error al intentar convertir la cadena en un objeto datetime
                return "Formato de fecha incorrecto. Utilice el formato 'yyyy-mm-dd'.", 400 #se devuelve un mensaje de error pidiendo el formato correcto. 
           
        # Filtrar por fecha límite
        if request.args.get('fecha_devolucion'):
            try:
                fecha_devolucion = datetime.strptime(request.args.get('fecha_devolucion'), "%Y-%m-%d")
                prestamos = prestamos.filter(PrestamoModel.fecha_devolucion == fecha_devolucion)
            except:
                return "Formato de fecha incorrecto. Utilice el formato 'yyyy-mm-dd'.", 400

        #Filtrar por Id de libro
        if request.args.get('libroID'):
            prestamos = prestamos.filter(PrestamoModel.libroID == request.args.get('libroID'))
        
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

