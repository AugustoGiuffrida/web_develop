from .. import db
from datetime import datetime

   
class Libro(db.Model):

    __tablename__ = 'libros'  # Nombre de la tabla en plural

    libroID = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    editorial = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=False)
    #relacion 1:M(1 Libro M copias)
    copias =  db.relationship('LibrosCopias', back_populates='libro', cascade='all, delete-orphan')
    #relacion 1:N(Libro es padre)
    resenas =  db.relationship('Resena', back_populates='libro', cascade='all, delete-orphan')
    #relacion N:M(Libro es padre)
    #autores = db.relationship("Autor", secondary="libros_autores", back_populates="libros")


    @property
    def cantidad(self):
        return len(self.copias)

    @property
    def estado(self):
        for copia in self.copias:
            if copia.estado:
                return 'No disponible'  
        return 'Disponible'
   

    @property
    def rating(self):
        if not self.resenas:
            return 0
        total_rating = 0
        for resena in self.resenas:
            total_rating += resena.valoracion
        return round(total_rating / len(self.resenas),1)

    @property
    def copias_disponibles(self):
        return [copia.to_json_book() for copia in self.copias if copia.estado == 'Disponible']


    def __repr__(self):
        return '<Libro: %r  >' % (self.libroID)

    # Convertir objeto en JSON
    def to_json(self):
        Libro_json = {
            "libroID": self.libroID,
            'titulo': self.titulo,
            "cantidad": self.cantidad,
            'editorial': self.editorial,
            'genero': self.genero,
            "image": self.image,
            "rating": self.rating
        }
        return Libro_json

    # Convertir objeto en JSON completo con lista de prestamos y resenas
    def to_json_complete(self):
        autores = [autor.to_json() for autor in self.autores]
        resenas = [resena.to_json() for resena in self.resenas]

        Libro_json = {
            "libroID": self.libroID,
            'titulo': self.titulo,
            "cantidad": self.cantidad,
            'editorial': self.editorial,
            'genero': self.genero,
            "image": self.image,
            "autores": autores,
            "resenas": resenas,
            "rating": self.rating,
            "copias_disponibles": self.copias_disponibles
        }
        return Libro_json  

    # Convertir objeto en JSON corto
    def to_json_short(self):
        Libro_json = {
            "libroID": self.libroID,
            "titulo": self.titulo,
            "image": self.image
        }
        return Libro_json

    # Convertir JSON a objeto
    @staticmethod
    def from_json(libro_json):
        titulo = libro_json.get('titulo')
        editorial = libro_json.get('editorial')
        genero = libro_json.get('genero')
        image = libro_json.get('image')
        return Libro(
                    titulo=titulo,
                    editorial=editorial,
                    genero=genero,
                    image=image
                    )
