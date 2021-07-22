from flask import Flask, render_template, request,redirect,url_for,flash,abort
from modelo.models import db, Usuario, Carreras, Empresas, Usuarios, Alumnos, Reclutadores, PersonalVinculacion, vVinculacion, vAlumnos, vReclutador, OfertaCategoria, Contratos
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


#@login_manager.user_loader
#def load_user(id):
#    return Usuario.query.get(int(id))

@login_manager.user_loader
def cargar_usuario(id):
    return Usuarios.query.get(int(id))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/Perfil')
def perfil():
    return render_template('Usuarios/EditarPerfil.html')

#############---CRUD  de ALUMNOS EGRESADOS###############################################


@app.route('/registrarAlumno')
def alumnos():
    return render_template('AlumnosEgresados/AlumnosEgresados.html')


@app.route('/altaAlumnos')
def alta_Alumnos():
    return render_template('AlumnosEgresados/altaAlumnos.html')


@app.route('/consultaAlumnos')
def consulta_Alumnos():
    return render_template('AlumnosEgresados/consultaAlumnos.html')


@app.route('/editarAlumnos')
def editar_Alumnos():
    return render_template('AlumnosEgresados/editarAlumnos.html')


@app.route('/eliminarAlumnos')
def eliminar_Alumnos():
    return render_template('AlumnosEgresados/eliminarAlumnos.html')


#@app.route('/opcionesAlumno')
#def opciones_Alumnos():
#    return render_template('AlumnosEgresados/opcionesAlumnos.html')
#############################################################################################################

#######################-------CRUD DE PersonalVinculacion--------###################


@app.route('/registrarPersonal')
def personal():
    return render_template('PersonalVinculacion/PersonalVinculacion.html')


@app.route('/altaPersonalVinculacion')
def alta_Reclutores():
    return render_template('PersonalVinculacion/altaPersonalVinculacion.html')


@app.route('/consultaPersonalVinculacion')
def consulta_PersonalVinculacion():
    return render_template('PersonalVinculacion/consultaPersonalVinculacion.html')


@app.route('/editarPersonalVinculacion')
def editar_PersonalVinculacion():
    return render_template('PersonalVinculacion/editarPersonalVinculacion.html')


@app.route('/eliminarPersonalVinculacion')
def eliminar_PersonalVinculacion():
    return render_template('PersonalVinculacion/eliminarPersonalVinculacion.html')


@app.route('/opcionesPersonal')
def opciones_Personal():
    return render_template('PersonalVinculacion/opcionesPersonal.html')
#####################----CRUD de Reclutores--------##############


@app.route('/registrarReclutador')
def reclutores():
    return render_template('Reclutadores/Reclutadores.html')


@app.route('/altaReclutores')
def alta_Reclutador():
    return render_template('Reclutadores/altaReclutores.html')


@app.route('/consultaReclutores')
def consulta_Reclutador():
    return render_template('Reclutadores/consultaReclutores.html')


@app.route('/editarReclutores')
def editar_Reclutador():
    return render_template('Reclutadores/editarReclutores.html')


@app.route('/eliminarReclutores')
def eliminar_Reclutador():
    return render_template('Reclutadores/eliminarReclutores.html')


@app.route('/opcionesReclutador')
def opciones_Reclutador():
    return render_template('Reclutadores/opcionesReclutadores.html')

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
        ca.nombre=request.form['nombre']
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
    ca.nombre=request.form['nombre']
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
    em.nombre=request.form['nombre']
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
    em.nombre=request.form['nombre']
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
    return render_template('Ofertas/registrarOfertas.html')


@app.route('/opcionesOfertas')
def opcionesOfertas():
    return render_template('Ofertas/opcionesOfertas.html')

#-----CRUD ENTREVISTAS-------#


@app.route('/registrarEntrevista')
def registrarEntrevista():
    return render_template('Entrevistas/registrarEntrevista.html')


@app.route('/opcionesEntrevista')
def opcionesEntrevista():
    return render_template('Entrevistas/opcionesEntrevista.html')

#######################################################-- Fin de Ale--###################################################   

#######################--------Tablas de meny-----------#############################
#####-----CRUD Contrato-----#####


