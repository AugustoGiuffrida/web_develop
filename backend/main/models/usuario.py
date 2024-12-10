from .. import db
#Importamos de python 2 funciones
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en plural
    
    usuarioID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_nombre = db.Column(db.String(100), nullable=False)
    usuario_apellido = db.Column(db.String(100), nullable=False)
    usuario_contrasena = db.Column(db.String(100), nullable=False)
    usuario_email = db.Column(db.String(100), nullable=False, unique=True)
    usuario_telefono = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.String(10), nullable=False, server_default="pending")

    # Relaciones con otros modelos
    resenas = db.relationship("Resena", uselist=False, back_populates="usuario", cascade="all, delete-orphan") 
    notificaciones = db.relationship("Notificacion", back_populates="usuario",cascade="all, delete-orphan")
    prestamos = db.relationship("Prestamo", uselist=False, back_populates="usuario", cascade="all, delete-orphan")

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')
    
    @plain_password.setter
    def plain_password(self, password):
        self.usuario_contrasena = generate_password_hash(password)
    
    def validate_pass(self, password):
        return check_password_hash(self.usuario_contrasena, password)

    def __repr__(self):
        return '<Usuario: %r %r %r >' % (self.usuarioID, self.usuario_nombre, self.usuario_contrasena)

    def to_json(self):
        usuario_json = {
            "usuarioID": self.usuarioID,
            "usuario_nombre": self.usuario_nombre,
            "usuario_apellido": self.usuario_apellido,
            "usuario_email": self.usuario_email,
            "usuario_telefono": self.usuario_telefono,
            "rol": self.rol
        }
        return usuario_json


    def to_json_complete(self):
        notificaciones_info = [notificacion.to_json() for notificacion in self.notificaciones]
        try:
            resena = self.resenas.to_json_short()
        except:
            resena = ""
        try:
            prestamo = self.prestamos.to_json_short()
        except:
            prestamo = ""
        Usuario_json = {
            "usuarioID": self.usuarioID,
            "usuario_nombre": self.usuario_nombre,
            "usuario_apellido": self.usuario_apellido,
            "usuario_email": self.usuario_email,
            "usuario_telefono": self.usuario_telefono,
            "rol": self.rol, 
            "resena": resena,
            "notificaciones": notificaciones_info,
            'prestamo': prestamo
        }
        return Usuario_json

    def to_json_short(self):
        Usuario_json = {
            "usuarioID": self.usuarioID,
            "usuario_nombre": self.usuario_nombre,
            "usuario_apellido": self.usuario_apellido,
            "usuario_email": self.usuario_email,
            "rol": self.rol  
        }
        return Usuario_json

    @staticmethod
    def from_json(usuario_json):
        usuario_nombre = usuario_json.get('usuario_nombre')
        usuario_apellido = usuario_json.get('usuario_apellido')
        usuario_contrasena = usuario_json.get('usuario_contrasena')
        usuario_email = usuario_json.get('usuario_email')
        usuario_telefono = usuario_json.get('usuario_telefono')
        rol = usuario_json.get('rol')
        return Usuario(usuario_nombre=usuario_nombre,
                        usuario_apellido=usuario_apellido,
                        plain_password=usuario_contrasena,
                        usuario_email=usuario_email,
                        usuario_telefono=usuario_telefono,
                        rol=rol
                       )
