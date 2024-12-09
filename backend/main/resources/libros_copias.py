from main.models import LibrosCopiasModel, LibroModel
from main.auth.decorators import role_required
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request, jsonify
from .. import db


class LibroCopia(Resource):
    def get(self, id):
        libro_copia = db.session.query(LibrosCopiasModel).get_or_404(id)
        return libro_copia.to_json()

    def delete(self, id):
        libro_copia = db.session.query(LibrosCopiasModel).get_or_404(id)
        try:
            db.session.delete(libro_copia)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al borrar la copia del libro"}, 400
        return {"message": "Eliminado correctamente", "copia": libro_copia.to_json()}, 200


class LibrosCopias(Resource):
    
    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def get(self):
        page = 1

        per_page = 10

        libros_copias = db.session.query(LibrosCopiasModel)

        if 'page' in request.args:
            page = int(request.args['page'])
        if 'per_page' in request.args:
            per_page = int(request.args['per_page'])

        libroID = request.args.get('libroID')  
        if libroID:
            libros_copias = libros_copias.filter(LibrosCopiasModel.libroID == libroID) 

        estado = request.args.get('estado')
        if estado:
            libros_copias = libros_copias.filter(LibrosCopiasModel.estado == estado)     

        libros_copias = libros_copias.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({'libros_copias': [libro_copia.to_json() for libro_copia in libros_copias.items],
            'total': libros_copias.total,
            'pages': libros_copias.pages,
            'page': libros_copias.page
        })

    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def post(self):
        data = request.get_json()
        libroID = data.get('libroID') #Id del libro al que se le va a agregar la copia
        db.session.query(LibroModel).get_or_404(libroID)
        cantidad = data.get('cantidad',1) #Cantidad de copias que se van a agregar, por defecto es 1
        if not isinstance(cantidad, int) or cantidad <= 0:
            return {"message": "La cantidad de copias debe ser un entero positivo"}, 400
        
        libros_copias = [LibrosCopiasModel.from_json({'libroID': libroID}) for _ in range(cantidad)]
        try:
            db.session.add_all(libros_copias)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar las copias del libro"}, 400
        return {"message": f"Copias {cantidad} agregadas correctamente"}, 201

        