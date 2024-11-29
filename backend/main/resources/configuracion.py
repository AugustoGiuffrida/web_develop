from flask_restful import Resource
from flask import request
from .. import db
from main.models import ConfiguracionModel
from flask import jsonify

CONFIGURACION = {
    1: {'modos oscuro':'si','idioma':'ingles'}
    
}

class Configuraciones(Resource):

    def get(self):
        configuraciones = db.session.query(ConfiguracionModel).all()
        return jsonify([configuracion.to_json() for configuracion in configuraciones])

    #insertar recurso
    def post(self):
        configuracion = ConfiguracionModel.from_json(request.get_json())
        try:
            db.session.add(configuracion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error a agregar la configuración"}, 400
        return configuracion.to_json(), 201
 



        #except:
            #return "Formato incorrecto", 400            
        
        