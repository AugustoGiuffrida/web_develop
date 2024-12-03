from datetime import datetime
from .. import db


class Prestamo(db.Model):
    __tablename__ = 'prestamos'  

    prestamoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarioID = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'), nullable=False) # Clave Foranea
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    fecha_devolucion = db.Column(db.DateTime, nullable=False)
    #relacion 1:1(Usuario es padre)
    usuario = db.relationship("Usuario", back_populates="prestamos",uselist=False,single_parent=True)
    #relacion 1:1(Libro es padre)
    copiaID = db.Column(db.Integer, db.ForeignKey('libros_copias.copiaID'), nullable=False)
    copias = db.relationship("LibrosCopias", back_populates="prestamos",uselist=False,single_parent=True)
    
    
    @property
    def days_left(self):
        today = datetime.now()
        days_left = (self.fecha_devolucion - today).days
        return days_left if days_left >= 0 else 0

    @property
    def status(self):
        if self.fecha_devolucio == datetime.now():
            return 'pending'
        elif self.fecha_devolucio > datetime.now():
            print(self.fecha_devolucio, datetime.now())
            print(self.fecha_devolucio > datetime.now())
            return 'active'
        else:
            return 'expired'

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
        copias = self.copias.to_json_short()
        prestamo_json = {
            "usuario": usuario,
            "copias": copias,
            "prestamoID": self.prestamoID,
            "fecha_entrega": self.fecha_entrega.strftime("%Y-%m-%d"),
            "fecha_devolucion": self.fecha_devolucion.strftime("%Y-%m-%d"),
            "days_left": self.days_left
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
        copiaID = prestamo_json.get('copiaID')
        fecha_entrega = datetime.strptime(prestamo_json.get('fecha_entrega'), '%Y-%m-%d')
        fecha_devolucion = datetime.strptime(prestamo_json.get('fecha_devolucion'), '%Y-%m-%d')
        return Prestamo(prestamoID=prestamoID,
                        usuarioID=usuarioID,
                        copiaID=copiaID,
                        fecha_entrega=fecha_entrega,
                        fecha_devolucion=fecha_devolucion)
