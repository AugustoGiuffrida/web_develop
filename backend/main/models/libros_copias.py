from .. import db

class LibrosCopias(db.Model):

    __tablename__ = 'libros_copias'

    copiaID = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    libroID = db.Column(db.Integer, db.ForeignKey('libros.libroID'), nullable=False)
    #relacion 1:M(1 Libro N Copias)
    libro = db.relationship('Libro', back_populates='copias')   
    #relacion 1:1(1 Copia 1 Prestamos)
    prestamos = db.relationship('Prestamo', back_populates='copias', cascade='all, delete-orphan')

    @property
    def estado(self):
        if self.prestamos =="disponible":
            return "Disponible"
        return "No disponible"    


    def __repr__(self):
        return '<Copia: %r  >' % (self.copiaID)


    def to_json_short(self):
        libros_copias_json = {
            "copiaID": self.copiaID,
            "libroID": self.libroID,
            "titulo": self.libro.titulo,
            "image": self.libro.image
        }
        return libros_copias_json


    def to_json(self):
        libros_copias_json = {
            "copiaID": self.copiaID,
            "libroID": self.libroID,
            "titulo": self.libro.titulo,
            "libro": self.libro.to_json_short(),
            "estado": self.estado
        }
        return libros_copias_json


    @staticmethod
    def from_json(libros_copias_json):
        copiaID = libros_copias_json.get('copiaID')
        libroID = libros_copias_json.get('libroID')
        return LibrosCopias(copiaID=copiaID, 
                             libroID=libroID)