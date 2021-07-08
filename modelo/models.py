from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    Nombre = Column(String, nullable=False)
    IdUsuario=Column(Integer,primary_key=True)
    Sexo=Column(String,nullable=False)
    Telefono=Column(String,nullable=False)
    Email = Column(String, nullable=False)
    Contraseña = Column(String(128), nullable=False)
    #Métodos para el cifrado de la contraseña
    @property
    def password(self):
        raise AttributeError('El atributo password no es un atributo de lectura')
    @password.setter
    def password(self,password):
        self.Contraseña=generate_password_hash(password)
    def validarPassword(self,password):
        return check_password_hash(self.Contraseña, password)
    #metodos del CRUD
    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self.consultaIndividual())
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self):
        return self.query.get(self.idUsuario)
    #Metodos para el perfilamiento de los usuarios
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def is_active(self):
        if self.estatus=='A':
            return True
        else:
            return False
    def is_admin(self):
        if self.tipo=='A':
            return True
        else:
            return False
    def getTipo(self):
        return self.tipo
    def get_id(self):
        return self.IdUsuario
    def validar(self,email,password):
        user=Usuario.query.filter_by(Email=email).first()
        if user!=None:
            if user.validarPassword(password):
                return user
            else:
                return None
        else:
            return None