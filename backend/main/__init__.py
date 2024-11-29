from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail

api=Api() #Iniciar Api de flask_restful
db=SQLAlchemy() #Iniciar SQLAlchemy

#Inicializar Migrate
migrate = Migrate()

#Inicializar JWT
jwt = JWTManager()

#Inicializar
mailsender = Mail()

def create_app():
    app = Flask(__name__)
    load_dotenv() #Se cargan variables del archivo .env
    

    #if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')): ## LINUX
        #os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))           ##


    # Configuración de SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                                                    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getenv('DATABASE_PATH'), os.getenv('DATABASE_NAME'))
    db.init_app(app)

    with app.app_context():  # Entrar en el contexto de la aplicación Flask                           ##
        # Crear la base de datos si no existe (Solo válido si se utiliza SQLite)                      ##WINDOWS
        if not os.path.exists(os.path.join(os.getenv('DATABASE_PATH'), os.getenv('DATABASE_NAME'))):  ##
            db.create_all()

    import main.resources as resources
    # Registrar Blueprints y recursos
    import main.auth  as auth_blueprint

    api.add_resource(resources.UsuariosResources, '/usuarios')
    api.add_resource(resources.UsuarioResources, '/usuario/<id>')

    api.add_resource(resources.LibrosResources, '/libros')
    api.add_resource(resources.LibroResources, '/libro/<id>')

    api.add_resource(resources.PrestamosResources, '/prestamos')
    api.add_resource(resources.PrestamoResources, '/prestamo/<id>')

    api.add_resource(resources.NotificacionesResources, '/notificaciones')

    api.add_resource(resources.ConfiguracionesResources, '/configuraciones')

    api.add_resource(resources.ReseñasResources, '/reseñas')
    api.add_resource(resources.ReseñaResources, '/reseña/<id>')

    api.add_resource(resources.AutoresResources, '/autores')
    api.add_resource(resources.AutorResources, '/autor/<id>')

    api.init_app(app)
    
#Cargar clave secreta
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    #Cargar tiempo de expiración de los tokens
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    from main.auth import routes
    #Importar blueprint
    app.register_blueprint(routes.auth) ##Forma de organizar una aplicacion web con modulos en flask

    #Configuración de mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar en app
    mailsender.init_app(app)

    return app