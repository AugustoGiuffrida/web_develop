from .. import db

notificaciones_usuarios = db.Table("notificaciones_usuarios",
    db.Column("notificacionID",db.Integer,db.ForeignKey("notificaciones.notificacionID"),primary_key=True),
    db.Column("usuarioID",db.Integer,db.ForeignKey("usuarios.usuarioID"),primary_key=True)
    )

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'  # Nombre de la tabla en plural
    
    notificacionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentario = db.Column(db.String(100), nullable=False)
    usuarioID = db.Column(db.Integer, db.ForeignKey("usuarios.usuarioID"), nullable=False)##---->Clave Foranea
    #relacion 1:N(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="notificaciones")
 

    def __repr__(self):
        return '<Notificacion: %r >' % self.notificacionID

    def to_json(self):
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "comentario":str(self.comentario),
        }
        return Notificacion_json

    def to_json_complete(self):
        usuarios_info = [usuario.to_json() for usuario in self.usuarios]
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "comentario":str(self.comentario),
            "usuarioID": self.usuarioID,
            'usuarios': usuarios_info
        }
        return Notificacion_json

    def to_json_short(self):
        Notificacion_json = {
            "notificacionID": self.notificacionID,
        }
        return Notificacion_json

    @staticmethod
    def from_json(notificacion_json):
        notificacionID = notificacion_json.get('notificacionID')
        usuarioID = notificacion_json.get('usuarioID')
        comentario = notificacion_json.get('comentario')
        return Notificacion(notificacionID=notificacionID,
                            usuarioID=usuarioID, 
                            comentario=comentario)