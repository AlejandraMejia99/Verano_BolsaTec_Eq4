from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey, Date, Float,DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#------- Apartado de Ale---------#

class Carreras(db.Model):
    __tablename__='Carreras'
    id_carrera=Column(Integer,primary_key=True)
    clave=Column(String,nullable=False)
    nombreC=Column(String,unique=True)
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
    nombreE= Column(String,nullable=False)
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


class Ofertas(db.Model):
    __tablename__='Ofertas'
    id_oferta=Column(Integer,primary_key=True)
    id_contrato=Column(Integer,ForeignKey('Contratos.id_contrato'))
    id_empresa=Column(Integer, ForeignKey('Empresas.id_empresa'))
    id_reclutor=Column(Integer, ForeignKey('Reclutadores.id_reclutor'))
    idofcat=Column(Integer, ForeignKey('OfertaCategoria.idofcat'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=False)
    fecha_publicacion=Column(Date, nullable=False)
    salario=Column(Float, nullable=False)
    num_vacante= Column(String,nullable=False)
    estatus= Column(String,nullable=False)
    contrato=relationship('Contratos', backref='ofertas')
    empresas=relationship('Empresas', backref='ofertas')
    reclutor=relationship('Reclutadores', backref='ofertas')
    categoria=relationship('OfertaCategoria', backref='ofertas')

    def insertar(self):                                                                                                                                                                          
        db.session.add(self)                                                                                                                                                                     
        db.session.commit() 

    def consultaGeneral(self):                                                                                                                                                                   
        of=self.query.all()                                                                                                                                                                   
        return of

    def consultaIndividual(self):
        of=self.query.get(self.id_oferta)
        return of
        
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        of=self.consultaIndividual()
        db.session.delete(of)
        db.session.commit()


class Entrevista(db.Model):
    __tablename__='Entrevista'
    id_entrevista=Column(Integer,primary_key=True)
    id_reclutor=Column(Integer, ForeignKey('Reclutadores.id_reclutor'))
    id_alumno=Column(Integer, ForeignKey('Alumnos.id_alumno'))
    id_oferta=Column(Integer, ForeignKey('Ofertas.id_oferta'))
    fecha_registro =Column(Date, nullable=False)
    fecha_entrevista=Column(Date, nullable=False)
    hora_inicio=Column(String, nullable=False)
    hora_fin=Column(String, nullable=False)
    resultado= Column(String,nullable=False)
    estatus= Column(String,nullable=False)
    reclutor=relationship('Reclutadores', backref='entrevista')
    alumnos=relationship('Alumnos',backref='entrevista')
    ofertas=relationship('Ofertas', backref='entrevista')

    def insertar(self):                                                                                                                                                                          
        db.session.add(self)                                                                                                                                                                     
        db.session.commit()

    def consultaGeneral(self):                                                                                                                                                                   
        en=self.query.all()                                                                                                                                                                   
        return en

    def consultaIndividual(self):
        en=self.query.get(self.id_entrevista)
        return en
        
    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        en=self.consultaIndividual()
        db.session.delete(en)
        db.session.commit()


#------------------------------------------------------Fin de Ale ---------------------#
    

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

    def consultaIndividual(self):
        us = self.query.get(self.id_usuario)
        return us
        
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
    id_usuario=Column(Integer, nullable=False)
    nombre=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    genero=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    usuario=Column(String, nullable=False)
    passwd=Column(String, nullable=False)
    estatus=Column(String, nullable=False)
    cargo=Column(String, nullable=False)

    def consultaGeneral(self):
        vin = self.query.all()
        return vin

    def consultaIndividual(self):
        vin = self.query.get(self.id_vinculacion)
        return vin

class vAlumnos(db.Model):
    __tablename__='vAlumnos'
    id_alumno=Column(Integer, primary_key=True)
    id_usuario=Column(Integer, nullable=False)
    nombre=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    genero=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    usuario=Column(String, nullable=False)
    passwd=Column(String, nullable=False)
    promedio=Column(Float, nullable=False)
    anioEgreso=Column(Date, nullable=False)
    cv=Column(String, nullable=False)
    estatus=Column(String, nullable=False)

    def consultaGeneral(self):
        alu = self.query.all()
        return alu

    def consultaIndividual(self):
        alu = self.query.get(self.id_alumno)
        return alu

class vReclutador(db.Model):
    __tablename__='vReclutador'
    id_reclutor=Column(Integer, primary_key=True)
    id_usuario=Column(Integer, nullable=False)
    nombre=Column(String, nullable=False)
    nombreE=Column(String, nullable=False)
    apellido_paterno=Column(String, nullable=False)
    apellido_materno=Column(String, nullable=False)
    genero=Column(String, nullable=False)
    telefono=Column(String, nullable=False)
    correo=Column(String, nullable=False)
    usuario=Column(String, nullable=False)
    passwd=Column(String, nullable=False)
    cargo=Column(String, nullable=False)
    estatus=Column(String, nullable=False)

    def consultaGeneral(self):
        rec = self.query.all()
        return rec

    def consultaIndividual(self):
        rec = self.query.get(self.id_reclutor)
        return rec

#-------Meny--------#
class Contratos(db.Model):
    __tablename__='Contratos'
    id_contrato=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

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

    def is_probicion(self):
        if self.tipo=='Alumno':
            return False
        else:
            return True

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

class OfertasAlum(db.Model):
    __tablename__ = 'OfertasAlum'
    id_of_alum = Column(Integer, primary_key=True)
    id_alumno = Column(Integer, ForeignKey('Alumnos.id_alumno'))
    id_oferta = Column(Integer, ForeignKey('Ofertas.id_oferta'))
    fecha_postulacion = Column(Date, nullable=False)
    estatus = Column(String, nullable=False)

    alumno = relationship('Alumnos', backref='ofertasalum')
    oferta = relationship('Ofertas', backref='OfertasAlum')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self):
        of=self.query.get(self.id_of_alum)
        return of

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self):
        of=self.consultaIndividual()
        db.session.delete(of)
        db.session.commit()