from flask_restful import Resource
from flask import request, jsonify
from main.models import AutorModel  
from .. import db
from sqlalchemy import or_

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

        autores = autores.paginate(page=page, per_page=per_page, error_out=True)
        return jsonify({
            'autores': [autor.to_json() for autor in autores],
            'total': autores.total,
            'pages': autores.pages,
            'page': page
        })
    
    def post(self):
        autor = AutorModel.from_json(request.get_json())
        try:
            db.session.add(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al agregar el autor"}, 400          
        return autor.to_json(), 201

class Autor(Resource):
    def get(self, id):   
        autor = db.session.query(AutorModel).get_or_404(id)
        return autor.to_json_complete()
    
    def delete(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        try:
            db.session.delete(autor)
            db.session.commit()
            return {"message": "Autor eliminado correctamente"}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al borrar el autor"}, 400

    def put(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(autor, key, value)
        try:
            db.session.add(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el autor"}, 400
        return autor.to_json(), 200

