from .. import db


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
        return f'{self.notificacionID} {self.titulo} {self.descripcion} {self.categoria}'

    def to_json(self):
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "titulo":str(self.titulo),
            "descripcion":str(self.descripcion),
            "vista":self.vista,
            "categoria":self.categoria,
            "usuarioID": self.usuarioID
        }
        return Notificacion_json

    def to_json_complete(self):
        usuario = self.usuario.to_json_short()
        Notificacion_json = {
            "notificacionID": self.notificacionID,
            "titulo":str(self.titulo),
            "descripcion":str(self.descripcion),
            "vista":self.vista,
            "categoria":self.categoria,
            "usuarioID": self.usuarioID,
            'usuarios': usuario
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
        titulo = notificacion_json.get('titulo')
        usuarioID = notificacion_json.get('usuarioID')
        descripcion = notificacion_json.get('descripcion')
        vista = notificacion_json.get('vista')
        categoria = notificacion_json.get('categoria')

        try:
            # Validaciones específicas
            if titulo is None or titulo.strip() == "":
                raise ValueError("El campo 'titulo' es obligatorio y no puede estar vacío.")
            if usuarioID is None:
                raise ValueError("El campo 'usuarioID' es obligatorio.")
            if descripcion is None or descripcion.strip() == "":
                raise ValueError("El campo 'descripcion' es obligatorio y no puede estar vacío.")
            if categoria not in ["warning", "danger", "info"]:
                raise ValueError("La categoría debe ser 'warning', 'danger' o 'info'.")

            # Construcción de la instancia
            return Notificacion(
                usuarioID=usuarioID,
                titulo=titulo,
                descripcion=descripcion,
                vista=False,
                categoria=categoria
            )
        except Exception as e:
            raise e
