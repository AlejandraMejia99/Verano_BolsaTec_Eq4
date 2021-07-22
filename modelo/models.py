from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin,db.Model):
    __tablename__='Usuario'
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


class Carreras(db.Model):
    __tablename__='Carreras'
    id_carrera=Column(Integer,primary_key=True)
    clave=Column(String,nullable=False)
    nombre=Column(String,unique=True)
    estatus= Column(String,nullable=False)


    def insertar(self):                                                                                                                                                                          
        db.session.add(self)                                                                                                                                                                     
        db.session.commit() 
    def consultaGeneral(self):                                                                                                                                                                   
        ca=self.query.all()                                                                                                                                                                   
        return ca
    def consultaIndividual(self):
        ca=self.query.get(self.id_carrera)
        return ca
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()
    def eliminar(self):
        ca=self.consultaIndividual()
        db.session.delete(ca)
        db.session.commit()

class Empresas(db.Model):
    __tablename__='Empresas'
    id_empresa =Column(Integer,primary_key=True)
    nombre= Column(String,nullable=False)
    rfc = Column(String,nullable=False)
    direccion = Column(String,nullable=False)
    giro=Column(String,nullable=False)
    paginaweb = Column(String,nullable=False)
    estatus = Column(String,nullable=False)

    def insertar(self):                                                                                                                                                                          
        db.session.add(self)                                                                                                                                                                     
        db.session.commit() 
    def consultaGeneral(self):                                                                                                                                                                   
        em=self.query.all()                                                                                                                                                                   
        return em
    def consultaIndividual(self):
        em=self.query.get(self.id_empresa)
        return em
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()
    def eliminar(self):
        em=self.consultaIndividual()
        db.session.delete(em)
        db.session.commit()

#-------VIGO--------#

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    usuario = Column(String, nullable=False)
    passwd = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    estatus = Column(String, nullable=False)

    @property 
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter
    def password(self, password):
        self.passwd=generate_password_hash(password)

    def validarPassword(self,passs):
        pwd = Usuarios.query.filter_by(passwd=passs).first()
        return pwd
    
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id_usuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False

    def is_alumno(self):
        if self.tipo=='Alumno':
            return True
        else:
            return False

    def is_reclutador(self):
        if self.tipo=='Reclutador':
            return True
        else:
            return False
    
    def validar(self,us,ps):
        emp=Usuarios.query.filter_by(usuario=us).first()
        if(emp!=None):
            if(emp.validarPassword(ps)):
                return emp
            else:
                return None

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()
        
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

class Alumnos(db.Model):
    __tablename__ = 'Alumnos'
    id_alumno = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('Usuarios.id_usuario'))
    id_carrera = Column(Integer, ForeignKey('Carreras.id_carrera'))
    no_control = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    promedio = Column(Float, nullable=False)
    anioEgreso = Column(Date, nullable=False)
    cv = Column(String, nullable=False)

    usuario = relationship('Usuarios', backref='alumnos')
    carrera = relationship('Carreras', backref='alumnos')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self):
        al = self.query.get(self.id_alumno)
        return al

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

class Reclutadores(db.Model):
    __tablename__ = 'Reclutadores'
    id_reclutor = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('Usuarios.id_usuario'))
    id_empresa = Column(Integer, ForeignKey('Empresas.id_empresa'))
    clave = Column(String, nullable=False)
    cargo = Column(String, nullable=False)

    usuario = relationship('Usuarios', backref='reclutadores')
    empresa = relationship('Empresas', backref='reclutadores')

    def insertar(self):
        db.session.add(self)
        db.session.commit()
    

class PersonalVinculacion(db.Model):
    __tablename__ = 'PersonalVinculacion'
    id_vinculacion = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('Usuarios.id_usuario'))
    clave = Column(String, nullable=False)
    cargo = Column(String, nullable=False)

    usuario = relationship('Usuarios', backref='personalvinculacion')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        vin = self.query.all()
        return vin

    def consultaIndividual(self):
        vin = self.query.get(self.id_empresa)
        return vin

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        vin = self.consultaIndividual()
        db.session.delete(vin)
        db.session.commit()

class vVinculacion(db.Model):
    __tablename__='vVinculacion'
    id_vinculacion=Column(Integer, primary_key=True)
    nombre=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    genero=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    usuario=Column(String, nullable=False)
    estatus=Column(String, nullable=False)
    cargo=Column(String, nullable=False)

    def consultaGeneral(self):
        vin = self.query.all()
        return vin

class vAlumnos(db.Model):
    __tablename__='vAlumnos'
    id_alumno=Column(Integer, primary_key=True)
    id_usuario=Column(Integer, nullable=False)
    nombre=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    promedio=Column(Float, nullable=False)
    anioEgreso=Column(Date, nullable=False)
    cv=Column(String, nullable=False)
    estatus=Column(String, nullable=False)

    def consultaGeneral(self):
        vin = self.query.all()
        return vin

class vReclutador(db.Model):
    __tablename__='vReclutador'
    id_reclutor=Column(Integer, primary_key=True)
    nombre=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    cargo=Column(String, nullable=False)
    estatus=Column(String, nullable=False)

    def consultaGeneral(self):
        vin = self.query.all()
        return vin

class Contratos(db.Model):
    __tablename__='Contratos'
    id_contrato=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        co=self.query.all()
        return co

    def consultaIndividual(self):
        co=self.query.get(self.id_contrato)
        return co

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        co=self.consultaIndividual()
        db.session.delete(co)
        db.session.commit()

class OfertaCategoria(db.Model):
    __tablename__='OfertaCategoria'
    idofcat=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        ca=self.query.all()
        return ca

    def consultaIndividual(self):
        ca=self.query.get(self.idofcat)
        return ca

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        ca=self.consultaIndividual()
        db.session.delete(ca)
        db.session.commit()