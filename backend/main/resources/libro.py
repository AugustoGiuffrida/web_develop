from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import LibroModel, AutorModel, PrestamoModel
from sqlalchemy import func, desc, asc
from main.auth.decorators import role_required
from flask_jwt_extended import jwt_required

class Libro(Resource): 
      
    def get(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        return libro.to_json_complete()

    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def delete(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        try:
            db.session.delete(libro)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al borrar el libro", "error": str(e)}, 400
        return {"message": "Libro eliminado correctamente", "libro": libro.to_json()}, 201

    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def put(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        data = request.get_json()                
        autores_ids = data.get('autores')

        if data.get('titulo'):
            libro.titulo = data.get('titulo')
        if data.get('editorial'):
            libro.editorial = data.get('editorial')
        if data.get('genero'):
            libro.genero = data.get('genero')
        if data.get('image'):
            libro.image = data.get('image')
        if autores_ids:
            autores = AutorModel.query.filter(AutorModel.autorID.in_(autores_ids)).all()
            libro.autores = autores

        try:
            db.session.add(libro)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message": "Error al agregar el libro"}, 400
        return libro.to_json(), 201


class Libros(Resource): 
    #obtener lista de los libros
    def get(self):
        #Página inicial por defecto
        page = 1
        #Cantidad de elementos por página por defecto
        per_page = 9
        
        libros = db.session.query(LibroModel)


        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))
        params = request.args

        ### FILTROS ### 

        #Filtrar por titulo
        if request.args.get('titulo'):
            libros = libros.filter(LibroModel.titulo.like('%' + request.args.get('titulo') + '%'))
        if 'sortby_titulo' in params:
            # Ordenar por título de forma descendente
            libros = libros.order_by(LibroModel.titulo.desc())

        #Filtrar por editorial
        if request.args.get('editorial'):
            libros = libros.filter(LibroModel.editorial == request.args.get('editorial'))
        if 'sortby_editorial' in params:
            libros = libros.order_by(LibroModel.editorial.desc())

        #Filtrar por id
        if request.args.get('id'):
            libros = libros.filter(LibroModel.libroID.like('%' + request.args.get('id') + '%'))
        
        #Sortby_prestamos
        if request.args.get('sortby_prestamos'):
            if request.args.get('sortby_prestamos') == "asc":
                libros=libros.outerjoin(LibroModel.prestamos).group_by(LibroModel.libroID).order_by(func.count(PrestamoModel.prestamoID).asc())
            if request.args.get('sortby_prestamos') == "desc":
                libros=libros.outerjoin(LibroModel.prestamos).group_by(LibroModel.libroID).order_by(func.count(PrestamoModel.prestamoID).desc())  
        ### FIN FILTROS ####     
          
        #Obtener valor paginado(evita que se traigan todos los registros)
        libros = libros.paginate(page=page, per_page=per_page, error_out=True)
                                                                #Si no existe la pag
                                                                #devuelve un error

        return jsonify({'libros': [libro.to_json_complete() for libro in libros],
                  'total': libros.total, #
                  'pages': libros.pages, # Esto se tiene que enviar al backend para paginar
                  'page': page           #
                })

    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def post(self):
        data = request.get_json()
        autores_ids = data.get('autores', [])  # Obtener los IDs de los autores del JSON o una lista vacía si no se proporcionan
        libro = LibroModel.from_json(data)

        if autores_ids:
            # Obtener las instancias de autores basadas en las IDs recibidas
            autores = AutorModel.query.filter(AutorModel.autorID.in_(autores_ids)).all()
            # Agregar las instancias de autor a la lista de autores del libro
            libro.autores.extend(autores)
        try:
            db.session.add(libro)
            db.session.commit()
        except:
            db.session.rollback()
            return {"message":"Error al agregar el libro", "libro": libro.to_json()}, 400
        return libro.to_json(), 201 #Si la operación es exitosa, se devuelve la representación JSON del libro con el código de estado 201.