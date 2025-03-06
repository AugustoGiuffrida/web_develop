from .. import db
from . import UsuarioModel


class Resena(db.Model):
    __tablename__ = 'resenas'  # Nombre de la tabla en plural

    resenaID = db.Column(db.Integer, primary_key=True)
    valoracion = db.Column(db.Integer)
    comentario = db.Column(db.String(100),)  
    usuarioID = db.Column(db.Integer, db.ForeignKey("usuarios.usuarioID"), nullable=False) #---> Clave Foranea
    libroID = db.Column(db.Integer, db.ForeignKey("libros.libroID"), nullable=False) #---> Clave Foranea
    #relacion 1:1(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="resenas")
    #relacion 1:N(Libro es padre)
    libro = db.relationship("Libro", back_populates="resenas")
    #libro = db.relationship("Libro", back_populates="resenas", uselist=False, single_parent=True)

    __table_args__ = (
        db.UniqueConstraint('usuarioID', 'libroID', name='unique_user_book_comment'),
    ) #no puede existir más de una reseña para un mismo libro hecha por un mismo usuario

    def __repr__(self):
        return '<Resena: %r >' % self.resenaID


    def to_json(self):
        usuario = db.session.query(UsuarioModel).get_or_404(self.usuarioID)
        Resena_json = {
            "resenaID": self.resenaID,
            "valoracion": self.valoracion,
            "comentario": self.comentario,
            "usuario": usuario.to_json_short(),
        }
        return Resena_json

    def to_json_complete(self):
        usuario_info = self.usuario.to_json_short()
        libro_info = self.libro.to_json_short()
        Resena_json = {
            "resenaID": self.resenaID,
            "valoracion": self.valoracion,
            "comentario": self.comentario,
            "usuario": usuario_info,
            "libro": libro_info,
        }
        return Resena_json

    # Convertir objeto en JSON corto
    def to_json_short(self):
        Resena_json = {
            "resenaID": self.resenaID,
            "valoracion": self.valoracion,
        }
        return Resena_json

    # Convertir JSON a objeto
    @staticmethod
    def from_json(resena_json):
        resenaID = resena_json.get('resenaID')
        usuarioID = resena_json.get('usuarioID')
        libroID = resena_json.get('libroID')
        valoracion = resena_json.get('valoracion')
        comentario = resena_json.get('comentario')
        return Resena(resenaID=resenaID,
                      usuarioID=usuarioID,
                      libroID=libroID,
                      valoracion=valoracion,
                      comentario=comentario)