@app.route('/registrarContrato')
def registrarContrato():
    return render_template('Contratos/registrarContrato.html')

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
    co=Contratos()
    co.id_contrato=id
    return render_template('/Contratos/modificarContratos.html',co=co.consultaIndividual())

@app.route('/eliminarContrato/<int:id>')
def ventanaElimiarContratos(id):
    co=Contratos()
    co.id_contrato=id
    co.estatus="Inactivo"
    co.actualizar()
    return redirect(url_for('opcionesContratos'))

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
    return render_template('Categoria/registrarCategoria.html')

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
    ca=OfertaCategoria()
    ca.idofcat=id
    return render_template('/Categoria/modificarCategoria.html',ca=ca.consultaIndividual())

@app.route('/eliminarCategoria/<int:id>')
def ventanaElimiarCategoria(id):
    ca=OfertaCategoria()
    ca.idofcat=id
    ca.estatus="Inactivo"
    ca.actualizar()
    return redirect(url_for('opcionesCategoria'))

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
    return render_template('Postulacion/registrarOAlu.html')


@app.route('/opcionesOAlu')
def opcionesOAlus():
    return render_template('Postulacion/opcionesOAlu.html')

##############################################################################


###############################----Tablas de Vigo-----#####################################

#-------CRUD-LOGIN----------#

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

@app.route("/actualizarPerfil")
def actualizarPerfil():
    usuario=Usuarios()

    usuario.nombre = request.form['nombre']
    usuario.telefono = request.form['telefono']
    usuario.usuario = request.form['usuario']
    usuario.passwd = request.form['contraseña']
    usuario.actualizar()

    return redirect(url_for("principal"))

#-------CRUD-ALUMNOS----------#

@app.route('/registrarAlumno')
def registrarAlumno():
    carreras = Carreras()
    return render_template('AlumnosEgresados/AlumnosEgresados.html',carrera=carreras.consultaGeneral())

@app.route('/opcionesAlumno')
def opcionesAlumno():
    alumno=vAlumnos()
    return render_template('AlumnosEgresados/opcionesAlumnos.html',alumnos=alumno.consultaGeneral())

@app.route('/editarAlumnos/<int:id>')
def editarAlumnos(id):
    alumno=Alumnos()
    alumno.id_alumno=id
    return render_template('AlumnosEgresados/editarAlumnos.html',alumnos=alumno.consultaIndividual())

@app.route('/eliminarAlumno/<int:id>')
def eliminarAlumno(id):
    us=Usuarios()
    us.id_usuario=id
    us.estatus="Inactivo"
    us.actualizar()
    return redirect(url_for('opcionesAlumno'))

@app.route('/actualizarAlumno', methods=['POST'])
def actualzarAlumno():
    al=Alumnos()
    al.fecha_nacimiento=request.form['nacimiento']
    al.promedio=request.form['promedio']
    al.anioEgreso=request.form['egreso']
    al.actualizar()
    return redirect(url_for('opcionesAlumno'))

@app.route('/insertarAlumnosBD', methods=['POST'])
def insertAlumnosBD():
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


#-------CRUD-RECLUTADORES----------#

@app.route('/registrarReclutador')
def registrarReclutador():
    empresas = Empresas()
    return render_template('Reclutadores/Reclutadores.html',empresa=empresas.consultaGeneral())

@app.route('/opcionesReclutador')
def opcionesReclutador():
    reclutor=vReclutador()
    return render_template('Reclutadores/opcionesReclutadores.html',reclutador=reclutor.consultaGeneral())

@app.route('/insertarReclutadorBD', methods=['POST'])
def insertReclutadorBD():
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


#-------CRUD-PERSONAL-VINCULACION----------#

@app.route('/registrarPersonal')
def registrarPersonal():
    return render_template('PersonalVinculacion/PersonalVinculacion.html')

@app.route('/opcionesPersonal')
def opcionesPersonal():
    personal=vVinculacion()
    return render_template('PersonalVinculacion/opcionesPersonal.html',vinculacion=personal.consultaGeneral())

@app.route('/insertarPersonalBD', methods=['POST'])
def insertPersonalBD():
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
    
    return render_template('PersonalVinculacion/opcionesPersonal.html')

@app.errorhandler(404)
def error_404(e):
    return render_template('Comunes/error404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('Comunes/error500.html'), 500


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
