from flask import request, jsonify, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.mail.functions import sendMail
#Blueprint para acceder a los métodos de autenticación
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Método de logueo
@auth.route('/login', methods=['POST'])
def login():
    #Busca al usuario en la db por mail
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.usuario_email == request.get_json().get("usuario_email")).first_or_404()
    #Valida la contrasena
    if usuario.validate_pass(request.get_json().get("usuario_contrasena")):
        #Genera un nuevo token
        #Pasa el objeto usuario como identidad
        print(usuario)
        access_token = create_access_token(identity=usuario)
        #Devolver valores y token
        data = {
            'usuarioID': str(usuario.usuarioID),
            'usuario_email': usuario.usuario_email,
            'access_token': access_token
        }

        return data, 200
    else:
        return 'Incorrect password', 401

#Método de registro
@auth.route('/register', methods=['POST'])
def register():
    # Get the JSON data and create the user object
    usuario_data = request.get_json()
    usuario = UsuarioModel.from_json(usuario_data)
    
    # Log the incoming email for debugging
    print(f"Attempting to register email: {usuario.usuario_email}")
    
    # Check if the email already exists in the DB
    exists = db.session.query(UsuarioModel).filter(db.func.lower(UsuarioModel.usuario_email) == usuario.usuario_email.lower()).scalar() is not None
    print(f"Email exists: {exists}")
    
    if exists:
        return jsonify({'error': 'Duplicated email'}), 409
    
    try:
        # Add user to DB
        db.session.add(usuario)
        db.session.commit()
        send = sendMail([usuario.usuario_email], "Welcome!", 'register', usuario=usuario)
    except Exception as error:
        db.session.rollback()
        print(f"Error during registration: {str(error)}")
        return jsonify({'error': str(error)}), 500
    
    return usuario.to_json(), 201
