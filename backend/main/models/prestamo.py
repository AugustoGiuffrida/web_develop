from datetime import datetime
from .. import db


class Prestamo(db.Model):
    __tablename__ = 'prestamos'  # Nombre de la tabla en plural

    prestamoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarioID = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'), nullable=False) # Clave Foranea
    libroID = db.Column(db.Integer, db.ForeignKey("libros.libroID"), nullable=False)  # Clave Foranea
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    fecha_devolucion = db.Column(db.DateTime, nullable=False)
    #relacion 1:1(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="prestamos",uselist=False,single_parent=True)
    #relacion N:M(Libro es padre)
    libro = db.relationship("Libro", back_populates="prestamos")
    

    def __repr__(self):
        return '<Prestamo: %r >' % (self.prestamoID)

    # Convertir objeto en JSON   
    def to_json(self):
        Prestamo_json = {
            "prestamoID": self.prestamoID,
            "fecha_entrega": self.fecha_entrega.strftime("%Y-%m-%d"),      
            "fecha_devolucion": self.fecha_devolucion.strftime("%Y-%m-%d"),
        }
        return Prestamo_json

    def to_json_complete(self):
        usuario = self.usuario.to_json_short()
        libro = self.libro.to_json_short()

        prestamo_json = {
            "prestamoID": self.prestamoID,
            "usuario": usuario,
            "libro": libro,
            "fecha_entrega": self.fecha_entrega.strftime("%Y-%m-%d"),
            "fecha_devolucion": self.fecha_devolucion.strftime("%Y-%m-%d"),
        }
        return prestamo_json

    def to_json_short(self):
        Prestamo_json = {
            "fecha_entrega": self.fecha_entrega.strftime("%Y-%m-%d"),      
            "fecha_devolucion": self.fecha_devolucion.strftime("%Y-%m-%d"),
        }
        return Prestamo_json

    @staticmethod
    # Convertir JSON a objeto
    def from_json(prestamo_json):
        prestamoID = prestamo_json.get('prestamoID')
        usuarioID = prestamo_json.get('usuarioID')
        libroID = prestamo_json.get('libroID')
        fecha_entrega = datetime.strptime(prestamo_json.get('fecha_entrega'), '%Y-%m-%d')
        fecha_devolucion = datetime.strptime(prestamo_json.get('fecha_devolucion'), '%Y-%m-%d')
        return Prestamo(prestamoID=prestamoID,
                        usuarioID=usuarioID,
                        libroID=libroID,
                        fecha_entrega=fecha_entrega,
                        fecha_devolucion=fecha_devolucion)
