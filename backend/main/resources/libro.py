from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import LibroModel, AutorModel, PrestamoModel, ResenaModel
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
    def get(self):
        # Página inicial por defecto
        page = 1
        per_page = 9
        
        libros = db.session.query(LibroModel)

        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))
        params = request.args

        ### FILTROS ### 

        # Filtrar por titulo
        if request.args.get('titulo'):
            libros = libros.filter(LibroModel.titulo.like('%' + request.args.get('titulo') + '%'))

        # Traemos todos los libros sin paginación para ordenarlos después
        libros = libros.all()

        # Si hay un parámetro para ordenar por rating
        if request.args.get('sortby_rating'):
            sort_order = request.args.get('sortby_rating')
            
            # Ordenar los libros en memoria según su rating (si rating es un decorador, 
            # asegúrate de que este decorador esté accediendo al valor correcto del rating)
            if sort_order == "asc":
                libros = sorted(libros, key=lambda libro: libro.rating)  # Ordenar ascendente
            elif sort_order == "desc":
                libros = sorted(libros, key=lambda libro: libro.rating, reverse=True)  # Ordenar descendente

        # Paginación manual de los libros después de ordenarlos
        start = (page - 1) * per_page
        end = start + per_page
        paginated_libros = libros[start:end]

        # Devolver los libros paginados
        return jsonify({
            'libros': [libro.to_json_complete() for libro in paginated_libros],
            'total': len(libros),  # Total de libros sin paginación
            'pages': (len(libros) + per_page - 1) // per_page,  # Cálculo de número total de páginas
            'page': page
        })


        # # Filtro y ordenación por rating
        # if request.args.get('sortby_rating'):
        #     sort_order = request.args.get('sortby_rating')
            
        #     # Subconsulta para obtener el rating
        #     rating_subquery = db.session.query(
        #         LibroModel.libroID,
        #         func.avg(ResenaModel.valoracion).label('avg_rating')
        #     ).join(ResenaModel).group_by(LibroModel.libroID).subquery()
            
        #     libros = libros.join(rating_subquery, LibroModel.libroID == rating_subquery.c.libroID)
            
        #     # Ordenar según la valoración
        #     if sort_order == "desc":
        #         libros = libros.order_by(rating_subquery.c.avg_rating.desc())
        #     elif sort_order == "asc":
        #         libros = libros.order_by(rating_subquery.c.avg_rating.asc())

        # # Paginar los libros
        # libros = libros.paginate(page=page, per_page=per_page, error_out=True)

        # return jsonify({
        #     'libros': [libro.to_json_complete() for libro in libros.items],
        #     'total': libros.total,
        #     'pages': libros.pages,
        #     'page': page
        # })


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