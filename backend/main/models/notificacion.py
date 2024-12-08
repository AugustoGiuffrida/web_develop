from .. import db

notificaciones_usuarios = db.Table("notificaciones_usuarios",
    db.Column("notificacionID",db.Integer,db.ForeignKey("notificaciones.notificacionID"),primary_key=True),
    db.Column("usuarioID",db.Integer,db.ForeignKey("usuarios.usuarioID"),primary_key=True)
    )

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'  
    
    notificacionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    vista = db.Column(db.Boolean, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    usuarioID = db.Column(db.Integer, db.ForeignKey("usuarios.usuarioID"), nullable=False)
    #relacion 1:N(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="notificaciones")
 

    def __repr__(self):
        return '<Notificacion: %r >' % self.notificacionID

    def to_json(self):
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "titulo":str(self.titulo),
            "descripcion":str(self.descripcion),
            "vista":self.vista,
            "categoria":self.categoria
        }
        return Notificacion_json

    def to_json_complete(self):
        usuarios_info = [usuario.to_json() for usuario in self.usuarios]
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "titulo":str(self.titulo),
            "descripcion":str(self.descripcion),
            "vista":self.vista,
            "categoria":self.categoria,
            "usuarioID": self.usuarioID,
            'usuarios': usuarios_info
        }
        return Notificacion_json

    def to_json_short(self):
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "titulo":str(self.titulo),
            "descripcion":str(self.descripcion),
        }
        return Notificacion_json

    @staticmethod
    def from_json(notificacion_json):
        notificacionID = notificacion_json.get('notificacionID')
        usuarioID = notificacion_json.get('usuarioID')
        descripcion = notificacion_json.get('descripcion')
        vista = notificacion_json.get('vista')
        categoria = notificacion_json.get('categoria')
        try:
            if not notificacionID or not usuarioID or not descripcion or not vista or not categoria:
                raise ValueError("Todos los campos son obligatorios")

            if categoria not in ["warning", "danger", "info"]:
                raise ValueError("La categoria solo puede ser 'warning', 'danger' o 'info'")

            return Notificacion(notificacionID=notificacionID,
                                    usuarioID=usuarioID, 
                                    descripcion=descripcion,
                                    vista=vista,
                                    categoria=categoria
                                    ) 
        except Exception as e:
            raise e