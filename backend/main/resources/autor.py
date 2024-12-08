from flask_restful import Resource
from flask import request, jsonify
from main.models import AutorModel  
from .. import db
from sqlalchemy import or_
from main.auth.decorators import role_required
from flask_jwt_extended import jwt_required

class Autor(Resource):
    def get(self, id):   
        autor = db.session.query(AutorModel).get_or_404(id)
        return autor.to_json_complete()
    
    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def put(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        data = request.get_json().items()

        if data.get('autor_nombre'):
            autor.autor_nombre = data.get('autor_nombre')
        if data.get('autor_apellido'):
            autor.autor_apellido = data.get('autor_apellido')
        try:
            db.session.add(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el autor"}, 400
        return autor.to_json(), 200

    @jwt_required()
    @role_required(roles=["admin", "librarian"]) 
    def delete(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        try:
            db.session.delete(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al borrar el autor"}, 400
        return {"message": "Autor eliminado correctamente", "autor": autor.to_json()}, 204



class Autores(Resource):
    def get(self):
        page = 1
        per_page = 5

        autores = db.session.query(AutorModel)

        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        ### FILTROS ###
        nombre_filter = request.args.get('nombre')
        if nombre_filter:
            autores=autores.filter(AutorModel.autor_nombre.like('%'+nombre_filter+'%'))
        
        apellido_filter = request.args.get('apellido')
        if apellido_filter:
            autores=autores.filter(AutorModel.autor_apellido.like('%'+apellido_filter+'%'))

        nombre_o_apellido = request.args.get('nombre_o_apellido')
        if nombre_o_apellido:
            autores = autores.filter(
                or_(
                    AutorModel.autor_nombre.like(f'%{nombre_o_apellido}%'),
                    AutorModel.autor_apellido.like(f'%{nombre_o_apellido}%')
                )
            )

        fullname = request.args.get('fullname')
        if fullname:
            nombre = fullname.split(' ')[0]
            apellido = fullname.split(' ')[1]
            autores = autores.filter(
                and_(
                    AutorModel.autor_nombre == nombre,
                    AutorModel.autor_apellido == apellido
                )
            )

        autores = autores.paginate(page=page, per_page=per_page, error_out=True)
        return jsonify({
            'autores': [autor.to_json() for autor in autores],
            'total': autores.total,
            'pages': autores.pages,
            'page': page
        })
    
    @jwt_required()
    @role_required(roles=['admin', 'librarian'])
    def post(self):
        autor = AutorModel.from_json(request.get_json())
        try:
            db.session.add(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al agregar el autor"}, 400          
        return autor.to_json(), 201



