from .. import db

class Reseña(db.Model):
    __tablename__ = 'reseñas'  # Nombre de la tabla en plural

    reseñaID = db.Column(db.Integer, primary_key=True)
    valoracion = db.Column(db.Integer)
    comentario = db.Column(db.String(100),)  
    usuarioID = db.Column(db.Integer, db.ForeignKey("usuarios.usuarioID"), nullable=False) #---> Clave Foranea
    libroID = db.Column(db.Integer, db.ForeignKey("libros.libroID"), nullable=False) #---> Clave Foranea
    #relacion 1:1(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="reseñas")
    #relacion 1:N(Libro es padre)
    libro = db.relationship("Libro", back_populates="reseñas")
    #libro = db.relationship("Libro", back_populates="reseñas", uselist=False, single_parent=True)

    def __repr__(self):
        return '<Reseña: %r >' % self.reseñaID

    def to_json(self):
        Reseña_json = {
            "resenaID": self.reseñaID,
            "valoracion": self.valoracion,
            "comentario": self.comentario,
            "usuarioID": self.usuarioID,
        }
        return Reseña_json

    def to_json_complete(self):
        usuario_info = self.usuario.to_json_short()
        libro_info = self.libro.to_json_short()
        Reseña_json = {
            "reseñaID": self.reseñaID,
            "valoracion": self.valoracion,
            "comentario": self.comentario,
            "usuario": usuario_info,
            "libro": libro_info,
        }
        return Reseña_json

    # Convertir objeto en JSON corto
    def to_json_short(self):
        Reseña_json = {
            "reseñaID": self.reseñaID,
            "valoracion": self.valoracion,
        }
        return Reseña_json

    # Convertir JSON a objeto
    @staticmethod
    def from_json(reseña_json):
        reseñaID = reseña_json.get('reseñaID')
        usuarioID = reseña_json.get('usuarioID')
        libroID = reseña_json.get('libroID')
        valoracion = reseña_json.get('valoracion')
        comentario = reseña_json.get('comentario')
        return Reseña(reseñaID=reseñaID,
                      usuarioID=usuarioID,
                      libroID=libroID,
                      valoracion=valoracion,
                      comentario=comentario)