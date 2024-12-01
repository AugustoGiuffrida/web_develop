from .. import db

libros_autores = db.Table("libros_autores",
    db.Column("libroID",db.Integer,db.ForeignKey("libros.libroID")),
    db.Column("autorID",db.Integer,db.ForeignKey("autores.autorID")),
    )  

class Autor(db.Model):
    __tablename__ = 'autores'  # Nombre de la tabla en plural
    
    autorID = db.Column(db.Integer, primary_key=True)
    autor_nombre = db.Column(db.String(100), nullable=False)
    autor_apellido = db.Column(db.String(100), nullable=False)
    # Nombre de la relación
    #relacion N:M(Libro es padre)
    libros = db.relationship("Libro", secondary=libros_autores, backref=db.backref('autores', lazy='dynamic'))

    def __repr__(self):
        return '<Autor: %r >' % self.autor_nombre

    def to_json(self):
        autor_json = {
            "autorID": self.autorID,
            "autor_nombre": self.autor_nombre,
            "autor_apellido": self.autor_apellido,
        }
        return autor_json

    def to_json_complete(self):
        libros = [libro.to_json_short() for libro in self.libros]
        autor_json = {
            "autorID": self.autorID,
            "autor_nombre": self.autor_nombre,
            "autor_apellido": self.autor_apellido,
            "libros": libros
        }
        return autor_json


    def to_json_short(self):
        autor_json = {
            "autorID": self.autorID,
            "autor_nombre": self.autor_nombre,
            "autor_apellido": self.autor_apellido
        }
        return autor_json

    @staticmethod
    # Convertir JSON a objeto
    def from_json(autor_json):
        autorID = autor_json.get('autorID')
        autor_nombre = autor_json.get('autor_nombre')
        autor_apellido = autor_json.get('autor_apellido')
        return Autor(autorID=autorID,
                    autor_nombre=autor_nombre, 
                    autor_apellido=autor_apellido
                    )