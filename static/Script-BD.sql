CREATE DATABASE IF NOT EXISTS bolsa;
use  bolsa;

create table Carreras (
	id_carrera int not null AUTO_INCREMENT,
	clave VARCHAR(15) NOT NULL,
	nombre varchar(50) not null,
	estatus VARCHAR(20) not null,
	primary key (id_carrera));

create table Contratos (
	id_contrato int not null AUTO_INCREMENT,
    nombre varchar(50) not null,
    estatus VARCHAR(20) not null,
	primary key (id_contrato)
);

Create table Empresas(
	id_empresa int not null AUTO_INCREMENT,
	nombre varchar(100)not null,
	rfc varchar(55) not null,
	direccion varchar(60) not null ,
	giro varchar(50) not null,
	paginaweb varchar(100) not null,
	estatus VARCHAR(20) not null,
	primary key (id_empresa));

create table OfertaCategoria(
	idofcat int not null AUTO_INCREMENT,
	nombre varchar(100)not null,
	estatus VARCHAR(20) not null,
	primary key (idofcat));

CREATE TABLE IF NOT EXISTS Usuarios(
  id_usuario INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  apellido_paterno VARCHAR(100) NOT NULL,
  apellido_materno VARCHAR(100) NOT NULL,
  genero VARCHAR(15) NOT NULL,
  telefono VARCHAR(15) NOT NULL,
  correo VARCHAR(60) NOT NULL,
  usuario VARCHAR(45) NOT NULL,
  passwd VARCHAR(45) NOT NULL,
  tipo VARCHAR(35) NOT NULL,
  estatus VARCHAR(20) NOT NULL,
  PRIMARY KEY (id_usuario));
  
CREATE TABLE IF NOT EXISTS Alumnos(
  id_alumno INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_carrera INT NOT NULL,
  no_control INT NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  promedio FLOAT NULL DEFAULT NULL,
  anioEgreso DATE not null,
  cv varchar(50) not null,
  PRIMARY KEY (id_alumno),
  foreign key(id_usuario) references Usuarios(id_usuario),
  foreign key (id_carrera) references Carreras(id_carrera));
  
Create table Reclutadores(
	id_reclutor int not null AUTO_INCREMENT,
	id_usuario int not null,
	id_empresa int not null,
	clave VARCHAR(15) NOT NULL,
	cargo varchar(50) not null,
	primary key (id_reclutor),
	foreign key(id_usuario) references Usuarios(id_usuario),
	foreign key(id_empresa) references Empresas(id_empresa));

Create table PersonalVinculacion(
	id_vinculacion int not null AUTO_INCREMENT,
	id_usuario int not null,
	clave VARCHAR(15) NOT NULL,
	cargo varchar(50),
	primary key (id_vinculacion),
	foreign key(id_usuario) references Usuarios(id_usuario));

Create table Ofertas(
	id_oferta int not null AUTO_INCREMENT,
	id_contrato int not null,
	id_empresa int not null,
	id_reclutor int not null,
	idofcat int not null,
	nombre varchar(50) not null,
	descripcion varchar(50) not null,
	fecha_publicacion date not null,
	salario float not null,
	num_vacante varchar(10) not null,
	estatus varchar(20) not null,
	primary key (id_oferta),
	foreign key(id_contrato) references Contratos(id_contrato),
	foreign key(id_empresa) references Empresas(id_empresa),
	foreign key(idofcat) references  OfertaCategoria(idofcat),
	foreign key(id_reclutor) references Reclutadores(id_reclutor));

create table Entrevista (
	id_entrevista int not null AUTO_INCREMENT,
    id_reclutor int  not null,
	id_alumno int not null,
    id_oferta int not null,
    fecha_registro date not null,
    fecha_entrevista date not null,
    hora_inicio datetime not null,
    hora_fin datetime not null,
    resultado varchar(50) not null,
    estatus varchar(20) not null,
	primary key (id_entrevista),
    foreign key(id_oferta) references Ofertas(id_oferta),
    foreign key(id_reclutor) references Reclutadores(id_reclutor),
    foreign key(id_alumno) references Alumnos(id_alumno));

create table OfertasAlum(
	id_of_alum int not null AUTO_INCREMENT,
	id_alumno int not null,
	id_oferta int not null,
	fecha_postulacion  date not null,
	estatus  varchar(20) not null,
	primary key (id_of_alum),
	foreign key(id_oferta) references Ofertas(id_oferta),
	foreign key(id_alumno) references Alumnos(id_alumno));


CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON bolsa.* TO 'admin'@'localhost';

SET SQL_SAFE_UPDATES = 0;


