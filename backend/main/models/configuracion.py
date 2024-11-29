from .. import db

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'  # Nombre de la tabla en plural

    configuracionID = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    idioma = db.Column(db.String, nullable=False)
    orden = db.Column(db.String, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'))#--->Clave Foranea
    #relación 1:1(usuario-padre)
    usuario = db.relationship("Usuario", back_populates="configuraciones")
   


    def __repr__(self):
        return '<Configuracion: %r >' % self.configuracionID

    #Convertir objeto en JSON
    def to_json(self):
        Configuracion_json = {
            "configuracionID":self.configuracionID,
            'idioma': str(self.idioma),
            'orden': str(self.orden),
        }
        return Configuracion_json

    def to_json_complete(self):
        usuarios = [usuario.to_json() for usuario in self.usuarios]
        Configuracion_json = {
            "configuracionID": self.configuracionID,
            'idioma': self.idioma,
            'orden': self.orden,
            'usuarios': usuarios
        }
        return Configuracion_json

    def to_json_short(self):
        Configuracion_json = {
            "configuracionID": self.configuracionID,
            'idioma': self.idioma,
            'orden': self.orden,
        }
        return Configuracion_json

    @staticmethod
    # Convertir JSON a objeto
    def from_json(configuracion_json):
        configuracionID = configuracion_json.get("configuracionID")
        idioma = configuracion_json.get('idioma')
        orden = configuracion_json.get('orden')
        return Configuracion(configuracionID=configuracionID,
                            idioma=idioma,
                             orden=orden,)

        