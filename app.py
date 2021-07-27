import re
from flask import Flask, render_template, request,redirect,url_for,flash,abort
from modelo.models import db, Carreras, Empresas, Usuarios, Alumnos, Reclutadores, PersonalVinculacion, vVinculacion, vAlumnos, vReclutador, OfertaCategoria, Contratos, OfertasAlum,Ofertas,Entrevista
from flask_login import login_user, LoginManager, current_user, logout_user

app = Flask(__name__)

# db=SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/bolsa'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='Cl4v3'
# Configuración de la gestion Usuarios con Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "mostrar_login"
# rutas para el ingreso a la aplicacion

###############################----Tablas de Vigo-----#####################################

#-------CRUD-LOGIN----------#

@login_manager.user_loader
def cargar_usuario(id):
    return Usuarios.query.get(int(id))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route("/validarSesion",methods=['POST'])
def iniciarSesion():
    Us=Usuarios()
    Us=Us.validar(request.form['usuario'],request.form['contraseña'])
    if(Us!=None and Usuarios.is_active(Us)):
        login_user(Us)
        return render_template('Principal.html')
    else:
        return "El usuario o la contraseña es invalido"

@app.route("/CloseSesion")
def cerrarSes():
    if(current_user.is_authenticated):
         logout_user()
         return redirect(url_for("inicio"))
    else:
        abort(404)

@app.route('/pagPrincipal')
def pagPrincipal():
    return render_template('Principal.html')

@app.route('/Perfil/<int:id>')
def perfil(id):
    usuarios=Usuarios()
    usuarios.id_usuario=id
    return render_template('Usuarios/EditarPerfil.html',usuario=usuarios.consultaIndividual())

#-------CRUD-ALUMNOS----------#

@app.route('/registrarAlumno')
def registrarAlumno():
    if current_user.is_admin():
        carreras = Carreras()
        return render_template('AlumnosEgresados/AlumnosEgresados.html',carrera=carreras.consultaGeneral())
    else:
        return "No tienes permitido acceder a esta sección"
    
@app.route('/opcionesAlumno')
def opcionesAlumno():
    if current_user.is_admin():
        alumno=vAlumnos()
        return render_template('AlumnosEgresados/opcionesAlumnos.html',alumnos=alumno.consultaGeneral())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/eliminarAlumno/<int:id>')
def eliminarAlumno(id):
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario=id
        us.estatus="Inactivo"
        us.actualizar()
        return redirect(url_for('opcionesAlumno'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/editarAlumnos/<int:id>')
def editarAlumnos(id):
    if current_user.is_admin():
        alumno=vAlumnos()
        alumno.id_alumno=id
        return render_template('AlumnosEgresados/editarAlumnos.html',alumnos=alumno.consultaIndividual())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/actualizarAlumno2', methods=['POST']) #Esto es algo que se creo para poder editar un perfil ya que con otro nombre daba un problema raro
def actualzarAlumno2():
    us=Usuarios()
    us.id_usuario = request.form['id']
    us.nombre = request.form['nombre']
    us.apellido_paterno = request.form['paterno']
    us.apellido_materno = request.form['materno']
    us.genero = request.form['genero']
    us.telefono = request.form['telefono']
    us.correo = request.form['correo']
    us.estatus = request.form['estatus']
    us.usuario = request.form['usuario']
    us.passwd = request.form['contraseña']
    us.tipo = request.form['tipo']
    us.actualizar()
    return redirect(url_for('pagPrincipal'))

@app.route('/actualizarAlumno', methods=['POST'])
def actualzarAlumno():
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario = request.form['id']
        us.nombre = request.form['nombre']
        us.apellido_paterno = request.form['paterno']
        us.apellido_materno = request.form['materno']
        us.genero = request.form['genero']
        us.telefono = request.form['telefono']
        us.correo = request.form['correo']
        us.estatus = request.form['estatus']
        us.usuario = request.form['usuario']
        us.passwd = request.form['contraseña']
        us.tipo = 'Alumno'
        us.actualizar()
        return redirect(url_for('opcionesAlumno'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/insertarAlumnosBD', methods=['POST'])
def insertAlumnosBD():
    if current_user.is_admin():
        alumnos = Alumnos()
        usuarios = Usuarios()
        usuarios.nombre = request.form['nombre']
        usuarios.apellido_paterno = request.form['paterno']
        usuarios.apellido_materno = request.form['materno']
        usuarios.genero = request.form['genero']
        usuarios.telefono = request.form['telefono']
        usuarios.correo = request.form['correo']
        alumnos.id_carrera = request.form['carrera']
        alumnos.no_control = request.form['control']
        alumnos.fecha_nacimiento = request.form['nacimiento']
        alumnos.promedio = request.form['promedio']
        alumnos.anioEgreso = request.form['egreso']
        alumnos.cv = request.form['cv']
        usuarios.usuario = request.form['usuario']
        usuarios.passwd = request.form['contraseña']
        usuarios.tipo = 'Alumno'
        usuarios.estatus = 'Activo'
        usuarios.insertar()
        alumnos.id_usuario = usuarios.id_usuario
        alumnos.insertar()
        return redirect (url_for('opcionesAlumno'))
    else:
        return "No tienes permitido acceder a esta sección"


#-------CRUD-RECLUTADORES----------#

@app.route('/registrarReclutador')
def registrarReclutador():
    if current_user.is_admin():
        empresas = Empresas()
        return render_template('Reclutadores/Reclutadores.html',empresa=empresas.consultaGeneral())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/opcionesReclutador')
def opcionesReclutador():
    if current_user.is_admin():
        reclutor=vReclutador()
        return render_template('Reclutadores/opcionesReclutadores.html',reclutador=reclutor.consultaGeneral())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/eliminarReclutador/<int:id>')
def eliminarReclutador(id):
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario=id
        us.estatus="Inactivo"
        us.actualizar()
        return redirect(url_for('opcionesReclutador'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/editarReclutador/<int:id>')
def editarReclutador(id):
    if current_user.is_admin():
        reclutador=vReclutador()
        reclutador.id_reclutor=id
        return render_template('Reclutadores/editarReclutadores.html',reclutor=reclutador.consultaIndividual())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/actualizarReclutador', methods=['POST'])
def actualzarReclutador():
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario = request.form['id']
        us.nombre = request.form['nombre']
        us.apellido_paterno = request.form['paterno']
        us.apellido_materno = request.form['materno']
        us.genero = request.form['genero']
        us.telefono = request.form['telefono']
        us.correo = request.form['correo']
        us.estatus = request.form['estatus']
        us.usuario = request.form['usuario']
        us.passwd = request.form['contraseña']
        us.tipo = 'Reclutador'
        us.actualizar()
        return redirect(url_for('opcionesReclutador'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/insertarReclutadorBD', methods=['POST'])
def insertReclutadorBD():
    if current_user.is_admin():
        reclutador = Reclutadores()
        usuarios = Usuarios()
        usuarios.nombre = request.form['nombre']
        usuarios.apellido_paterno = request.form['paterno']
        usuarios.apellido_materno = request.form['materno']
        usuarios.genero = request.form['genero']
        usuarios.telefono = request.form['telefono']
        usuarios.correo = request.form['correo']
        reclutador.id_empresa = request.form['empresa']
        reclutador.clave = request.form['clave']
        reclutador.cargo = request.form['cargo']
        usuarios.usuario = request.form['usuario']
        usuarios.passwd = request.form['contraseña']
        usuarios.tipo = 'Reclutador'
        usuarios.estatus = 'Activo'
        usuarios.insertar()
        reclutador.id_usuario = usuarios.id_usuario
        reclutador.insertar()
        return redirect (url_for('opcionesReclutador'))
    else:
        return "No tienes permitido acceder a esta sección"


#-------CRUD-PERSONAL-VINCULACION----------#

@app.route('/registrarPersonal')
def registrarPersonal():
    if current_user.is_admin():
        return render_template('PersonalVinculacion/PersonalVinculacion.html')
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/opcionesPersonal')
def opcionesPersonal():
    if current_user.is_admin():
        personal=vVinculacion()
        return render_template('PersonalVinculacion/opcionesPersonal.html',vinculacion=personal.consultaGeneral())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/eliminarPersonal/<int:id>')
def eliminarPersonal(id):
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario=id
        us.estatus="Inactivo"
        us.actualizar()
        return redirect(url_for('opcionesPersonal'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/editarPersonal/<int:id>')
def editarPersonal(id):
    if current_user.is_admin():
        vinculacion=vVinculacion()
        vinculacion.id_vinculacion=id
        return render_template('PersonalVinculacion/editarPersonal.html',personal=vinculacion.consultaIndividual())
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/actualizarPersonal', methods=['POST'])
def actualzarPersonal():
    if current_user.is_admin():
        us=Usuarios()
        us.id_usuario = request.form['id']
        us.nombre = request.form['nombre']
        us.apellido_paterno = request.form['paterno']
        us.apellido_materno = request.form['materno']
        us.genero = request.form['genero']
        us.telefono = request.form['telefono']
        us.correo = request.form['correo']
        us.estatus = request.form['estatus']
        us.usuario = request.form['usuario']
        us.passwd = request.form['contraseña']
        us.tipo = 'Reclutador'
        us.actualizar()
        return redirect(url_for('opcionesPersonal'))
    else:
        return "No tienes permitido acceder a esta sección"

@app.route('/insertarPersonalBD', methods=['POST'])
def insertPersonalBD():
    if current_user.is_admin():
        personal = PersonalVinculacion() 
        usuarios = Usuarios()
        usuarios.nombre = request.form['nombre']
        usuarios.apellido_paterno = request.form['paterno']
        usuarios.apellido_materno = request.form['materno']
        usuarios.genero = request.form['genero']
        usuarios.telefono = request.form['telefono']
        usuarios.correo = request.form['correo']
        personal.clave = request.form['clave']
        personal.cargo = request.form['cargo']
        usuarios.usuario = request.form['usuario']
        usuarios.passwd = request.form['contraseña']
        usuarios.tipo = 'Administrador'
        usuarios.estatus = 'Activo'
        usuarios.insertar()
        personal.id_usuario = usuarios.id_usuario
        personal.insertar()
        return redirect (url_for('opcionesPersonal'))
    else:
        return "No tienes permitido acceder a esta sección"

#######################################################-- Fin de Vigo--###################################################

###################################################----Tablas de Ale-----#####################################

#-------CRUD-CARRERAS----------#

@app.route('/registrarCarrera')
def registrarCarreras():
    return render_template('Carreras/registrarCarreras.html')

@app.route('/opcionesCarreras')
def opcionesCarreras():
    ca=Carreras()
    return render_template('Carreras/opcionesCarreras.html', carrera=ca.consultaGeneral())

@app.route('/editarCarrera/<int:id>')
def ventanaEditarCarrera(id):
    ca=Carreras()
    ca.id_carrera=id
    return render_template('Carreras/modificarCarreras.html',ca=ca.consultaIndividual())

@app.route('/eliminarCarrera/<int:id>')
def ventanaEliminarCarrera(id):
    ca=Carreras()
    ca.id_carrera=id
    ca.estatus="Inactivo"
    ca.actualizar()
    return redirect(url_for('opcionesCarreras'))

@app.route('/insertarCarrerasBD', methods=['POST'])
def insertCarrerasBD():
    try:
        ca=Carreras()
        ca.nombreC=request.form['nombre']
        ca.clave=request.form['clave']
        ca.estatus='Activo'
        ca.insertar()
        flash('¡ Carrera agregada con exito !')
    except: 
        flash('¡ Error al agregar la Carrera !')
    return redirect (url_for('opcionesCarreras')) 

@app.route('/actualizarCarrerasBD', methods=['POST'])
def actualzarTurnosBD():
    ca=Carreras()
    ca.id_carrera=request.form['idcarrera']
    ca.nombreC=request.form['nombre']
    ca.clave=request.form['clave']
    ca.estatus=request.form['estatus']
    ca.actualizar()
    return redirect(url_for('opcionesCarreras'))

#------CRUD EMPRESAS----------#


@app.route('/registrarEmpresa')
def registrarEmpresas():
    return render_template('Empresas/registrarEmpresas.html')


@app.route('/opcionesEmpresa')
def opcionesEmpresas():
    em=Empresas()
    return render_template('Empresas/opcionesEmpresas.html', empresa=em.consultaGeneral())

@app.route('/editarEmpresa/<int:id>')
def ventanaEditarEmpresa(id):
    em=Empresas()
    em.id_empresa=id
    return render_template('Empresas/modificarEmpresas.html', em=em.consultaIndividual())


@app.route('/eliminarEmpresa/<int:id>')
def ventanaEliminarEmpresa(id):
    em=Empresas()
    em.id_empresa=id
    em.estatus="Inactivo"
    em.actualizar()

    return redirect(url_for('opcionesEmpresas'))

@app.route('/insertarEmpresasBD', methods=['POST'])
def insertEmpresasBD():
    em=Empresas()
    em.nombreE=request.form['nombre']
    em.rfc=request.form['rfc']
    em.direccion=request.form['direccion']
    em.giro=request.form['giro']
    em.paginaweb=request.form['web']
    em.estatus='Activo'
    em.insertar()
    return redirect (url_for('opcionesEmpresas')) 

@app.route('/actualizarEmpresasBD', methods=['POST'])
def actualzarEmpresaBD():
    em=Empresas()
    em.id_empresa=request.form['idempresa']
    em.nombreE=request.form['nombre']
    em.rfc=request.form['rfc']
    em.direccion=request.form['direccion']
    em.giro=request.form['giro']
    em.paginaweb=request.form['web']
    em.estatus=request.form['estatus']
    em.actualizar()
    return redirect(url_for('opcionesEmpresas'))


#------CRUD de Ofertas---------#

@app.route('/registrarOferta')
def registrarOfertas():

    emp = Empresas()
    con=Contratos()
    re=vReclutador()
    cat=OfertaCategoria()

    empresa=emp.consultaGeneral()
    contrato=con.consultaGeneral()
    reclutor=re.consultaGeneral()
    categoria=cat.consultaGeneral()

    return render_template('Ofertas/registrarOfertas.html',empresa=empresa,contrato=contrato, reclutor=reclutor, categoria=categoria)

@app.route('/opcionesOfertas')
def opcionesOfertas():
    of= Ofertas()
    emp = Empresas()
    con=Contratos()
    re=vReclutador()
    cat=OfertaCategoria()

    empresa=emp.consultaGeneral()
    contrato=con.consultaGeneral()
    reclutor=re.consultaGeneral()
    categoria=cat.consultaGeneral()
    ofertas=of.consultaGeneral()
    return render_template('Ofertas/opcionesOfertas.html',empresa=empresa, contrato=contrato, reclutor=reclutor, categoria=categoria, ofertas=ofertas )

@app.route('/insertarOfertasBD', methods=['POST'])
def insertOfertasBD():
    of=Ofertas()

    of.id_empresa=request.form['empresa']
    of.idofcat=request.form['categoria']
    of.id_contrato=request.form['contrato']
    of.id_reclutor=request.form['reclutor']
    of.nombre=request.form['nombre']
    of.descripcion=request.form['descr']
    of.fecha_publicacion=request.form['fecha']
    of.salario=request.form['salario']
    of.num_vacante=request.form['vacantes']
    of.estatus='Activo'

    of.insertar()
    return redirect (url_for('opcionesOfertas')) 

@app.route('/editarOferta/<int:id>')
def ventanaEditarOferta(id):
    of=Ofertas()
    of.id_oferta=id
    return render_template('Ofertas/modificarOfertas.html', of=of.consultaIndividual())


@app.route('/eliminarOferta/<int:id>')
def ventanaEliminarOferta(id):
    of=Ofertas()
    of.id_oferta=id
    of.estatus="Inactivo"
    of.actualizar()

    return redirect(url_for('opcionesOfertas'))

    
@app.route('/actualizarOfertasBD', methods=['POST'])
def actualzarOfertaBD():
    of=Ofertas()

    of.id_oferta=request.form['idoferta']
    of.id_empresa=request.form['empresa']
    of.idofcat=request.form['categoria']
    of.id_contrato=request.form['contrato']
    of.nombre=request.form['nombre']
    of.descripcion=request.form['descr']
    of.fecha_publicacion=request.form['fecha']
    of.salario=request.form['salario']
    of.num_vacante=request.form['vacantes']
    of.estatus=request.form['estatus']

    of.actualizar()
    return redirect(url_for('opcionesOfertas'))




#-----CRUD ENTREVISTAS-------#

@app.route('/registrarEntrevista')
def registrarEntrevista():

    re=vReclutador()
    alu=vAlumnos()
    of=Ofertas()

    reclutor=re.consultaGeneral()
    alumno=alu.consultaGeneral()
    oferta=of.consultaGeneral()
    return render_template('Entrevistas/registrarEntrevista.html' ,reclutor=reclutor, alumno=alumno,oferta=oferta)


@app.route('/opcionesEntrevista')
def opcionesEntrevista():
    en=Entrevista()
    
    re=vReclutador()
    alu=vAlumnos()
    of=Ofertas()

    reclutor=re.consultaGeneral()
    alumno=alu.consultaGeneral()
    oferta=of.consultaGeneral()
    return render_template('Entrevistas/opcionesEntrevista.html',reclutor=reclutor, alumno=alumno,oferta=oferta)



@app.route('/insertarEntrevistaBD', methods=['POST'])
def insertOEntrevistaBD():
    en=Entrevista()

  
    en.id_reclutor=request.form['reclutor']
    en.id_alumno=request.form['alumno']
    en.id_oferta=request.form['oferta']
    en.fecha_registro=request.form['registro']
    en.fecha_entrevista=request.form['entrevista']
    en.hora_inicio=request.form['hinicio']
    en.hora_fin=request.form['hfin']
    en.resultado=request.form['resultado']
    en.estatus='Activo'

    en.insertar()
    return redirect (url_for('opcionesEntrevista')) 

@app.route('/editarEntrevista/<int:id>')
def ventanaEditarEntrevista(id):
    en=Entrevista()
    en.id_entrevista=id
    return render_template('Entrevistas/modificarEntevistas.html', en=en.consultaIndividual())


@app.route('/eliminarEntrevista/<int:id>')
def ventanaEliminarEntrevista(id):
    en=Entrevista()
    en.id_entrevista=id
    en.estatus="Inactivo"
    en.actualizar()

    return redirect(url_for('opcionesEntrevista'))

    
@app.route('/actualizarEntrevistaBD', methods=['POST'])
def actualzarEntrevistaBD():
    en=Entrevista()

    en.id_entrevista=request.form['identrevista']
    en.estatus=request.form['estatus']

    en.actualizar()
    return redirect(url_for('opcionesEntrevista'))

#######################################################-- Fin de Ale--###################################################   

#######################--------Tablas de meny-----------#############################
#####-----CRUD Contrato-----#####


@app.route('/registrarContrato')
def registrarContrato():
    if current_user.is_admin():
        return render_template('Contratos/registrarContrato.html')
    else:
        return "No tienes permiso para registra un contrato" 
        

@app.route('/Contratos/registrarContratoBD',methods=['post'])
def insertContrato():
    co =  Contratos()
    co.nombre = request.form['nombre']
    co.estatus = 'Activo'
    co.insertar()
    return render_template('Contratos/registrarContrato.html')

@app.route('/opcionesContratos')
def opcionesContratos():
    co=Contratos()
    return render_template('Contratos/opcionesContratos.html', contratos=co.consultaGeneral())

@app.route('/editarContrato/<int:id>')
def ventanaEditarContratos(id):
    if current_user.is_admin():
        co=Contratos()
        co.id_contrato=id
        return render_template('/Contratos/modificarContratos.html',co=co.consultaIndividual())
    else:
        return "No puedes editar un contracto no tienes permisos expeciales"

@app.route('/eliminarContrato/<int:id>')
def ventanaElimiarContratos(id):
    if current_user.is_admin():
        co=Contratos()
        co.id_contrato=id
        co.estatus="Inactivo"
        co.actualizar()
        return redirect(url_for('opcionesContratos'))
    else:
        return "No puedes eliminar un contrato ocupas permisos expeciales"

@app.route('/actualizarContratosBD', methods=['POST'])
def actualizarContratoBD():
    co=Contratos()
    co.id_contrato=request.form['id_contrato']
    co.nombre=request.form['nombre']
    co.estatus=request.form['estatus']
    co.actualizar()
    return redirect(url_for('opcionesContratos'))

#####-----CRUD Categoria-----#####

@app.route('/registrarCategoria')
def registrarCategoria():
    if current_user.is_admin():
        return render_template('Categoria/registrarCategoria.html')
    else:
        return "No tienes permisos registra una categoria"

@app.route('/Categoria/registrarCategoriaBD',methods=['post'])
def insertCategoria():
    ca =  OfertaCategoria()
    ca.nombre = request.form['nombre']
    ca.estatus = 'Activo'
    ca.insertar()
    return render_template('Categoria/registrarCategoria.html')

@app.route('/opcionesCategoria')
def opcionesCategoria():
    ca=OfertaCategoria()
    return render_template('Categoria/opcionesCategoria.html', ofertacategoria=ca.consultaGeneral())

@app.route('/editarCategoria/<int:id>')
def ventanaEditarCategoria(id):
    if current_user.is_admin():
        ca=OfertaCategoria()
        ca.idofcat=id
        return render_template('/Categoria/modificarCategoria.html',ca=ca.consultaIndividual())
    else:
        return "No puedes editar una categoria"

@app.route('/eliminarCategoria/<int:id>')
def ventanaElimiarCategoria(id):
    if current_user.is_admin():
        ca=OfertaCategoria()
        ca.idofcat=id
        ca.estatus="Inactivo"
        ca.actualizar()
        return redirect(url_for('opcionesCategoria'))
    else:
        return "No tienes permisos para elimiar la categoria"

@app.route('/actualizarCategoriaBD', methods=['POST'])
def actualizarCategoriaBD():
        ca=OfertaCategoria()
        ca.idofcat=request.form['idofcat']
        ca.nombre=request.form['nombre']
        ca.estatus=request.form['estatus']
        ca.actualizar()
        return redirect(url_for('opcionesCategoria'))

#####-----CRUD Postulacion-----#####

@app.route('/registrarOAlu')
def registrarOAlu():
    if current_user.is_admin():
        alumno=vAlumnos();
        ofertas=Ofertas();
        return render_template('Postulacion/registrarOAlu.html',alumnos=alumno.consultaGeneral(), oferta=ofertas.consultaGeneral())
    else:
        return "No puedes restra una oferta alumno sin permiso expeciales"

@app.route('/opcionesOAlu')
def opcionesOAlu():
    oa=OfertasAlum()
    return render_template('Postulacion/opcionesOAlu.html', ofertasalum=oa.consultaGeneral())

@app.route('/editarOAlu/<int:id>')
def ventanaEditarCAlu(id):
    ##if current_user.is_admin():
        oa=OfertasAlum()
        oa.id_of_alum=id
        return render_template('/Postulacion/modificarOAlu.html',oa=oa.consultaIndividual())
    ##else:
        ##return "No puedes editar un contracto no tienes permisos expeciales"

##############################################################################

@app.errorhandler(404)
def error_404(e):
    return render_template('Comunes/error404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('Comunes/error500.html'), 500


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
